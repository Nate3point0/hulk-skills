---
name: wan-mps-patcher
description: >
  Verifies and re-applies all MPS compatibility patches for running Wan 2.2 TI2V 5B on Apple
  Silicon (M1/M2/M3/M4) via ComfyUI-WanVideoWrapper. Activate whenever the user says "check
  my patches", "did the update break things", "WanVideoWrapper updated", "re-apply MPS fixes",
  "patches missing", "ComfyUI broke after update", "patch TI2V", "verify wan patches", or
  whenever a WanVideoWrapper git pull or update has been run. Also fire proactively if the user
  reports a float64, fp8, OOM, or channel mismatch error in ComfyUI with the Wan model — these
  are the classic signs patches have been wiped. This skill is critical: a single `git pull` on
  WanVideoWrapper silently reverts all 3 patched files with no warning until runtime after a
  5-minute model load.
---

# wan-mps-patcher

Checks all 6 MPS patches required to run Wan 2.2 TI2V 5B on Apple Silicon, reports status,
and re-applies any that are missing.

## Background

ComfyUI-WanVideoWrapper is written for CUDA. Six patches are needed for Apple MPS. None are
upstream — a `git pull` or Manager update silently reverts them. Always run this after any
WanVideoWrapper update.

## Patch inventory

| # | File | What's patched | Symptom if missing |
|---|------|----------------|-------------------|
| 1 | `visual_pipeline.py` `wan_ti2v_api()` | `WanVideoTextEncode` gets `"device": "cpu"` | `Float8_e4m3fn to the MPS backend` at T5 encode |
| 2 | `wanvideo/modules/model.py` ~line 200 | `rope_params()`: `float64`→`float32` | `Cannot convert a MPS Tensor to float64 dtype` |
| 3 | `wanvideo/modules/model.py` ~lines 234,274 | `rope_apply`/`rope_apply_1d`: `.to(torch.float64)`→`.to(torch.float32)` | Same float64 error during sampling |
| 4 | `nodes_model_loading.py` ~line 1705 | patch_embedding 48→96ch via `sd[]` dict; keep `in_dim=48` | `expected input to have 48 channels, got 96` or `got 100` |
| 5 | `custom_linear.py` `_prepare_weight()` | fp8→uint8 reinterpret before CPU move | `Float8_e4m3fn to the MPS backend` at attention layers |
| 6 | `comfyui-start.sh` | `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0` | MPS OOM during VAE decode (255MB over ceiling) |

## Step 1 — Verify all patches

Run the checker script:

```bash
python ~/hulk-scripts/wan_mps_patcher.py --check
```

Read `references/patch-details.md` for the exact strings each check grep for.

The script outputs one of:
- ✅ `[PATCH N] present` — good
- ⚠️ `[PATCH N] MISSING` — needs re-application

## Step 2 — Re-apply missing patches

For any patch reported MISSING, run:

```bash
python ~/hulk-scripts/wan_mps_patcher.py --fix --patch N
```

Or fix all at once:

```bash
python ~/hulk-scripts/wan_mps_patcher.py --fix --all
```

The script makes a `.bak` backup of each file before editing.

## Step 3 — Restart ComfyUI

Patches to Python files take effect on next ComfyUI start. The env var patch (patch 6) is in
`comfyui-start.sh` so it's always picked up on restart.

```bash
kill $(pgrep -f "ComfyUI/main.py")
sleep 2
bash ~/hulk-scripts/comfyui-start.sh --background
```

## Step 4 — Verify with a quick test

```bash
sleep 20 && python ~/hulk-scripts/visual_pipeline.py ti2v \
  --image ~/Pictures/test.png \
  --steps 3 \
  --frames 5
```

3 steps / 5 frames completes in ~3 min and exercises all 6 patch sites.

---

## Architecture notes (for context when re-applying manually)

Read `references/patch-details.md` for exact code diffs for each patch if the automated
script fails or the file structure has changed significantly after an update.

Key constraints that must be preserved:
- **`transformer.in_dim` must stay 48** — if set to 96, sampler prepends a 4ch mask making
  input 100ch → crash. The `in_dim` field only controls mask-skip logic; the actual Conv3d
  channel count is what matters.
- **Patch `sd[]` dict, not `transformer.patch_embedding.weight`** — at patch time the
  transformer is built with `init_empty_weights()` so all weights are meta tensors. Must
  inject the real 96ch weight into the `sd` dict before `_replace_linear` materializes it.
- **fp8 uint8 trick order matters** — `w.view(torch.uint8)` first (reinterpret bytes as
  uint8, MPS can move uint8), then `.to(device="cpu")`, then `.view(orig_dtype)` back to fp8
  on CPU, then `.to(dtype=torch.float32)`. Any other order crashes.
