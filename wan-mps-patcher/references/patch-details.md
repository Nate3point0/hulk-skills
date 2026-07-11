# Patch Details — Exact diffs for each MPS fix

All paths relative to `~/` unless noted.

---

## Patch 1 — T5 on CPU (`visual_pipeline.py`)

**File:** `~/hulk-scripts/visual_pipeline.py`
**Function:** `wan_ti2v_api()`, node `"2"` (`WanVideoTextEncode`)
**Grep to verify:** `"device": "cpu"` inside `WanVideoTextEncode` inputs

```python
# MUST HAVE:
"2": {
    "class_type": "WanVideoTextEncode",
    "inputs": {
        ...
        "device": "cpu"   # ← THIS LINE
    },
}
```

**Why:** T5 encoder weights are fp8. MPS cannot cast fp8 tensors. Running on CPU avoids the
entire MPS dispatch path. Adds ~90s to encode but is the only reliable fix.

---

## Patch 2 — RoPE float64 in `rope_params()` (`model.py`)

**File:** `~/ComfyUI/custom_nodes/ComfyUI-WanVideoWrapper/wanvideo/modules/model.py`
**Location:** `rope_params()` function, ~line 200
**Grep to verify:** no `torch.float64` in `rope_params`

```python
# BEFORE (breaks MPS):
freqs = torch.arange(..., dtype=torch.float64)

# AFTER:
freqs = torch.arange(..., dtype=torch.float32)  # float64 unsupported on MPS
```

**Why:** MPS outright refuses float64 — not just a fallback miss, it hard errors.

---

## Patch 3 — RoPE float64 in `rope_apply` and `rope_apply_1d` (`model.py`)

**File:** Same as patch 2
**Locations:** `rope_apply()` ~line 234, `rope_apply_1d()` ~line 274
**Grep to verify:** no `.to(torch.float64)` in either function

```python
# BEFORE:
x_i = torch.view_as_complex(x[i, :seq_len].to(torch.float64).reshape(...))

# AFTER:
x_i = torch.view_as_complex(x[i, :seq_len].to(torch.float32).reshape(...))  # float64 unsupported on MPS
```

Apply in both `rope_apply` and `rope_apply_1d` — they have the same pattern.

---

## Patch 4 — patch_embedding 48→96ch (`nodes_model_loading.py`)

**File:** `~/ComfyUI/custom_nodes/ComfyUI-WanVideoWrapper/nodes_model_loading.py`
**Location:** After the `dual_controller` block (~line 1705), before `comfy_model.diffusion_model = transformer`
**Grep to verify:** `TI2V 5B detected` log string present in file

```python
# INSERT THIS BLOCK:
if "ti2v" in model.lower() and transformer.in_dim == 48:
    log.info("TI2V 5B detected — expanding patch_embedding from 48→96ch for image conditioning")
    old_pe = transformer.patch_embedding

    # 1. Patch sd[] dict BEFORE _replace_linear materializes weights
    pe_w = sd.get("patch_embedding.weight")   # [out, 48, kT, kH, kW]
    pe_b = sd.get("patch_embedding.bias")
    if pe_w is not None:
        new_w = torch.zeros(
            pe_w.shape[0], 96, *pe_w.shape[2:],
            dtype=torch.float32, device="cpu"
        )
        new_w[:, :48].copy_(pe_w.to(torch.float32))
        sd["patch_embedding.weight"] = new_w
    if pe_b is not None:
        sd["patch_embedding.bias"] = pe_b.to(torch.float32).clone()

    # 2. Replace meta Conv3d with 96-ch one (still meta — no data yet)
    with init_empty_weights():
        new_pe = nn.Conv3d(
            96, old_pe.out_channels,
            kernel_size=old_pe.kernel_size, stride=old_pe.stride, padding=old_pe.padding,
        )
    transformer.patch_embedding = new_pe
    transformer.original_patch_embedding = new_pe
    transformer.expanded_patch_embedding = new_pe
    # CRITICAL: keep in_dim=48 so sampler skips mask prepend (line 233 check)
    transformer.model_type = "i2v"
```

**Why NOT set `in_dim=96`:** Line 233 in `nodes_sampler.py` checks
`elif transformer.in_dim not in [48, 32]` → if True, prepends 4ch mask to image_cond(48ch)
= 52ch, then cat noise(48ch) = 100ch → `expected 96 channels, got 100`. Keep `in_dim=48`.

**Why NOT copy `old_pe.weight`:** At patch time transformer was built with `init_empty_weights()`
— all weights are meta tensors with no data. `Cannot copy out of meta tensor` error.

---

## Patch 5 — fp8 dequant on MPS (`custom_linear.py`)

**File:** `~/ComfyUI/custom_nodes/ComfyUI-WanVideoWrapper/custom_linear.py`
**Function:** `CustomLinear._prepare_weight()`
**Grep to verify:** `view(torch.uint8)` present in `_prepare_weight`

```python
def _prepare_weight(self, input):
    if self.is_gguf:
        weight = dequantize_gguf_tensor(self.weight).to(self.compute_dtype)
    else:
        w = self.weight
        # MPS cannot cast fp8 — reinterpret as uint8, move to CPU, view back, cast to f32
        _fp8_types = {torch.float8_e4m3fn, torch.float8_e5m2}
        for _attr in ("float8_e4m3fnuz", "float8_e5m2fnuz"):
            _t = getattr(torch, _attr, None)
            if _t is not None:
                _fp8_types.add(_t)
        if w.dtype in _fp8_types:
            orig_dtype = w.dtype
            orig_shape = w.shape
            w_cpu = w.view(torch.uint8).to(device="cpu").view(orig_dtype)
            w = w_cpu.to(dtype=torch.float32)
        weight = w.to(input)
    return weight
```

**Why the uint8 trick:** MPS supports uint8 device moves. fp8 device moves fail even when
just changing device (not dtype). Reinterpreting fp8 bytes as uint8 lets them move to CPU,
then reinterpreting back to fp8 on CPU, then casting to float32 on CPU works cleanly.
`w.to(device="cpu", dtype=torch.float32)` in one call fails — MPS dispatch intercepts it.

---

## Patch 6 — MPS memory ceiling (`comfyui-start.sh`)

**File:** `~/hulk-scripts/comfyui-start.sh`
**Grep to verify:** `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0` present

```bash
# ADD THIS LINE (after PYTORCH_ENABLE_MPS_FALLBACK=1):
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0
```

**Why:** After 26min of sampling the MPS allocator has ~6GB reserved. Default watermark
ratio (0.8) caps total at ~30.19GB. VAE decode upsampler needs 255MB more → hard OOM.
Setting ratio to 0.0 disables the ceiling — MPS uses all available unified memory.
Risk is low on M4 24GB unified; worst case falls back to swap rather than crashing.
