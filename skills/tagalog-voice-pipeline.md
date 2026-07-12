# Tagalog Voice Pipeline

**Trigger:** When generating Tagalog TTS (text-to-speech), translating content, or creating voice content

**Platforms:** Mac (local MMS-TTS + Ollama LLM setup)

**MCP Required:** Yes — MMS-TTS MCP + Ollama translation model

## What It Does

Full local Tagalog text-to-speech and translation pipeline. Converts English or Tagalog text to natural-sounding Tagalog audio, handles dialect variations, and includes commercial licensing guards for resale/public use. No cloud dependency, no cost per request, full privacy.

## How to Use

1. Provide English text or Tagalog content that needs voice
2. Claude translates (if needed) and generates MP3 audio via MMS-TTS
3. Claude checks commercial licensing and creates derivative work records
4. Save the audio file and use in courses, funnels, or products

## Notes

- MMS-TTS model: ~200MB, supports 1000+ languages including Tagalog
- Audio quality: natural sounding, ~200-300ms latency on M-series Mac
- Licensing: MMS-TTS is open source (MIT), safe for commercial use
- Dialect support: can generate Quezon City (standard) or Iloilo/Mindanao variants
- Batch processing: queue up to 50 conversions for overnight runs
- Rate limiting: none locally, but inference queues if running multiple models
- Storage: each minute of audio ~300KB MP3, budget accordingly for courses
- Resale rules: document that audio is AI-generated; some jurisdictions require disclosure

---

**Created:** Nate (Ceepeezee), July 2026
**Last updated:** July 2026
**Status:** Production