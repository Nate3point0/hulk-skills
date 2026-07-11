---
name: visual-pipeline-runner
description: >
  Generates marketing visuals — product images, thumbnails, animated clips, social media graphics —
  using the local ComfyUI pipeline (visual_pipeline.py on Hulk/MacBook). Activate whenever the user
  says "generate an image", "make a thumbnail", "create a visual for", "animate this photo",
  "make a product shot", "generate marketing images", "create a video clip from this image",
  "batch generate visuals", "make social media images", "render a promo video", or any request
  for visual content that should be AI-generated locally. Also fire when the user pastes an image
  and says "animate this" or "make a video from this". Routes fast stills to flux_schnell and
  animations to TI2V automatically — user doesn't need to know the model names.
---

# visual-pipeline-runner

Generates marketing visuals via the local ComfyUI engine. Two modes:

- **🖼️ Image** (flux_schnell) — fast, high-quality stills in ~30s. Use for thumbnails, product shots, social graphics, cover art.
- **🎬 Video** (Wan 2.2 TI2V) — animates a source image into a short clip (~27min on M4 Pro 24GB). Use for promo loops, animated thumbnails, product reveals.

## Before You Start

Confirm ComfyUI is running:

```bash
curl -s http://127.0.0.1:8188/system_stats | python3 -c "import sys,json; print('✅ ComfyUI online')" 2>/dev/null || echo "❌ ComfyUI offline — run: bash ~/hulk-scripts/comfyui-start.sh"
```

If offline, start it:
```bash
bash ~/hulk-scripts/comfyui-start.sh
sleep 20  # wait for model server to initialize
```

---

## 🖼️ MODE 1 — Generate Still Images (flux_schnell)

**Best for:** thumbnails, social posts, product shots, cover art, backgrounds

### Usage

```bash
python ~/hulk-scripts/visual_pipeline.py image \
  --prompt "YOUR PROMPT HERE" \
  --width 1024 \
  --height 1024 \
  --steps 4
```

### Common presets

| Use case | Width | Height | Steps | Notes |
|----------|-------|--------|-------|-------|
| YouTube thumbnail | 1280 | 720 | 4 | Standard 16:9 |
| Instagram square | 1024 | 1024 | 4 | Default |
| Instagram portrait | 832 | 1040 | 4 | 4:5 ratio |
| Twitter/X banner | 1500 | 500 | 4 | Wide crop |
| TikTok/Reels cover | 1080 | 1920 | 6 | 9:16 vertical |
| Product shot | 1024 | 1024 | 8 | More steps = finer detail |

### Prompt formula that works well

```
[subject], [style], [lighting], [mood], professional product photography, 
high detail, 8k, commercial quality
```

**Examples:**
```bash
# YouTube thumbnail — AI music tool
python ~/hulk-scripts/visual_pipeline.py image \
  --prompt "neon glowing musical notes floating around a laptop, dark studio background, purple and gold lighting, cinematic, professional product photography" \
  --width 1280 --height 720

# Systeme.io product cover
python ~/hulk-scripts/visual_pipeline.py image \
  --prompt "sleek digital dashboard showing revenue charts going up, modern flat design, blue gradient, clean minimalist" \
  --width 1024 --height 1024

# TikTok hook frame
python ~/hulk-scripts/visual_pipeline.py image \
  --prompt "close up of hands on DJ controller, dynamic motion blur, concert lights, energetic, cinematic" \
  --width 1080 --height 1920
```

### Output

Images save to `~/ComfyUI/output/` as `hulk_image_NNNNN_.png`.

---

## 🎬 MODE 2 — Animate an Image (Wan 2.2 TI2V)

**Best for:** animated thumbnails, promo loops, product reveals, social video content

**Requirements:**
- Source image at 832×480 or similar 16:9 (script handles resize)
- MPS patches verified (run `python ~/hulk-scripts/wan_mps_patcher.py --check` first)
- ~27min per clip on M4 Pro 24GB

### Usage

```bash
python ~/hulk-scripts/visual_pipeline.py ti2v \
  --image ~/Pictures/YOUR_IMAGE.png \
  --prompt "MOTION DESCRIPTION" \
  --frames 41 \
  --steps 20
```

### Frame count guide

| Frames | Duration @ 24fps | Time to render | Use case |
|--------|-----------------|----------------|----------|
| 17 | ~0.7s | ~12min | Quick loop / boomerang |
| 41 | ~1.7s | ~27min | Standard promo clip ✅ recommended |
| 57 | ~2.4s | ~38min | Extended reveal |

### Motion prompt formula

```
[subject] [motion verb], [camera move], [atmosphere]
```

**Examples:**
```bash
# Animate a product photo
python ~/hulk-scripts/visual_pipeline.py ti2v \
  --image ~/Pictures/product_shot.png \
  --prompt "product slowly rotating, camera zooming in gently, soft studio lighting, premium feel"

# Animate a person/artist photo  
python ~/hulk-scripts/visual_pipeline.py ti2v \
  --image ~/Pictures/artist.png \
  --prompt "subtle breathing motion, eyes blinking slowly, camera slowly pushing in, cinematic portrait"

# Animate a landscape/background
python ~/hulk-scripts/visual_pipeline.py ti2v \
  --image ~/Pictures/bg.png \
  --prompt "clouds drifting slowly, light rays shifting, peaceful and atmospheric"
```

### Output

Video saves to `~/ComfyUI/output/` as `hulk_ti2v_NNNNN_.mp4` (H.264, 24fps).

**MPS patches check** (always run before TI2V if WanVideoWrapper was recently updated):
```bash
python ~/hulk-scripts/wan_mps_patcher.py --check
```

---

## 🔁 BATCH MODE — Multiple Images from One Prompt List

Generate a set of variations or different images for a campaign:

```bash
# Create a prompt file
cat > /tmp/batch_prompts.txt << 'EOF'
neon music producer at desk, purple lighting, cinematic, 8k
vinyl records floating in space, colorful, abstract, commercial
DJ booth at night club, laser lights, crowd energy, professional
EOF

# Run batch (loop in bash)
while IFS= read -r prompt; do
  python ~/hulk-scripts/visual_pipeline.py image \
    --prompt "$prompt" \
    --width 1280 --height 720
  sleep 5  # brief pause between jobs
done < /tmp/batch_prompts.txt
```

---

## Marketing Visual Workflow (End-to-End)

For a complete Systeme.io product launch visual set:

```bash
# 1. Hero image (product cover)
python ~/hulk-scripts/visual_pipeline.py image \
  --prompt "YOUR PRODUCT CONCEPT, professional, high detail" \
  --width 1024 --height 1024

# 2. YouTube thumbnail (16:9)
python ~/hulk-scripts/visual_pipeline.py image \
  --prompt "same concept, dramatic, eye-catching thumbnail style, bold" \
  --width 1280 --height 720

# 3. TikTok/Reels vertical
python ~/hulk-scripts/visual_pipeline.py image \
  --prompt "same concept adapted for mobile vertical, close crop, punchy" \
  --width 1080 --height 1920

# 4. Animate the hero image into a promo loop
python ~/hulk-scripts/visual_pipeline.py ti2v \
  --image ~/ComfyUI/output/hulk_image_00001_.png \
  --prompt "subtle animation, product reveal, cinematic"
```

All outputs land in `~/ComfyUI/output/` — move to your content folder when done:
```bash
ls -lt ~/ComfyUI/output/ | head -10
```

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `ComfyUI is not running` | `bash ~/hulk-scripts/comfyui-start.sh && sleep 20` |
| TI2V float64/fp8 error | `python ~/hulk-scripts/wan_mps_patcher.py --fix --all` |
| TI2V MPS OOM at step 0 | Reduce `--frames` to 17 or 41 (not 81) |
| TI2V MPS OOM in VAE decode | Check `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0` is in `comfyui-start.sh` |
| Image looks wrong resolution | Check `--width` and `--height` are multiples of 64 |
| Output not found | Check `~/ComfyUI/output/` — may be named differently |

See `references/prompt-library.md` for proven prompt templates by use case.
