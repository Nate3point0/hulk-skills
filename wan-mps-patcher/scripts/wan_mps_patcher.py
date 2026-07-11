#!/usr/bin/env python3
"""
wan_mps_patcher.py — Verify and re-apply all MPS patches for Wan 2.2 TI2V 5B on Apple Silicon.

Usage:
  python ~/hulk-scripts/wan_mps_patcher.py --check
  python ~/hulk-scripts/wan_mps_patcher.py --fix --patch 4
  python ~/hulk-scripts/wan_mps_patcher.py --fix --all
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

HOME = Path.home()

# ── File paths ────────────────────────────────────────────────────────────────
VISUAL_PIPELINE  = HOME / "hulk-scripts/visual_pipeline.py"
MODEL_PY         = HOME / "ComfyUI/custom_nodes/ComfyUI-WanVideoWrapper/wanvideo/modules/model.py"
NODES_MODEL      = HOME / "ComfyUI/custom_nodes/ComfyUI-WanVideoWrapper/nodes_model_loading.py"
CUSTOM_LINEAR    = HOME / "ComfyUI/custom_nodes/ComfyUI-WanVideoWrapper/custom_linear.py"
COMFY_START      = HOME / "hulk-scripts/comfyui-start.sh"

# ── Colour helpers ────────────────────────────────────────────────────────────
def c(code, text): return f"\033[{code}m{text}\033[0m"
def ok(msg):  print(c("32", f"  ✅  [PATCH {msg}] present"))
def miss(msg): print(c("31", f"  ⚠️   [PATCH {msg}] MISSING — run --fix --patch {msg.split()[0]}"))
def info(msg): print(c("36", f"  ▶  {msg}"))
def fixed(msg): print(c("32;1", f"  🔧  {msg}"))
def err(msg):  print(c("31", f"  ✗  {msg}")); sys.exit(1)

# ── Check helpers ─────────────────────────────────────────────────────────────
def file_contains(path: Path, pattern: str) -> bool:
    if not path.exists():
        return False
    return pattern in path.read_text()

def backup(path: Path):
    bak = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, bak)
    info(f"Backup: {bak}")

# ── PATCH 1: T5 on CPU in visual_pipeline.py ─────────────────────────────────
def check_1():
    return file_contains(VISUAL_PIPELINE, '"device": "cpu"')

def fix_1():
    if check_1():
        info("Patch 1 already present."); return
    if not VISUAL_PIPELINE.exists():
        err(f"File not found: {VISUAL_PIPELINE}")
    backup(VISUAL_PIPELINE)
    text = VISUAL_PIPELINE.read_text()
    # Find WanVideoTextEncode block and add device: cpu
    old = '"force_offload": True,\n                "t5": ["1", 0],'
    new = '"force_offload": True,\n                "device": "cpu",\n                "t5": ["1", 0],'
    if old not in text:
        # Try alternate ordering
        old = '"t5": ["1", 0],\n                "force_offload": True,'
        new = '"t5": ["1", 0],\n                "device": "cpu",\n                "force_offload": True,'
    if old not in text:
        err("Patch 1: Cannot find insertion point in visual_pipeline.py — check manually.\n"
            "Add '\"device\": \"cpu\"' to the WanVideoTextEncode node inputs in wan_ti2v_api().")
    VISUAL_PIPELINE.write_text(text.replace(old, new, 1))
    fixed("Patch 1 applied: T5 device=cpu in visual_pipeline.py")

# ── PATCH 2: rope_params float64→float32 ─────────────────────────────────────
def check_2():
    if not MODEL_PY.exists(): return False
    lines = MODEL_PY.read_text().splitlines()
    # Find rope_params and scan its body (until next top-level def/class).
    # Ignore occurrences of 'float64' that appear only in comments (after #).
    in_func = False
    for line in lines:
        if re.match(r'^def rope_params\(', line):
            in_func = True
            continue
        if in_func:
            if re.match(r'^def |^class ', line):
                break  # left the function
            code_part = line.split('#')[0]  # strip comment
            if 'float64' in code_part:
                return False  # float64 still in actual code → patch missing
    return True  # no float64 in code (comments don't count)

def fix_2():
    if check_2():
        info("Patch 2 already present."); return
    if not MODEL_PY.exists():
        err(f"File not found: {MODEL_PY}")
    backup(MODEL_PY)
    text = MODEL_PY.read_text()
    # Replace float64 inside rope_params only
    def replace_in_func(src, func_name, old_str, new_str):
        pattern = rf'(def {func_name}\(.*?)({re.escape(old_str)})'
        return re.sub(pattern, lambda m: m.group(1) + new_str, src, count=1, flags=re.DOTALL)
    new_text = replace_in_func(text, "rope_params", "dtype=torch.float64", "dtype=torch.float32  # float64 unsupported on MPS")
    if new_text == text:
        err("Patch 2: Could not find dtype=torch.float64 in rope_params — check manually.")
    MODEL_PY.write_text(new_text)
    fixed("Patch 2 applied: rope_params float32 in model.py")

# ── PATCH 3: rope_apply + rope_apply_1d float64→float32 ──────────────────────
def check_3():
    if not MODEL_PY.exists(): return False
    text = MODEL_PY.read_text()
    for fn in ("rope_apply", "rope_apply_1d"):
        match = re.search(rf'def {fn}\(.*?\n(?=def )', text, re.DOTALL)
        if match and "float64" in match.group(0):
            return False
    return True

def fix_3():
    if check_3():
        info("Patch 3 already present."); return
    if not MODEL_PY.exists():
        err(f"File not found: {MODEL_PY}")
    backup(MODEL_PY)
    text = MODEL_PY.read_text()
    # Replace .to(torch.float64) → .to(torch.float32) in view_as_complex calls
    new_text = re.sub(
        r'(view_as_complex\([^)]*?)\.to\(torch\.float64\)',
        r'\1.to(torch.float32)  # float64 unsupported on MPS',
        text
    )
    if new_text == text:
        err("Patch 3: Could not find .to(torch.float64) in rope_apply — check manually.")
    MODEL_PY.write_text(new_text)
    fixed("Patch 3 applied: rope_apply float32 in model.py")

# ── PATCH 4: patch_embedding 48→96ch ─────────────────────────────────────────
PATCH_4_MARKER = "TI2V 5B detected — expanding patch_embedding"
PATCH_4_CODE = '''
        if "ti2v" in model.lower() and transformer.in_dim == 48:
            log.info("TI2V 5B detected — expanding patch_embedding from 48→96ch for image conditioning")
            old_pe = transformer.patch_embedding

            # 1. Patch sd[] dict BEFORE _replace_linear materializes weights (they are meta tensors now)
            pe_w = sd.get("patch_embedding.weight")
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

            # 2. Replace meta Conv3d with 96-ch one (still meta — _replace_linear fills it)
            with init_empty_weights():
                new_pe = nn.Conv3d(
                    96, old_pe.out_channels,
                    kernel_size=old_pe.kernel_size, stride=old_pe.stride, padding=old_pe.padding,
                )
            transformer.patch_embedding = new_pe
            transformer.original_patch_embedding = new_pe
            transformer.expanded_patch_embedding = new_pe
            # CRITICAL: keep in_dim=48 — sampler checks `in_dim not in [48,32]` to skip mask prepend
            # Setting in_dim=96 causes 4ch mask prepend → 100ch input → crash
            transformer.model_type = "i2v"
'''

def check_4():
    return file_contains(NODES_MODEL, PATCH_4_MARKER)

def fix_4():
    if check_4():
        info("Patch 4 already present."); return
    if not NODES_MODEL.exists():
        err(f"File not found: {NODES_MODEL}")
    backup(NODES_MODEL)
    text = NODES_MODEL.read_text()
    # Find insertion point: after dual_controller block, before comfy_model.diffusion_model
    target = "comfy_model.diffusion_model = transformer"
    if target not in text:
        err("Patch 4: Cannot find 'comfy_model.diffusion_model = transformer' — check nodes_model_loading.py manually.")
    insert_before = f"        {target}"
    new_text = text.replace(insert_before, PATCH_4_CODE + "\n        " + target, 1)
    if new_text == text:
        err("Patch 4: Replacement failed — check indentation in nodes_model_loading.py.")
    NODES_MODEL.write_text(new_text)
    fixed("Patch 4 applied: patch_embedding 48→96ch in nodes_model_loading.py")

# ── PATCH 5: fp8 uint8 reinterpret in custom_linear.py ───────────────────────
PATCH_5_MARKER = "view(torch.uint8)"
PATCH_5_PREPARE_WEIGHT = '''    def _prepare_weight(self, input):
        """Prepare weight tensor - handles both regular and GGUF weights"""
        if self.is_gguf:
            weight = dequantize_gguf_tensor(self.weight).to(self.compute_dtype)
        else:
            w = self.weight
            # MPS cannot cast fp8 dtype — dequantize via uint8 reinterpret on CPU.
            # Reinterpret fp8 bytes as uint8 (MPS can move uint8), move to CPU,
            # view back as fp8, cast to float32, then .to(input) sends to MPS as bf16.
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
'''

def check_5():
    return file_contains(CUSTOM_LINEAR, PATCH_5_MARKER)

def fix_5():
    if check_5():
        info("Patch 5 already present."); return
    if not CUSTOM_LINEAR.exists():
        err(f"File not found: {CUSTOM_LINEAR}")
    backup(CUSTOM_LINEAR)
    text = CUSTOM_LINEAR.read_text()
    # Find and replace the _prepare_weight method
    pattern = r'    def _prepare_weight\(self, input\):.*?(?=\n    def |\nclass |\Z)'
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        err("Patch 5: Cannot find _prepare_weight method in custom_linear.py — check manually.")
    new_text = text[:match.start()] + PATCH_5_PREPARE_WEIGHT + text[match.end():]
    CUSTOM_LINEAR.write_text(new_text)
    fixed("Patch 5 applied: fp8 uint8 reinterpret in custom_linear.py")

# ── PATCH 6: MPS watermark ratio in comfyui-start.sh ─────────────────────────
def check_6():
    return file_contains(COMFY_START, "PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0")

def fix_6():
    if check_6():
        info("Patch 6 already present."); return
    if not COMFY_START.exists():
        err(f"File not found: {COMFY_START}")
    backup(COMFY_START)
    text = COMFY_START.read_text()
    old = "export PYTORCH_ENABLE_MPS_FALLBACK=1"
    new = ("export PYTORCH_ENABLE_MPS_FALLBACK=1\n"
           "export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0  "
           "# Disable MPS memory ceiling — prevents VAE decode OOM after long sampling runs")
    if old not in text:
        err(f"Patch 6: Cannot find PYTORCH_ENABLE_MPS_FALLBACK in {COMFY_START} — add manually.")
    COMFY_START.write_text(text.replace(old, new, 1))
    fixed("Patch 6 applied: PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 in comfyui-start.sh")

# ── Registry ──────────────────────────────────────────────────────────────────
PATCHES = {
    1: ("T5 on CPU (visual_pipeline.py)", check_1, fix_1),
    2: ("RoPE float32 in rope_params (model.py)", check_2, fix_2),
    3: ("RoPE float32 in rope_apply/rope_apply_1d (model.py)", check_3, fix_3),
    4: ("patch_embedding 48→96ch (nodes_model_loading.py)", check_4, fix_4),
    5: ("fp8 uint8 reinterpret (custom_linear.py)", check_5, fix_5),
    6: ("MPS watermark ratio (comfyui-start.sh)", check_6, fix_6),
}

# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Wan 2.2 TI2V MPS patch checker/fixer")
    parser.add_argument("--check", action="store_true", help="Check all patches")
    parser.add_argument("--fix", action="store_true", help="Fix missing patches")
    parser.add_argument("--patch", type=int, help="Patch number (1-6)")
    parser.add_argument("--all", action="store_true", dest="all_patches", help="Fix all missing patches")
    args = parser.parse_args()

    if not args.check and not args.fix:
        parser.print_help(); sys.exit(0)

    print(f"\n\033[35;1m{'─'*54}\n  WAN MPS PATCHER — Wan 2.2 TI2V 5B on Apple Silicon\n{'─'*54}\033[0m\n")

    if args.check or args.fix:
        all_good = True
        missing = []
        for num, (desc, check_fn, _) in PATCHES.items():
            present = check_fn()
            if present:
                ok(f"{num} — {desc}")
            else:
                miss(f"{num} — {desc}")
                missing.append(num)
                all_good = False

        print()
        if all_good:
            print(c("32;1", "  ✅  All 6 patches verified. TI2V should run on MPS.\n"))
        else:
            print(c("33", f"  ⚠️   {len(missing)} patch(es) missing: {missing}\n"))

    if args.fix:
        targets = []
        if args.all_patches:
            targets = [n for n in PATCHES if not PATCHES[n][1]()]
        elif args.patch:
            targets = [args.patch]
        else:
            parser.error("--fix requires --patch N or --all")

        if not targets:
            print(c("32", "  Nothing to fix — all selected patches already present.\n"))
            return

        print(c("35;1", f"  Applying {len(targets)} patch(es): {targets}\n"))
        for num in targets:
            _, _, fix_fn = PATCHES[num]
            fix_fn()

        print()
        print(c("33", "  ⚠️   Restart ComfyUI for patches to take effect:"))
        print(c("36", "       kill $(pgrep -f 'ComfyUI/main.py')"))
        print(c("36", "       bash ~/hulk-scripts/comfyui-start.sh --background\n"))

if __name__ == "__main__":
    main()
