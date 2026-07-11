---
name: hulk-process-sentinel
description: >
  Diagnoses and kills runaway Python/ML processes eating CPU or GPU on Mac. Activate whenever
  the user says "my Mac is slow", "runaway process", "Python eating CPU", "kill the process",
  "machine is sluggish", "Activity Monitor shows high CPU", "ComfyUI hung", "Python zombie",
  "GPU is pegged", "kernel_task is high", "machine feels hot", "fan is running loud",
  "ML job won't stop", "kill it", "terminate the script", or pastes Activity Monitor output
  showing high CPU/GPU usage. Also fire when the user shares a screenshot of Activity Monitor
  or a ps/top output showing suspicious Python processes. kernel_task at high CPU is always
  a symptom — find the actual Python/ML hog causing it.
---

# hulk-process-sentinel

Identify and kill runaway Python/ML processes on Mac. Fast triage → identify → kill → verify.

## Step 1 — Battlefield Intel (30 seconds)

Run this to get a complete picture:

```bash
# Top CPU hogs right now
ps aux --sort=-%cpu | head -20

# GPU usage (MPS processes)
sudo powermetrics --samplers gpu_power -n 1 2>/dev/null | grep -E "GPU|Active|Idle" | head -5

# Any zombie/hung Python processes
ps aux | grep -E "python|ComfyUI|torch" | grep -v grep
```

Paste the output and identify:
- Which PID has >100% CPU?
- How long has it been running? (`TIME` column — `182:34` = 182 hours = zombie)
- What's the command? (`COMMAND` column)

---

## Step 2 — Identify the Script

Once you have a PID (e.g., `80813`), get the full command:

```bash
# Full command line
ps -p 80813 -o pid,ppid,etime,command

# What files it has open (shows which script/model is loading)
lsof -p 80813 | grep -E "\.py|\.safetensors|\.gguf|\.pt" | head -10

# Is it a child of ComfyUI?
ps -p 80813 -o ppid= | xargs ps -p
```

### Common culprits in this setup

| Process | Likely cause | Safe to kill? |
|---------|-------------|---------------|
| `python3.10` high CPU, old runtime | ComfyUI sampling job that hung | ✅ Yes |
| `Python` with GPU usage | Active ComfyUI job (may still be running!) | ⚠️ Check first |
| `python3` with no GPU | Batch script, audio processing | ✅ Usually yes |
| `ComfyUI/main.py` | ComfyUI server itself | ✅ Yes, restart after |
| Demucs / Basic Pitch | Audio stem separation | ✅ Yes if stuck |

---

## Step 3 — Kill It

### Graceful kill first (gives Python time to clean up)
```bash
kill 80813
sleep 3
# Check if it's dead:
ps -p 80813 > /dev/null && echo "Still alive" || echo "Dead ✅"
```

### Force kill if still alive
```bash
kill -9 80813
```

### Kill ALL Python processes (nuclear option — use when ComfyUI is totally hung)
```bash
# Preview what you're about to kill
ps aux | grep -E "python|ComfyUI" | grep -v grep

# Then kill them all
pkill -f "python" && pkill -f "ComfyUI"
```

### Kill by script name (safer than killing all Python)
```bash
# Example: kill any hung ComfyUI job
pkill -f "ComfyUI/main.py"

# Kill a specific audio processing script
pkill -f "demucs"
pkill -f "basic_pitch"
```

---

## Step 4 — Verify Machine Recovery

After killing:

```bash
# CPU should drop back to <20% total within 30 seconds
top -l 2 -n 0 | grep "CPU usage"

# GPU should idle out
sudo powermetrics --samplers gpu_power -n 1 2>/dev/null | grep "GPU Active"

# Check kernel_task dropped (it will within ~60s of the hog dying)
ps aux | grep kernel_task | awk '{print $3}'
```

Machine should snap back responsive within 30–60 seconds of killing the hog.

---

## Step 5 — Restart What You Need

If you killed ComfyUI intentionally:
```bash
bash ~/hulk-scripts/comfyui-start.sh
sleep 20
curl -s http://127.0.0.1:8188/system_stats | python3 -c "import sys,json; print('✅ ComfyUI back online')"
```

If a TI2V job died mid-run, verify patches before restarting:
```bash
python ~/hulk-scripts/wan_mps_patcher.py --check
```

---

## Prevention

### Set up a watchdog alias (add to ~/.zshrc)
```bash
# Quick health check
alias hulk-health='ps aux --sort=-%cpu | head -10 && echo "---" && ps aux | grep -E "python|ComfyUI" | grep -v grep'

# Kill all Python except ComfyUI
alias kill-python='pkill -f "python3" && echo "Killed all python3 processes"'

# Kill ComfyUI cleanly
alias kill-comfy='kill $(pgrep -f "ComfyUI/main.py") && echo "ComfyUI stopped"'
```

Add them:
```bash
echo '
alias hulk-health="ps aux --sort=-%cpu | head -10"
alias kill-python="pkill -f python3"
alias kill-comfy="kill \$(pgrep -f ComfyUI/main.py)"' >> ~/.zshrc
source ~/.zshrc
```

### Understanding kernel_task

`kernel_task` at high CPU is **never the root cause** — it's macOS thermal management throttling the CPU to prevent overheating. The actual enemy is always the process burning the most CPU. Kill that, and `kernel_task` drops within ~60 seconds.

High `kernel_task` = Mac is hot/throttled. Find the real hog.

---

## Quick Reference — One-Liners

```bash
# Who's eating my CPU?
ps aux --sort=-%cpu | head -5

# What is PID 80813 actually doing?
ps -p 80813 -o command=

# Kill it gracefully
kill 80813

# Force kill
kill -9 80813

# Kill all hung Python (nuclear)
pkill -9 -f python3

# Machine status after kill
top -l 1 -n 0 | grep "CPU usage"
```
