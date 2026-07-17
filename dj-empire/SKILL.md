---
name: dj-empire
description: Operate the HULK Copyright-Safe DJ Empire — Audio Library scraper/downloader, mix renderer, setlist factory, distribution packaging, Systeme.io publishing. Triggers on "dj pipeline", "mix pack", "setlist", "audio library", "render mix", "download tracks", "dj product".
---

# DJ Empire — Operating Manual

All paths on HULK. Python = `/Volumes/HULK-STORAGE/00-SYSTEM/hulk/.venv/bin/python` (ALWAYS this venv).
Pipeline root: `/Volumes/HULK-STORAGE/00-SYSTEM/hulk/dj-pipeline/`

## The machine (5 stages, all built & proven 2026-07-16)

| Stage | Script | What it does |
|---|---|---|
| Scrape | `phase1_scraper.py` | YouTube Studio Audio Library → safe_tracks.db (216+ tracks) |
| Download | `phase1b_downloader.py` | Bulk-download licensed MP3s → HULK-AUDIO-OUTPUT/dj-pipeline-library/ (681 files) |
| Curate | `phase3_mix_builder.py` | DB → tracklist JSON/MD (`--genre "" ` to disable filter!) |
| Render | `phase3b_mix_renderer.py --mix NAME` | tracklist JSON → single crossfaded MP3 in rendered-mixes/ |
| Publish | `phase4_publisher.py` | adds squeeze step to DJ Page funnel 7150277 (NEVER create new funnels — plan at limit) |

Setlist factory (themed sellable song-list guides): `~/hulk/setlist_factory.py --next --tracks 60`
(daily 5:30am LaunchAgent com.hulk.setlist-factory; themes backlog in ~/hulk/setlist_themes.json;
kimi-k2 generates, code numbers/dedupes, evaluator gates at 6, one critique-revision pass).

## Non-negotiable gotchas
- Studio scrape/download needs the persistent Chrome profile (`secrets/chrome-profile`) from `phase1_scraper.py --login` — OAuth token CANNOT auth the web UI. Modern Chrome UA required or "unsupported browser" wall.
- Channel-scoped URL only: `studio.youtube.com/channel/{CID}/music`. Rows = `ytmus-library-row`, cells `.cell-body`, pagination via ytcp-table-footer (set 50/page).
- Ollama direct (`localhost:11434`) for local models — proxy RAG middleware overflows dolphin3.
- dolphin3 CANNOT do factual song lists; kimi-k2 via `_llm.chat` can. Never ask models for numbering or BPM.
- Audio Library license = claim-free monetized YouTube use. Commercial songs: sell the SETLIST (curation), never the audio; point buyers to record pools (BPM Supreme/DJCity).

## Distribution packaging (the MixPack pattern)
`HULK-AUDIO-OUTPUT/DISTRIBUTION/<Pack>/` with: `mixes/` (rendered MP3s), `library/` (source MP3s), `playlists/*.m3u8` (relative `../library/` paths → import into Traktor/Serato/rekordbox), README, UGC-INFOMERCIAL-SCRIPTS.md, DJ-SOFTWARE-IMPORT-GUIDE.md. Copy the one folder to a drive = done.
Reference example: `DISTRIBUTION/RapRnB-MixPack/` (100 tracks, 5 volumes, 1GB).

## Products live
- Vol.1 mix page: moto-city.systeme.io/25955975 · Line Dance Top 100: /38e4619b · Mexican Wedding: /cfe29baf
- Page content saved via official Systeme MCP `save_funnel_page_content` (works; REST funnel-create 422s).
