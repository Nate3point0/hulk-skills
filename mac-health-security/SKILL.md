---
name: mac-health-security
description: >
  Full-system health, security, and dependency-update audit for Apple Silicon Macs (M1/M2/M3/M4).
  Activate this skill whenever the user asks to: "check my Mac's health", "run a security audit",
  "check for updates", "what's outdated on my Mac", "audit my dependencies", "is my Mac secure",
  "check my firewall", "check my M4", "system check", "health check", "security scan", "safe
  update", "update without breaking", or any variation of wanting to know the state of their macOS
  system. Also trigger when the user mentions wanting to check Homebrew, npm globals, or pip
  packages for updates alongside any system context. Produces a rich, color-coded markdown report
  directly in chat with SAFE vs RISKY update classifications — no files needed.
---

# Mac Health, Security & Dependency Audit (with Safe-Update Intelligence)

You are conducting a full system audit on an Apple Silicon Mac (likely M4). Your goal is to
produce a clear, actionable report — and critically, to **never suggest commands that could
silently break a complex, interconnected environment**. The user may have a sophisticated ML/AI
setup (torch, transformers, numpy, fastapi, litellm, etc.) where a blind `pip install -U` would
cascade into breakage. Treat updates as potentially dangerous until proven safe.

## Step 1 — Run the bundled audit script

The fastest, most reliable way to gather all data is to run the bundled script:

```bash
bash <skill_dir>/scripts/audit.sh
```

If the skill directory path isn't directly available, fall back to running the individual command
blocks in the sections below using `mcp__Desktop_Commander__start_process` or
`mcp__Control_your_Mac__osascript`.

## Step 2 — Pre-flight: detect exact-pin landmines

Before classifying anything as "safe", run this to find packages that other installed tools
have pinned to an exact version (`==`). Upgrading those will always trigger pip warnings —
and occasionally real breakage if the pinning app checks version at runtime.

```bash
# Find which installed packages use exact-version pins (==) on their dependencies
pip3 show $(pip3 list --format=names 2>/dev/null) 2>/dev/null \
  | grep -A 999 "^Requires:" \
  | grep "==" \
  | sort -u 2>/dev/null | head -40
```

Or faster — just run `pip3 check` to see pre-existing conflicts before touching anything:

```bash
pip3 check 2>&1 | head -30
```

**Key insight from real usage:** tools like `aider-chat` pin their dependencies to exact versions
for reproducibility. When you upgrade those deps, pip will warn about the conflict — but the
tools usually still work fine because the code is compatible with minor version differences.
Always verify by importing the affected packages after an upgrade:

```bash
python3 -c "import aider, gradio, sympy, omegaconf; print('all OK')" 2>&1
```

If any import fails, immediately roll back that specific package:
```bash
pip3 install "package-name==previous.version"
```

## Step 3 — Gather dependency data for risk analysis

After the pre-flight, collect the raw pip outdated list (needed for risk scoring):

```bash
pip3 list --outdated --format=json 2>/dev/null
```

This gives you `name`, `version` (current), and `latest_version` for every package — use it to
drive the risk classification logic below.

## Step 3 — Classify every update by risk

**This is the most important part of the skill.** Before showing upgrade commands, sort every
outdated package into one of three buckets:

### 🟢 SAFE — patch/minor bumps, isolated packages
A package is SAFE if:
- It's a **patch bump** (e.g., `2.1.3 → 2.1.5`)
- It's a **minor bump** with no known breaking history (e.g., `certifi`, `urllib3`, `idna`,
  `charset-normalizer`, `smmap`, `python-dotenv`, `wcwidth`, `wrapt`, `soupsieve`)
- It has **no known interdependencies** with ML/AI stacks

### 🟡 REVIEW — minor bumps or packages with ecosystem neighbors
A package needs REVIEW if:
- It's a minor bump on anything in the extended web/API stack:
  `fastapi`, `starlette`, `uvicorn`, `pydantic`, `pydantic_core`, `httpx`, `anyio`,
  `aiohttp`, `websockets`, `gunicorn`, `uvloop`
- It's a **data/ML utility** with frequent API changes:
  `numpy`, `scipy`, `pillow`, `polars`, `sympy`, `tokenizers`, `safetensors`, `regex`,
  `tiktoken`, `thinc`, `spacy*`
- It's any **cloud SDK** (boto3, azure-*, openai, anthropic)
- It has a **minor version jump of 2+** on anything non-trivial

### 🔴 HOLD — known breaking or tightly coupled ecosystem packages
HOLD any package that is part of a **coupled ecosystem group** — these must be upgraded
together or not at all:

**PyTorch Ecosystem** (must match exactly):
`torch`, `torchaudio`, `torchvision`, `accelerate`
→ Check https://pytorch.org/get-started/locally/ for compatible version sets.
→ Never upgrade individually. Upgrading torch 2.x → 2.12 while torchaudio stays at 2.6 = crash.

**HuggingFace Stack** (should be compatible):
`transformers`, `tokenizers`, `huggingface_hub`, `diffusers`, `safetensors`
→ transformers 4.x → 5.x is a major breaking release. Pin until you've read the migration guide.

**NumPy** (ecosystem anchor):
`numpy`
→ numpy 1.x → 2.x is a **major ABI break** — torch, scipy, pillow, and many others compiled
  against numpy 1.x will segfault or crash at import with numpy 2.x.
→ ONLY upgrade numpy after confirming every dependent package supports numpy 2.x.

**LiteLLM / Proxy Stack**:
`litellm`, `litellm-enterprise`, `litellm-proxy-extras`
→ These three versions must stay in sync. Check the LiteLLM changelog for compatibility.

**Pydantic / FastAPI / Starlette**:
`pydantic`, `pydantic_core`, `fastapi`, `starlette`
→ pydantic v2 → v3 would be breaking. starlette 0.x → 1.x is already flagged breaking.
→ fastapi major bumps depend on starlette. Upgrade these as a group after reading changelogs.

**MCP SDK**:
`mcp`
→ The MCP protocol evolves; minor bumps can change tool-call schemas. Review before upgrading.

**curated-tokenizers / curated-transformers / spacy stack**:
`curated-tokenizers`, `curated-transformers`, `spacy-curated-transformers`, `thinc`
→ These version numbers must stay compatible with each other.

### Additional HOLD triggers
- Any package where `current` major != `latest` major (e.g., `1.x → 2.x`, `0.x → 1.x`)
- Any package that jumped **3+ minor versions** in one step without a changelog review
- `cryptography` — major bumps often drop legacy cipher support; audit what uses it first
- `pyroscope-io` — profiling agents; check for API changes before upgrading

## Step 4 — Generate safe upgrade commands

**Do NOT output a single `pip install -U` command for everything.** Generate three separate,
copy-paste-ready command blocks:

```bash
# ✅ SAFE to run now — isolated patches
pip3 install -U \
  certifi urllib3 idna charset-normalizer \
  requests python-dotenv wcwidth smmap soupsieve \
  [... other safe packages ...]
```

```bash
# 🟡 REVIEW FIRST — read changelogs, then run
# Check each package's release notes before upgrading
pip3 install -U \
  fastapi starlette uvicorn pydantic \
  [... after you've reviewed ...]
```

```bash
# 🔴 HOLD — ecosystem upgrades, coordinate manually
# PyTorch: visit https://pytorch.org/get-started/locally/
# pip3 install torch==X.Y.Z torchaudio==X.Y.Z torchvision==X.Y.Z

# HuggingFace: check https://github.com/huggingface/transformers/releases
# pip3 install transformers==X.Y.Z tokenizers==... huggingface_hub==...

# numpy: only after confirming all dependents support numpy 2.x
# pip3 install numpy==2.x.x
```

For **Homebrew**, the risk is lower but still segment:
- `brew upgrade` is generally safe for formulas (libraries)
- For casks (apps): `brew upgrade --cask <name>` one at a time — major app versions can have
  config changes

For **npm globals**, running `npm update -g` is usually safe since globals are isolated.

## Step 5 — Compose the final report

Write the report as rich markdown in chat. Use this structure:

---

## 🖥️ Mac Health & Security Report
*Generated: [timestamp]* · *[Model] · macOS [version]*

---

### ⚙️ System Health

| Metric | Value | Status |
|--------|-------|--------|
| Chip | Apple M4 Pro | ✅ |
| RAM | 24 GB | ✅ |
| CPU Load (1m) | 2.11 | ✅ |
| Memory Free | 64% | ✅ |
| Disk (/System/Volumes/Data) | 589G / 926G (63%) | ✅ |
| Battery | 78% — Battery Power · 51 cycles | ✅ |

**Top CPU:** WindowServer (39%), Claude (19%), ...
**Top RAM:** VirtualMachine (5%), Google Chrome (3.3%), ...

---

### 🔒 Security

| Check | Status |
|-------|--------|
| Firewall | ✅ Enabled |
| FileVault | ✅ On |
| Gatekeeper | ✅ Enabled |
| SIP | ✅ Enabled |
| macOS Updates | ✅ Up to date |

**Listening ports:** list each as `port ← process`, flag known-risky ports

---

### 📦 Dependency Updates (Risk-Classified)

**🍺 Homebrew** — N outdated
(list with `current → latest`)
Safe command: `brew upgrade` for formulas, `brew upgrade --cask <name>` individually for casks

**📦 npm globals** — N outdated
Safe command: `npm update -g`

**🐍 pip — N total outdated**

| Risk | Count | Packages |
|------|-------|----------|
| 🟢 Safe now | N | certifi, urllib3, ... |
| 🟡 Review first | N | fastapi, pydantic, ... |
| 🔴 Hold / coordinate | N | torch, numpy, transformers, ... |

Then show the three separate command blocks from Step 4.

---

### 🎯 Action Items

Most important first — be direct:
1. **🔴 Security:** [any security issues]
2. **🟢 Quick win:** Run the safe pip upgrades — N packages, no coordination needed
3. **🟡 This week:** Review fastapi/starlette/pydantic changelogs, then upgrade together
4. **🔴 Plan carefully:** PyTorch ecosystem upgrade — coordinate torch/torchaudio/torchvision
5. **🔴 Anchor first:** numpy 1→2 requires confirming all ML packages are compatible

---

## Status thresholds

| Metric | ✅ OK | ⚠️ Watch | 🔴 Action needed |
|--------|-------|----------|-----------------|
| CPU load (1m avg) | < 4.0 | 4–8 | > 8 |
| Disk used | < 75% | 75–90% | > 90% |
| Memory free | > 40% | 20–40% | < 20% |
| Battery charge | > 30% | 15–30% | < 15% |
| Firewall | Enabled | — | Disabled |
| FileVault | On | — | Off |
| SIP | Enabled | — | Disabled |
| Gatekeeper | Enabled | — | Anywhere/off |
| macOS updates | 0 pending | 1–2 pending | Security update pending |

## Tone

Be a trusted sysadmin, not a lawyer. Don't hedge everything — be direct about what's safe vs
what needs care. If everything is healthy, say so: "Your Mac is clean and secure." The Action
Items list is the payoff — make it immediately actionable.
