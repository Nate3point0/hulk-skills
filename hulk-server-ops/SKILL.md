---
name: hulk-server-ops
description: Use this skill for anything related to operating, maintaining, debugging, or extending the Hulk Mac Mini server. Triggers on: FastAPI proxy, LaunchAgent, Ollama, port management, Tailscale, proxy.py, hulk services, server startup, background processes, nohup, BrainVault proxy, Kimi agents, server health.
---

# Hulk Server Operations

## Machine Identity
- **Hardware**: Mac Mini 2018 Intel
- **Name**: Hulk
- **Tailscale IP**: 100.106.11.18
- **OS**: macOS (Intel — no Apple Silicon optimizations apply)
- **Shell**: zsh with custom functions in ~/.zshrc

## Port Map
| Port | Service | Notes |
|------|---------|-------|
| 4000 | BrainVault FastAPI proxy (proxy.py) | Primary AI gateway |
| 5005 | VAULTMIND web dashboard | React frontend |
| 11434 | Ollama local inference | phi3.5 model |

## FastAPI Proxy (proxy.py)
- Built for Python 3.14 compatibility — no LiteLLM (callback failures)
- ~120 lines, async I/O
- Routes to OpenRouter by default
- Logs all conversations as structured Markdown to `BrainVault/00-Inbox/`
- Key headers: `X-Conversation-ID` for threading, source tagging
- Auto model routing via `model: "auto"`
- Endpoints: `/v1/chat/completions`, `/health`, `/stats`

### Start proxy
```bash
nohup python3 proxy.py > ~/logs/proxy.log 2>&1 &
```

### Check proxy health
```bash
curl http://localhost:4000/health
```

### Test proxy
```bash
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"auto","messages":[{"role":"user","content":"ping"}]}'
```

## Ollama (Local Inference)
- Intel Mac requires DYLD_LIBRARY_PATH — set via shell function in ~/.zshrc
- Cold start: ~48–60 seconds. Always use 90s timeout + warmup ping
- Model: phi3.5

### Start Ollama
```bash
# Use the zshrc shell function, not raw ollama serve
ollama_start  # calls the function that sets DYLD_LIBRARY_PATH
```

### Warmup ping (run after start, before first real query)
```bash
curl -s http://localhost:11434/api/generate \
  -d '{"model":"phi3.5","prompt":"hi","stream":false}' --max-time 90
```

## LaunchAgents (Persistent Daemons)
Services that should survive reboots live in `~/Library/LaunchAgents/`.

### Load a LaunchAgent
```bash
launchctl load ~/Library/LaunchAgents/com.hulk.proxy.plist
```

### Unload / reload
```bash
launchctl unload ~/Library/LaunchAgents/com.hulk.proxy.plist
launchctl load ~/Library/LaunchAgents/com.hulk.proxy.plist
```

### Check if running
```bash
launchctl list | grep hulk
```

### LaunchAgent plist template
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.hulk.SERVICE_NAME</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>/path/to/script.py</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>/Users/YOUR_USER/logs/SERVICE_NAME.log</string>
  <key>StandardErrorPath</key>
  <string>/Users/YOUR_USER/logs/SERVICE_NAME.err</string>
</dict>
</plist>
```

## Background Process Pattern (nohup)
Reliable pattern for non-daemon background processes:
```bash
nohup python3 script.py > ~/logs/script.log 2>&1 &
echo "PID: $!"
```

Always log the PID so you can kill it later:
```bash
kill $(lsof -ti:4000)  # kill whatever is on a port
```

## Tailscale Network
- Hulk Tailscale IP: 100.106.11.18
- Four devices on the mesh
- Access Hulk from any device: `http://100.106.11.18:4000`

## Kimi AI Swarm
- 7 specialized business agents
- Routed through the FastAPI proxy
- Agent roles: [document as you define them]

## Docker
- Installed: v29.2.0
- Currently unused — available for future containerization

## Log Locations
```
~/logs/proxy.log       # FastAPI proxy
~/logs/proxy.err       # Proxy errors
~/logs/ollama.log      # Ollama output
~/logs/watcher.log     # hulk_watcher.py
```

## Common Troubleshooting

### Port already in use
```bash
lsof -ti:4000 | xargs kill -9
```

### Proxy not responding
1. Check process: `ps aux | grep proxy.py`
2. Check log: `tail -50 ~/logs/proxy.log`
3. Check port: `lsof -i:4000`
4. Restart: `nohup python3 proxy.py > ~/logs/proxy.log 2>&1 &`

### Ollama not responding
1. Check process: `ps aux | grep ollama`
2. Cold start takes 48-60s — wait before declaring failure
3. Verify DYLD_LIBRARY_PATH is set (Intel Mac requirement)
