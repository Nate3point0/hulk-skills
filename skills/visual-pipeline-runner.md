# Visual Pipeline Runner

**Trigger:** When generating marketing visuals, product images, or promotional graphics

**Platforms:** Mac (local ComfyUI server), any OS with ComfyUI installed

**MCP Required:** Yes — ComfyUI MCP server + local GPU/CPU setup

## What It Does

Generates high-quality marketing visuals via a local ComfyUI pipeline. Creates product photos, funnel graphics, social media banners, and ad creatives without cloud costs or quality loss. Works with Stable Diffusion, SDXL, and other open-source models. Batch processing supported for multi-image campaigns.

## How to Use

1. Describe the visual you need (e.g., "Red automotive banner 1200x400 with 'Summer Sale' text")
2. Claude configures the ComfyUI workflow, applies your brand colors, and runs inference
3. Claude saves the image and posts it to your assets folder
4. Use directly in Systeme.io funnels or social media

## Notes

- ComfyUI setup: requires GPU (M1/M2/M3 preferred, CPU works but slow)
- Model files: SDXL is ~6GB, Stable Diffusion 1.5 is ~4GB — store on fast SSD
- Inference time: 30-60 seconds per image on M-series Mac, slower on CPU
- Batch mode: can queue 10-50 images overnight if running headless
- LoRA training: custom style models take 2-4 hours to train on dedicated GPU
- Quality tips: use DDIM sampler, 30-50 steps for best results without overhead
- Brand consistency: save your color palette as ComfyUI workflow template

---

**Created:** Nate (Ceepeezee), July 2026
**Last updated:** July 2026
**Status:** Production