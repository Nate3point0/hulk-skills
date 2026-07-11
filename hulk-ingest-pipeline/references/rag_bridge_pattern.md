# RAG Bridge Pattern — Retrieval Wiring

This is the pattern that closes the gap between "files are stored and
embedded" and "the AI actually uses them when you talk to it." Proven in
production on a HULK-style local deployment (proxy on localhost:4000,
sqlite-vec backed vector store called `brainvault.db`).

## The core problem

Two separate systems can each be "working" and the user still gets no
value:

- An intake watcher moves files into the right folders. ✓ working
- An indexer embeds markdown/text into a vector DB. ✓ working
- ...but the chat interface the user actually talks to never queries that
  vector DB. Nothing is wrong, exactly — it's just that nobody wired step
  3\. This is the most common reason someone says "I imported all this
  stuff and my AI still doesn't know about it."

## The fix: inject at the proxy/API layer, not per-conversation

Rather than requiring the user to manually run a query script every time,
wire retrieval into whatever layer sits between the user and the model
(an API proxy, a middleware layer, a custom chat backend). On every
incoming request:

1. Extract the user's question/prompt text.
2. Embed it with the same embedding model used to index the knowledge base.
3. Query the vector store for the top-N nearest chunks (N=5 worked well
   in testing).
4. **Apply a relevance threshold before injecting anything.** This is the
   step that's easy to skip and causes real damage if skipped — retrieval
   without a threshold means every single question, including ones that
   have nothing to do with the imported knowledge, pays a retrieval-latency
   cost and gets irrelevant context stuffed into the prompt. In testing,
   a cosine-distance cutoff below 1.0 correctly separated on-topic queries
   (which got 5 injected chunks) from off-topic ones (which got 0).
5. If chunks clear the threshold, inject them as system/context content
   before the user's actual message. If not, send the prompt through
   unmodified.

## Make it toggleable

Expose the behavior via environment variables so it can be tuned or
disabled without a code change or redeploy:

```bash
# Disable RAG retrieval entirely
launchctl setenv HULK_RAG_ENABLED 0

# Tighten the threshold (fewer, more confident matches)
launchctl setenv HULK_RAG_DISTANCE_THRESHOLD 0.8

# Loosen the threshold (more recall, more risk of noise)
launchctl setenv HULK_RAG_DISTANCE_THRESHOLD 1.2

# Apply changes
launchctl kickstart -k gui/501/com.hulk.proxy
```

(Substitute your actual service name/UID for the launchctl target, or the
equivalent restart command for your service manager if not using launchd.)

## Dependency gotcha

The embedding step usually needs `sqlite-vec` / `sentence-transformers` or
similar — packages the *existing* proxy/service's Python environment may
not have. Rather than polluting that environment, it's cleaner to give the
RAG bridge its own virtual environment and have the proxy launch through a
small wrapper script that activates it. This avoids version conflicts
between whatever the proxy already depends on and the embedding stack.

## Verification

Always test both directions before calling this done:

- **On-topic question** — should retrieve chunks and the response should
  visibly reference specific content only present in the imported files
  (not something the model could plausibly know generically).
- **Off-topic question** (something you're certain isn't in the knowledge
  base — weather, an unrelated fact) — should retrieve zero chunks and
  respond with no trace of injected content. If it "hallucinates" a
  connection to the imported material anyway, the threshold is too loose
  or something's forcing injection regardless of relevance.
- **Latency sanity check** — off-topic questions should be noticeably
  faster than on-topic ones once the threshold is working correctly,
  since they skip the injection step entirely.
