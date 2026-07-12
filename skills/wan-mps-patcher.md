# WAN MPS Patcher

**Trigger:** When verifying or re-applying MPS patches for Wan 2.2 TI2V video generation

**Platforms:** macOS (Apple Silicon M1/M2/M3, Apple Neural Engine)

**MCP Required:** No

## What It Does

Verifies and re-applies MPS (Metal Performance Shaders) patches for Wan 2.2 TI2V (text-to-image-to-video) on Apple Silicon. Fixes GPU acceleration issues, VRAM leaks, and inference timeouts. Ensures consistent video generation quality and speed on Mac.

## How to Use

1. Run into slow video generation or GPU crashes on Wan 2.2
2. Say: "Patch Wan MPS pipeline"
3. Claude checks current patches, identifies breaks, re-applies fixes
4. Inference resumes at normal speed (60-90 sec per video on M3)

## Notes

- MPS support: Wan 2.2 officially added MPS support in v2.2.1 (check version first)
- PyTorch version: requires PyTorch 2.0+ with metal support compiled
- VRAM management: 8GB VRAM can generate 30-60 second videos; 16GB+ is comfortable
- Patch location: typically in site-packages/wan2/mps_accelerator.py
- Common breaks: PyTorch updates sometimes overwrite patches; check after `pip install --upgrade`
- Performance: MPS-accelerated inference is 3-4x faster than CPU on M-series
- Known issue: audio mixing sometimes fails with MPS — fallback to CPU for audio post-processing
- Reinstall cleanly: if patches fail repeatedly, `pip uninstall wan2 && pip install wan2` from scratch

---

**Created:** Nate (Ceepeezee), July 2026
**Last updated:** July 2026
**Status:** Production