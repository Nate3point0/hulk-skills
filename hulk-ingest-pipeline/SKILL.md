---
name: hulk-ingest-pipeline
description: Set up or extend a multi-source AI knowledge ingestion pipeline on a local AI server (HULK-style Mac Mini setup with BrainVault/RAG). Use this skill whenever the user wants to get files from ANY platform (Kimi Claw, Notion, Google Drive, Dropbox, ChatGPT exports, Claude exports, etc.) into their local AI system so it can be searched and referenced in conversation. Make sure to trigger this whenever the user mentions "ingest," "pipeline," "watcher," "drop folder," "BrainVault," "RAG," "index my files," "get files onto my server," "feed my AI system," "point my AI at this folder," or wants a new platform/source added to an existing ingestion setup — even if they don't use the word "pipeline" explicitly. Also trigger if the user asks why their AI server "doesn't remember" or "isn't using" imported files — that's usually a missing RAG-wiring step this skill covers.
---

# HULK Multi-Source Ingestion Pipeline

## What this skill builds

A repeatable pattern for getting files from any external platform into a
local AI system so they're both **stored** and **actually used in
conversation** — not just sitting on disk. There are three distinct pieces,
and skipping any one of them is the most common way this kind of system
ends up half-working:

1. **Intake watcher** — classifies dropped files by type and routes them
   to the right destination (docs/knowledge files vs. code vs. junk).
2. **Embedding/indexing** — turns text content into vector embeddings so
   it's semantically searchable, not just grep-able.
3. **Retrieval wiring** — makes sure whatever the user actually talks to
   (a chat proxy, an assistant, a CLI) queries the embedded knowledge
   *before* answering, with a relevance threshold so irrelevant questions
   don't get noise injected.

If the user's problem is "I dropped files in and my AI still doesn't know
about them," suspect step 2 or 3 is missing — most people get step 1 working
and stop there, which only solves storage, not retrieval.

## When to use which mode

**New source onboarding** (most common request): the user already has this
pipeline running for one platform and wants to add another. This is
deliberately cheap — see "Onboarding a new source" below. Don't rebuild
anything; just create a folder.

**First-time setup**: the user has no ingestion pipeline yet. Walk through
all three pieces below in order.

**Diagnosing "it's not working"**: ask which of the three pieces (intake,
embedding, retrieval) is confirmed working, and isolate from there. Most
"broken" reports are actually step 3 missing, not a bug.

## Step 1: Intake watcher

Use `scripts/ingest_watcher.py` as the template. It's designed to be
source-agnostic from the start — don't hardcode a single platform's name,
because the whole point of doing this once is that step 2, 3, ... N
platforms shouldn't require touching the script again.

Key design decisions baked into this script (keep these when adapting it):

- **Discovers sources by folder convention** (`INBOX/FROM-<SOURCE>/_drop/`)
  rather than a hardcoded path. Adding platform #2 is `mkdir`, not a code
  edit.
- **Classifies by file extension** into markdown/text (goes to the
  knowledge base), code, documents, and unsorted/junk. Adjust the
  extension sets to the user's actual file types if they differ.
- **State-tracked** via a JSON file keyed by resolved path + mtime, so
  restarts don't reprocess old files and nothing gets silently duplicated.
- **Non-destructive** — moves, never deletes. Preserves subfolder structure
  when a whole export folder (not just loose files) gets dropped in.
- **Stdlib only** — no dependency on `watchdog` or similar, so it runs on
  any stock Python 3 without a fragile venv requirement for this piece
  specifically (the embedding step is a different story — see Step 2).

Ask the user for their actual paths (storage volume, knowledge base
location, inbox location) rather than assuming — the constants at the top
of the script are the only thing that should need editing per-deployment.

## Step 2: Embedding / indexing

This is usually already running if the user has any RAG setup at all — the
watcher's job is just to route markdown/text content to wherever that
indexer watches. Confirm with the user:

- What embeds their files into a vector store (a script? a service?)
- Where is the vector DB file/instance?
- Is the indexing service actually running right now (`launchctl list` /
  `systemctl status` / equivalent), not just installed?

If nothing exists yet, that's a bigger build (embedding model choice,
vector store choice, chunking strategy) — flag it as a separate task rather
than bolting it onto the intake watcher.

## Step 3: Retrieval wiring (the step people forget)

Storing embeddings does nothing for the user's actual conversations unless
whatever they talk to is wired to query the vector store first. Check:

- Does the chat interface / proxy / API layer the user actually talks
  through call the vector store before generating a response?
- Is there a **relevance threshold**? Don't inject retrieved chunks
  unconditionally — an irrelevant question (weather, unrelated code) still
  paying a retrieval cost and getting noise injected degrades quality and
  wastes latency. Use a distance/similarity cutoff so retrieval only
  activates when there's an actual match.

Reference `references/rag_bridge_pattern.md` for the specific pattern used
in the HULK deployment (proxy-level injection with a cosine-distance
threshold, toggleable via environment variable).

## Onboarding a new source

Once the pipeline exists for platform #1, adding platform #2+ should never
require touching the watcher script. Just:

```bash
mkdir -p <INBOX_ROOT>/FROM-<NEW_SOURCE>/_drop
```

Confirm with the user that the watcher's polling loop re-discovers new
source folders each cycle (the bundled script does this) rather than only
scanning sources it knew about at startup — this is what makes onboarding
truly free.

## Verification checklist (always run before calling this "done")

Don't consider the pipeline complete until all four of these are true —
each one has failed silently in real deployments:

1. **Drop a real file, confirm it moves** — check the destination folder
   and the watcher's log within one polling interval.
2. **Audit the "unsorted/junk" bucket** — if a meaningful fraction of files
   land there, check whether they're legitimately unclassifiable
   (binaries, build artifacts) or whether the classifier is missing a
   real content type. Don't assume "sorted" numbers without a spot check.
3. **Confirm embedding actually happened** — query the vector store
   directly for something you know is in a newly-dropped file, don't just
   trust that the indexer service is "running."
4. **Test retrieval with an on-topic AND an off-topic question** — the
   on-topic one should surface the imported content; the off-topic one
   should NOT inject irrelevant chunks or add unnecessary latency. Both
   failure modes (never retrieves / always retrieves) are common and
   easy to miss if you only test the happy path.

## Bundled files

- `scripts/ingest_watcher.py` — the source-agnostic intake watcher,
  ready to adapt to a new deployment's paths.
- `scripts/launchd_template.plist` — macOS background-service template
  for keeping the watcher running persistently. Swap in the real paths
  and interpreter before use. (Linux users: convert to a systemd unit —
  same ProgramArguments/WorkingDirectory concept.)
- `references/rag_bridge_pattern.md` — the retrieval-wiring pattern
  (relevance threshold, environment-variable toggles) for Step 3.
- `references/install_checklist.md` — copy-paste command sequence for a
  fresh install, plus the onboarding-a-new-source shortcut.
