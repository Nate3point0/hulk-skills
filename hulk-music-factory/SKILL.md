---
name: hulk-music-factory
description: >
  Automate music asset production: generate sample packs, MIDI loops, organize for Systeme.io upload.
  Use when: "generate audio pack", "create MIDI loops", "package for Systeme.io", "bundle samples", 
  "prepare for distribution". Provides parallel audio synthesis, music theory MIDI generation, and 
  genre-based packaging with checksums and manifests. Outputs ready for bulk upload/sale.

compatibility: |
  - Python 3.8+ with: numpy, soundfile, librosa, mido
  - Bash 4.0+
  - Utilities: zip, ffmpeg (optional, for MP3 preview generation)
  - Output directories: ~/hulk-output/music-assets/, ~/hulk-output/midi-loops/, ~/hulk-output/products/
---

# HULK Music Factory Skill

## Overview

This skill automates the full music asset production pipeline used for creating and distributing digital products via Systeme.io. It's designed to run unattended overnight and produce marketplace-ready sample packs, training datasets, and MIDI libraries.

Three production scripts work together:

1. **Audio Synthesis** (night-synthesis-v2-parallel.sh) → 550+ original audio files
2. **MIDI Generation** (night-midi-generation.py) → 1000+ music theory-aware loops
3. **Packaging & Distribution** (asset-packager.py) → Systeme.io-ready ZIP bundles with metadata

All outputs are organized by genre, checksummed for integrity, and include CSV manifests for bulk import.

## When to Use This Skill

**Trigger scenarios:**
- User asks to "generate a sample pack" or "create drum loops"
- User needs assets "ready for Systeme.io" or "for bulk upload"
- User requests "batch MIDI generation" or "1000 loops"
- User wants to "package audio by genre" or "organize samples for distribution"
- User needs to "prepare training data" for AI models
- User says "package for distribution" or "create product bundles"

**Not appropriate if:**
- User wants to edit/process existing audio (use DAW tools instead)
- User needs real-time audio synthesis (use synthesizer software)
- User wants to analyze or transcribe audio (use music analysis tools instead)

## Quick Start

### Generate Audio Sample Pack

```bash
# 1. Synthesis (parallel generation, ~15-20 min)
bash scripts/night-synthesis-v2-parallel.sh

# 2. Packaging (organize by genre, ~1-2 min)
python3 scripts/asset-packager.py

# Output: ~/hulk-output/products/UPLOAD_MANIFEST.json
```

### Generate MIDI Loop Library

```bash
# 1. MIDI generation (theory-aware, ~30-60 min)
python3 scripts/night-midi-generation.py

# 2. Package for distribution
# (Same asset-packager handles MIDI + audio)
python3 scripts/asset-packager.py
```

### Full Unattended Pipeline

```bash
# Launch the orchestrator (synthesis + MIDI + packaging)
bash scripts/hulk-night-factory-launcher.sh

# Watch progress
tail -f ~/hulk-logs/factory.log
```

## Output Format

### Directory Structure

```
~/hulk-output/
├── music-assets/          # Raw audio from synthesis
│   ├── drums/            # 200+ kick/snare/clap/hihat files
│   ├── synths/           # 150+ melodic synth sounds
│   ├── bass/             # 120+ sub/wobble bass hits
│   └── fx/               # 80+ risers/impacts/transitions
├── midi-loops/           # Raw MIDI from generation
│   ├── trap/             # 200 trap MIDI loops
│   ├── drill/            # 200 drill MIDI loops
│   ├── rnb/              # 200 R&B MIDI loops
│   ├── hyperpop/         # 200 hyperpop MIDI loops
│   └── lofi/             # 200 lofi MIDI loops
└── products/             # Ready-to-upload bundles
    ├── trap-bundle.zip
    ├── drill-bundle.zip
    ├── [other genres...]
    └── UPLOAD_MANIFEST.json  # Master index
```

### Manifest Format

Each genre bundle includes:
- **All WAV/MIDI files** - organized by instrument type
- **MANIFEST.csv** - file inventory with checksums and metadata
- **systeme-meta.json** - product specs for Systeme.io importer
- **UPLOAD_MANIFEST.json** (root level) - master index of all bundles

Example manifest entry:
```json
{
  "genre": "trap",
  "zip_file": "trap-bundle.zip",
  "zip_size_mb": 22.5,
  "product_name": "TRAP Audio Pack",
  "file_count": 316
}
```

## Configuration & Parameters

### Audio Synthesis Settings

Edit `scripts/night-synthesis-v2-parallel.sh` to adjust:
- **DRUMS**: `total = 200` (change to 300, 400, etc.)
- **SYNTHS**: `total = 150`
- **BASS**: `total = 120`
- **FX**: `total = 80`

Total output: 550 files (adjustable). Parallel execution: 4 generators running concurrently.

### MIDI Generation Settings

Edit `scripts/night-midi-generation.py` to adjust:
- **GENRES**: trap, drill, rnb, hyperpop, lofi (add custom as needed)
- **BPM RANGES**: Customize per genre (trap: 130-150, drill: 140-150, etc.)
- **SCALES**: minor, major, phrygian, dorian (add more as needed)
- **LOOPS_PER_GENRE**: 200 (change to 100, 300, etc.)

Total output: 1000 MIDI files (5 genres × 200 loops).

## Examples

### Example 1: Create Trap Sample Pack

**User request:** "Generate 200 trap drum samples, organize by type, and create a ZIP ready for Systeme.io"

```bash
# Synthesis generates 200 drum files (kick, snare, clap, hihat)
# Asset packager groups by genre
# Output: trap-bundle.zip with 200 drum files + MANIFEST.csv
```

**Output:** `~/hulk-output/products/trap-bundle.zip`

Files in bundle:
- 50× trap_kick_*.wav
- 50× trap_snare_*.wav
- 50× trap_clap_*.wav
- 50× trap_hihat_*.wav
- MANIFEST.csv (checksummed inventory)
- systeme-meta.json (product metadata)

### Example 2: Create MIDI Training Dataset

**User request:** "Generate 1000 MIDI loops for training a model, organized by genre"

```bash
# MIDI generation creates 200 loops per genre × 5 genres
# Each loop has melody + bassline tracks
# Asset packager bundles by genre
# Output: 5 ZIP files ready for ML training
```

**Output:** `~/hulk-output/products/` contains:
- trap-bundle.zip (200 MIDI loops)
- drill-bundle.zip (200 MIDI loops)
- rnb-bundle.zip (200 MIDI loops)
- hyperpop-bundle.zip (200 MIDI loops)
- lofi-bundle.zip (200 MIDI loops)

### Example 3: Full Product Pipeline (Unattended Overnight)

**User request:** "Generate everything overnight — audio, MIDI, package for Systeme.io upload"

```bash
# Launch orchestrator
nohup bash scripts/hulk-night-factory-launcher.sh &

# Watch progress
tail -f ~/hulk-logs/factory.log

# Result next morning:
# - 550+ audio files (organized by category)
# - 1000+ MIDI loops (organized by genre)
# - 11 genre bundles ready for upload
# - UPLOAD_MANIFEST.json with all specs
```

## Technical Details

### Audio Synthesis (night-synthesis-v2-parallel.sh)

- **Parallel execution**: 4 bash functions run concurrently using `&`
- **Checkpoint/resume**: Each category saves progress to JSON (survives crashes)
- **Sample rate**: 44100 Hz (44.1 kHz CD quality)
- **Audio codec**: WAV (uncompressed, 16-bit)
- **Normalization**: All samples peak-normalized to -3dB for safety headroom
- **Metadata**: Filename encoding includes genre, type, BPM, and scale/pitch info

**Example filename:** `trap_kick_0001_140bpm.wav`
- Genre: trap
- Type: kick
- Index: 0001
- BPM: 140

### MIDI Generation (night-midi-generation.py)

- **Music theory**: Scale-aware note selection (minor, major, phrygian, dorian)
- **BPM ranges**: Genre-specific (trap: 130-150, lofi: 70-90, etc.)
- **Structure**: 8-bar loops with melody + bass tracks
- **Humanization**: Random note durations and velocities (60-110)
- **MIDI format**: Standard SMF (Standard MIDI File), compatible with all DAWs
- **Metadata**: Filename includes genre, BPM, scale, and note root

**Example filename:** `trap_loop_0001_140bpm_minor.mid`

### Packaging (asset-packager.py)

- **Grouping**: Files automatically grouped by genre (first word of filename)
- **Checksums**: SHA256 (truncated to 16 chars) for integrity verification
- **Manifests**: CSV with columns: filename, filesize_kb, checksum, path
- **Metadata JSON**: Includes product name, file count, total size, creation timestamp
- **ZIP compression**: Standard DEFLATE, compatible with all OS (macOS, Windows, Linux)

## Troubleshooting

### Synthesis stalls or crashes

**Issue**: Process stops mid-generation

**Solution**: Check `~/hulk-logs/night-synthesis-v2.log`
```bash
tail -100 ~/hulk-logs/night-synthesis-v2.log
```

If a category failed, checkpoint JSON exists in `~/hulk-checkpoints/`. Delete it to restart from scratch, or edit the JSON to resume from a specific count.

### Missing dependencies

**Issue**: "ModuleNotFoundError: No module named 'soundfile'"

**Solution**: Install dependencies
```bash
pip install soundfile librosa mido numpy --break-system-packages
```

### ZIP creation fails

**Issue**: "zip: command not found"

**Solution**: Install zip utility
```bash
brew install zip  # macOS
apt-get install zip  # Linux
```

### Packager finds no files

**Issue**: "Found 0 genres"

**Cause**: Synthesis scripts haven't run yet, or output directory path is wrong.

**Solution**: Verify synthesis completed
```bash
ls ~/hulk-output/music-assets/*/
```

Should show .wav files. If empty, rerun synthesis.

## Advanced: Custom Genres & Scales

### Add a Custom Scale

Edit `night-midi-generation.py` and add to `SCALES`:
```python
SCALES = {
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "custom_scale": [0, 1, 3, 5, 6, 8, 10]  # Your scale intervals
}
```

### Add a Custom Genre

Edit `night-midi-generation.py` and add to `GENRES`:
```python
GENRES = {
    "my_genre": {
        "bpm": [120, 130, 140],
        "scale": "custom_scale",
        "pattern": "custom"
    }
}
```

Then add handling in `generate_loop()` if your pattern is unique.

## Integration with Systeme.io

1. **Export UPLOAD_MANIFEST.json** from `~/hulk-output/products/`
2. **Open Systeme.io** → Products → Bulk Import
3. **Upload each ZIP bundle** listed in the manifest
4. **Auto-populate** product name, description, file count from metadata
5. **Set pricing** and publish
6. **Link to funnels** (email sequences, landing pages, checkout)

## Performance & Costs

### Typical Output Sizes

| Pipeline | Files | Size | Runtime |
|----------|-------|------|---------|
| Audio only | 550 | 214MB | ~15 min |
| MIDI only | 1000 | ~150MB | ~30-60 min |
| Full (both) | 1550 | ~364MB | ~2 hours |

### Hardware Requirements

- **CPU**: 4+ cores recommended (parallel synthesis uses all cores)
- **RAM**: 8GB+ (NumPy array generation)
- **Storage**: 500MB for outputs
- **Network**: None required (fully local generation)

## Next Steps

After running the factory:
1. **Download bundles** from `~/hulk-output/products/`
2. **QA check**: Listen to sample files, verify MIDI timing
3. **Customize**: Edit bundle descriptions, pricing, product images
4. **Upload to Systeme.io**: Use bulk importer with UPLOAD_MANIFEST.json
5. **Distribute**: Link products to your funnels, promote on social media

---

## Scripts Reference

All scripts are in `scripts/`:
- `night-synthesis-v2-parallel.sh` - Audio generation (bash)
- `night-midi-generation.py` - MIDI generation (Python)
- `asset-packager.py` - Packaging & bundling (Python)
- `hulk-night-factory-launcher.sh` - Full orchestrator (bash)

Run any script standalone or use the orchestrator for unattended execution.
