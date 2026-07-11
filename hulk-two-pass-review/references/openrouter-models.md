# OpenRouter Model Pairings

Reference for choosing writer/reviewer models. All slugs are OpenRouter-compatible.

## Recommended Default Pairing

| Role | Model | Slug | Why |
|---|---|---|---|
| Writer | Claude Sonnet 4.5 | `anthropic/claude-sonnet-4-5` | Strong reasoning, long context, reliable code |
| Reviewer | Kimi K2 | `moonshotai/kimi-k2` | Independent, different training data, strong at agentic critique |

## Alternate Pairings

### Budget (lowest cost)
| Role | Model | Slug |
|---|---|---|
| Writer | Claude Haiku 4.5 | `anthropic/claude-haiku-4-5` |
| Reviewer | Mistral Small | `mistralai/mistral-small` |

### Max quality
| Role | Model | Slug |
|---|---|---|
| Writer | Claude Opus 4.5 | `anthropic/claude-opus-4-5` |
| Reviewer | GPT-4o | `openai/gpt-4o` |

### Speed-optimized
| Role | Model | Slug |
|---|---|---|
| Writer | Claude Haiku 4.5 | `anthropic/claude-haiku-4-5` |
| Reviewer | Gemini Flash 2.0 | `google/gemini-flash-2.0` |

### Full independence (no Anthropic in loop)
| Role | Model | Slug |
|---|---|---|
| Writer | Kimi K2 | `moonshotai/kimi-k2` |
| Reviewer | DeepSeek R1 | `deepseek/deepseek-r1` |

## Cost Estimates (approximate, per /review call)

These are rough estimates based on ~500 token prompt + ~800 token output per pass.

| Pairing | Approx Cost |
|---|---|
| Sonnet + Kimi K2 | ~$0.008 |
| Haiku + Mistral Small | ~$0.001 |
| Opus + GPT-4o | ~$0.06 |

## Notes

- All models above support OpenRouter's chat completions API with no changes to the code
- Kimi K2 is available at `moonshotai/kimi-k2` — confirm slug at openrouter.ai/models if you get a 400
- The reviewer benefits from being a model with **different training data** than the writer
  — that's the whole point. Don't use the same model family for both roles.
- For security review specifically, models with RLHF tuned for safety (Claude, GPT-4o) tend to
  surface more conservative/thorough findings. DeepSeek R1 is more aggressive in flagging issues.
