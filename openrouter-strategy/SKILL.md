---
name: openrouter-strategy
description: Use this skill for anything involving OpenRouter model selection, cost optimization, conversation threading, API routing, or model tier decisions on the Hulk stack. Triggers on: OpenRouter, model selection, cost per token, free models, Haiku, Sonnet, auto routing, X-Conversation-ID, API keys, model switching, token cost.
---

# OpenRouter Strategy & Model Routing

## Core Principle
**Default to free. Pay only when capability requires it.**

## Model Tier System

### Tier 1 — Free (Default)
Use for: all routine queries, brainstorming, simple tasks, testing, agent background work

| Model | Best For |
|-------|---------|
| `meta-llama/llama-3.1-8b-instruct:free` | Fast responses, simple tasks |
| `meta-llama/llama-3.1-70b-instruct:free` | More capable free option |
| `mistralai/mistral-7b-instruct:free` | Lightweight fallback |
| `google/gemma-2-9b-it:free` | Alternative free model |

### Tier 2 — Claude Haiku (Paid, Low Cost)
Use for: code generation, structured output, tool use, anything needing reliability
- Model string: `anthropic/claude-haiku-4-5`
- When: free models fail, code tasks, JSON output, function calling

### Tier 3 — Claude Sonnet (Paid, Higher Cost)
Use for: complex reasoning, architecture decisions, long-form analysis, critical outputs
- Model string: `anthropic/claude-sonnet-4-5`
- When: genuinely complex reasoning required, important decisions, multi-step logic

### Tier 4 — Local (Ollama/phi3.5)
Use for: offline work, privacy-sensitive data, experimentation, no-cost local inference
- Base URL: `http://localhost:11434`
- Model: `phi3.5`
- Note: 48-60s cold start, 90s timeout required

## Auto Routing
When you set `model: "auto"` in the proxy, it applies this logic:
1. Try free Llama first
2. Fall back to Haiku if free model fails or task is code-related
3. Escalate to Sonnet only for flagged complex tasks

## API Configuration

### OpenRouter base URL
```
https://openrouter.ai/api/v1
```

### Request format through Hulk proxy
```bash
curl -X POST http://100.106.11.18:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-Conversation-ID: your-thread-id" \
  -d '{
    "model": "auto",
    "messages": [{"role": "user", "content": "your message"}]
  }'
```

### Conversation Threading
Use `X-Conversation-ID` header to maintain thread context across requests:
```
X-Conversation-ID: hulk-session-20240115-project-brainvault
```

Naming convention: `hulk-[date]-[project-name]`

### Source Tagging
Tag requests by source for log filtering:
```json
{
  "metadata": {
    "source": "iphone_shortcut | vaultmind | claude_code | kimi_agent"
  }
}
```

## Claude Code Environment Variables
Claude Code uses OpenRouter via environment variable overrides:

```bash
# In ~/.zshrc or set before running claude
export ANTHROPIC_BASE_URL=https://openrouter.ai/api/v1
export ANTHROPIC_API_KEY=your-openrouter-key
```

## Cost Tracking
The proxy `/stats` endpoint returns:
- Total tokens used per session
- Estimated cost breakdown by model tier
- Request count by source

```bash
curl http://localhost:4000/stats
```

## Kimi AI Swarm Agent Routing
7 specialized agents routed through the proxy:
- Assign agents to Tier 1 (free) for routine tasks
- Escalate specific agents to Haiku for code/structured output
- Only use Sonnet for the orchestrator agent on complex multi-agent tasks

## Cost Decision Framework
```
Is this task experimental or exploratory?  → Free Tier
Is this task code generation or tool use?  → Haiku
Is this task complex reasoning/analysis?   → Sonnet
Is this task privacy-sensitive?            → Local (Ollama)
Is this task background/automated?         → Free Tier
```

## OpenRouter Dashboard
Monitor usage, costs, and model performance at:
`https://openrouter.ai/activity`
