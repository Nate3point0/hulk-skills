#!/usr/bin/env bash
# ============================================================
# Mac Health, Security & Dependency Audit Script
# For Apple Silicon Macs (M1/M2/M3/M4) — macOS 13+
# Usage: bash audit.sh
# ============================================================

# ── Colors ──────────────────────────────────────────────────
RED='\033[0;31m'; YELLOW='\033[1;33m'; GREEN='\033[0;32m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'
OK="✅"; WARN="⚠️ "; CRIT="🔴"; INFO="ℹ️ "

sep() { echo -e "${CYAN}────────────────────────────────────────${RESET}"; }

echo ""
echo -e "${BOLD}🖥️  Mac Health, Security & Dependency Audit${RESET}"
echo -e "   $(date '+%Y-%m-%d %H:%M:%S')"
sep

# ── 1. HARDWARE ──────────────────────────────────────────────
echo -e "\n${BOLD}⚙️  SYSTEM OVERVIEW${RESET}"
MODEL=$(system_profiler SPHardwareDataType 2>/dev/null | grep "Model Name" | awk -F': ' '{print $2}' | xargs)
CHIP=$(system_profiler SPHardwareDataType 2>/dev/null | grep "Chip" | awk -F': ' '{print $2}' | xargs)
RAM=$(system_profiler SPHardwareDataType 2>/dev/null | grep "Memory:" | awk -F': ' '{print $2}' | xargs)
MACOS=$(sw_vers -productVersion 2>/dev/null)
echo "  Model : ${MODEL:-Unknown}"
echo "  Chip  : ${CHIP:-Unknown}"
echo "  RAM   : ${RAM:-Unknown}"
echo "  macOS : ${MACOS:-Unknown}"

# ── 2. CPU LOAD ──────────────────────────────────────────────
echo -e "\n${BOLD}📊 CPU & MEMORY${RESET}"
LOAD=$(sysctl -n vm.loadavg 2>/dev/null | awk '{print $2}')
LOAD_INT=$(echo "$LOAD" | cut -d. -f1)
if   [ "$LOAD_INT" -lt 4 ] 2>/dev/null; then LOAD_ICON="$OK"
elif [ "$LOAD_INT" -lt 8 ] 2>/dev/null; then LOAD_ICON="$WARN"
else LOAD_ICON="$CRIT"; fi
echo "  CPU load (1m avg): $LOAD  $LOAD_ICON"

# Memory: free % from memory_pressure (macOS outputs "System-wide memory free percentage: X%.")
MEM_FREE_RAW=$(memory_pressure 2>/dev/null | grep -i "free percentage" | grep -oE '[0-9]+' | tail -1)
if [ -n "$MEM_FREE_RAW" ]; then
  if   [ "$MEM_FREE_RAW" -ge 40 ] 2>/dev/null; then MP_ICON="$OK"
  elif [ "$MEM_FREE_RAW" -ge 20 ] 2>/dev/null; then MP_ICON="$WARN"
  else MP_ICON="$CRIT"; fi
  echo "  Memory free: ${MEM_FREE_RAW}%  $MP_ICON  (>40% = healthy on macOS)"
else
  # Fallback: estimate from vm_stat
  PAGESIZE=$(pagesize 2>/dev/null || echo 16384)
  VMSTAT=$(vm_stat 2>/dev/null)
  PAGES_FREE=$(echo "$VMSTAT" | grep "Pages free"        | awk '{print $3}' | tr -d '.')
  PAGES_SPEC=$(echo "$VMSTAT" | grep "Pages speculative" | awk '{print $3}' | tr -d '.')
  if [ -n "$PAGES_FREE" ] && [ -n "$PAGES_SPEC" ]; then
    FREE_MB=$(( (PAGES_FREE + PAGES_SPEC) * PAGESIZE / 1048576 ))
    echo "  Approx. free memory: ~${FREE_MB} MB"
  fi
fi

# ── 3. DISK ──────────────────────────────────────────────────
echo -e "\n${BOLD}💾 DISK USAGE${RESET}"
# On APFS, only /System/Volumes/Data and / show real usage.
# Use diskutil to get the most accurate container usage.
DISK_INFO=$(df -g 2>/dev/null | grep -E "^/dev" | grep -v "devfs|map")
# Show only meaningful volumes (skip virtual APFS snapshots at 0 used)
echo "$DISK_INFO" | awk '
{
  size=$2; used=$3; avail=$4; mount=$NF
  if (size == 0) next
  pct = int(used * 100 / size)
  icon = (pct < 75) ? "✅" : (pct < 90) ? "⚠️" : "🔴"
  printf "  %-40s  %dG used / %dG total  (%d%%)  %s\n", mount, used, size, pct, icon
}' | sort -u

# ── 4. BATTERY ────────────────────────────────────────────────
BATT=$(pmset -g batt 2>/dev/null)
if echo "$BATT" | grep -q "%"; then
  echo -e "\n${BOLD}🔋 BATTERY${RESET}"
  PCT=$(echo "$BATT" | grep -oE '[0-9]+%' | head -1)
  STATE=$(echo "$BATT" | grep -oE '(charging|discharging|charged|AC attached|Battery Power|AC Power)' | head -1)
  PCT_NUM=$(echo "$PCT" | tr -d '%')
  # Thresholds are for current CHARGE level (not health)
  if   [ "$PCT_NUM" -ge 30 ] 2>/dev/null; then BATT_ICON="$OK"
  elif [ "$PCT_NUM" -ge 15 ] 2>/dev/null; then BATT_ICON="$WARN"
  else BATT_ICON="$CRIT"; fi
  # Cycle count
  CYCLES=$(system_profiler SPPowerDataType 2>/dev/null | grep "Cycle Count" | awk '{print $3}')
  echo "  Charge: $PCT  $BATT_ICON  |  State: $STATE  |  Cycles: ${CYCLES:-N/A}"
fi

# ── 5. TOP PROCESSES ─────────────────────────────────────────
echo -e "\n${BOLD}🔝 TOP PROCESSES (CPU)${RESET}"
ps -Arco pid,pcpu,pmem,comm 2>/dev/null | head -6 | tail -5 | \
  awk '{printf "  PID %-6s  CPU %-6s  MEM %-6s  %s\n", $1, $2"%", $3"%", $4}'

echo -e "\n${BOLD}🔝 TOP PROCESSES (RAM)${RESET}"
ps -Amco pid,pcpu,pmem,comm 2>/dev/null | head -6 | tail -5 | \
  awk '{printf "  PID %-6s  CPU %-6s  MEM %-6s  %s\n", $1, $2"%", $3"%", $4}'

sep
# ── 6. SECURITY ──────────────────────────────────────────────
echo -e "\n${BOLD}🔒 SECURITY CHECKS${RESET}"

# Firewall
FW=$(/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null)
if echo "$FW" | grep -qi "enabled"; then
  echo "  Firewall    : $OK  Enabled"
else
  echo "  Firewall    : $CRIT DISABLED — enable in System Settings → Network → Firewall"
fi

# FileVault
FV=$(fdesetup status 2>/dev/null)
if echo "$FV" | grep -qi "FileVault is On"; then
  echo "  FileVault   : $OK  Enabled (disk encrypted)"
else
  echo "  FileVault   : $CRIT OFF — enable in System Settings → Privacy & Security → FileVault"
fi

# Gatekeeper
GK=$(spctl --status 2>/dev/null)
if echo "$GK" | grep -qi "enabled"; then
  echo "  Gatekeeper  : $OK  Enabled"
else
  echo "  Gatekeeper  : $WARN Disabled — consider re-enabling for security"
fi

# SIP
SIP=$(csrutil status 2>/dev/null)
if echo "$SIP" | grep -qi "enabled"; then
  echo "  SIP         : $OK  Enabled"
elif echo "$SIP" | grep -qi "disabled"; then
  echo "  SIP         : $WARN Disabled — only disable if you have a specific need"
else
  echo "  SIP         : $INFO Run 'csrutil status' in Terminal to verify"
fi

# macOS Updates
echo -e "\n  Checking macOS updates (may take a moment)..."
SWUPDATE=$(softwareupdate -l 2>&1)
if echo "$SWUPDATE" | grep -qi "no new software available"; then
  echo "  macOS Updates: $OK  Up to date"
elif echo "$SWUPDATE" | grep -qi "recommended\|security"; then
  echo "  macOS Updates: $CRIT Security updates available:"
  echo "$SWUPDATE" | grep -E "^\*|Label:|Title:" | sed 's/^/    /'
else
  PENDING=$(echo "$SWUPDATE" | grep -c "^\*")
  [ "$PENDING" -gt 0 ] && echo "  macOS Updates: $WARN  $PENDING update(s) available" || echo "  macOS Updates: $OK  Up to date"
fi

# Open Ports
echo -e "\n${BOLD}🌐 LISTENING PORTS${RESET}"
PORTS=$(lsof -i -P -n 2>/dev/null | grep LISTEN | awk '{print $1, $9}' | sort -u)
KNOWN_SAFE="rapportd|Spotify|Figma|zoom|Slack|sharingd|UserEventAgent|GitHub|node|Python|ruby|php|ControlCe|airportd|mDNSRespo"
SUSPICIOUS_PORTS="445|3389|5900|23\b|21\b|139\b"
if [ -z "$PORTS" ]; then
  echo "  No listening ports found (or permission needed)"
else
  echo "$PORTS" | while IFS= read -r line; do
    PROC=$(echo "$line" | awk '{print $1}')
    ADDR=$(echo "$line" | awk '{print $2}')
    PORT_NUM=$(echo "$ADDR" | rev | cut -d: -f1 | rev)
    if echo "$PORT_NUM" | grep -qE "$SUSPICIOUS_PORTS"; then
      echo "  $CRIT  $ADDR  ← $PROC  (review this)"
    else
      echo "  $OK  $ADDR  ← $PROC"
    fi
  done
fi

sep
# ── 7. DEPENDENCY UPDATES ────────────────────────────────────
echo -e "\n${BOLD}📦 DEPENDENCY UPDATES${RESET}"

# Homebrew
echo -e "\n  ${BOLD}🍺 Homebrew${RESET}"
if command -v brew &>/dev/null; then
  BREW_OUT=$(brew outdated --verbose 2>/dev/null)
  BREW_CASK=$(brew outdated --cask 2>/dev/null)
  BREW_COUNT=$(echo "$BREW_OUT" | grep -c . 2>/dev/null || echo 0)
  CASK_COUNT=$(echo "$BREW_CASK" | grep -c . 2>/dev/null || echo 0)
  if [ "$BREW_COUNT" -eq 0 ] && [ "$CASK_COUNT" -eq 0 ]; then
    echo "  $OK  All Homebrew packages up to date"
  else
    [ "$BREW_COUNT" -gt 0 ] && echo "  $WARN  $BREW_COUNT formula(e) outdated:" && echo "$BREW_OUT" | sed 's/^/    /'
    [ "$CASK_COUNT" -gt 0 ] && echo "  $WARN  $CASK_COUNT cask(s) outdated (casks):" && echo "$BREW_CASK" | sed 's/^/    /'
    echo ""
    echo "  🟢 Safe:  brew upgrade           (formulas — generally safe)"
    [ "$CASK_COUNT" -gt 0 ] && echo "  🟡 Review: upgrade casks one-by-one — major app versions may need config migration"
    [ "$CASK_COUNT" -gt 0 ] && echo "            brew upgrade --cask $(echo "$BREW_CASK" | tr '\n' ' ')"
  fi
else
  echo "  $INFO  brew not installed"
fi

# npm
echo -e "\n  ${BOLD}📦 npm globals${RESET}"
if command -v npm &>/dev/null; then
  NPM_OUT=$(npm outdated -g --depth=0 2>/dev/null)
  if [ -z "$NPM_OUT" ]; then
    echo "  $OK  All npm global packages up to date"
  else
    NPM_COUNT=$(echo "$NPM_OUT" | tail -n +2 | grep -c .)
    echo "  $WARN  $NPM_COUNT package(s) outdated:"
    echo "$NPM_OUT" | sed 's/^/    /'
    echo "  → Run: npm update -g"
  fi
else
  echo "  $INFO  npm not installed"
fi

# pip — pre-flight conflict check
echo -e "\n  ${BOLD}🐍 pip — Pre-flight Environment Check${RESET}"
PIP_CHECK=$(pip3 check 2>&1)
if echo "$PIP_CHECK" | grep -qi "No broken"; then
  echo "  $OK  No pre-existing dependency conflicts"
else
  CONFLICT_COUNT=$(echo "$PIP_CHECK" | grep -c "incompatible\|requires" 2>/dev/null || echo "?")
  echo "  $INFO  $CONFLICT_COUNT pre-existing conflict(s) noted (from pip check):"
  echo "$PIP_CHECK" | grep -v "^$" | head -8 | sed 's/^/    /'
  echo "    (These existed before any upgrades — pip warnings are common in global envs)"
fi

# pip — with risk classification
echo -e "\n  ${BOLD}🐍 pip (Python) — Risk-Classified Updates${RESET}"
PIP_CMD=""
command -v pip3 &>/dev/null && PIP_CMD="pip3"
command -v pip  &>/dev/null && [ -z "$PIP_CMD" ] && PIP_CMD="pip"
if [ -n "$PIP_CMD" ]; then
  PIP_OUT=$($PIP_CMD list --outdated --format=columns 2>/dev/null | tail -n +3)
  PIP_COUNT=$(echo "$PIP_OUT" | grep -c . 2>/dev/null || echo 0)
  if [ "$PIP_COUNT" -eq 0 ]; then
    echo "  $OK  All pip packages up to date"
  else
    echo "  $WARN  $PIP_COUNT package(s) outdated — classified by upgrade risk:"
    echo ""

    # ── Risk group definitions (all names normalized to lowercase-hyphenated) ──
    # Packages that must be upgraded as a coordinated group
    PYTORCH_GROUP="torch torchaudio torchvision accelerate"
    HF_GROUP="transformers tokenizers huggingface-hub diffusers safetensors hf-xet"
    LITELLM_GROUP="litellm litellm-enterprise litellm-proxy-extras"
    PYDANTIC_GROUP="pydantic pydantic-core fastapi starlette"
    SPACY_GROUP="thinc spacy curated-tokenizers curated-transformers spacy-curated-transformers"
    MCP_GROUP="mcp"
    # numpy is handled separately as ecosystem anchor

    # Individually-risky packages (minor bumps but API-sensitive)
    REVIEW_SOLO="scipy pillow polars polars-runtime-32 tiktoken regex anyio aiohttp \
      gunicorn uvicorn uvloop boto3 botocore s3transfer azure-identity azure-storage-blob \
      openai anthropic cryptography pyroscope-io gradio gradio-client oslex rfc3986 \
      sympy networkx fsspec filelock importlib-metadata importlib-resources \
      orjson posthog mixpanel gitpython websockets"

    # Containers for output
    SAFE_PKGS=""
    REVIEW_PKGS=""
    HOLD_PYTORCH=""
    HOLD_HF=""
    HOLD_LITELLM=""
    HOLD_PYDANTIC=""
    HOLD_SPACY=""
    HOLD_MCP=""
    HOLD_NUMPY=""
    HOLD_OTHER=""

    # Helper: is this package name in a space-separated list?
    in_group() {
      local pkg="$1"; local grp="$2"
      echo "$grp" | tr ' ' '\n' | grep -qi "^${pkg}$"
    }

    # Helper: detect major version bump
    is_major_bump() {
      local cur="$1" latest="$2"
      local cur_maj latest_maj
      cur_maj=$(echo "$cur"    | cut -d. -f1 | tr -d 'v')
      latest_maj=$(echo "$latest" | cut -d. -f1 | tr -d 'v')
      [ "$cur_maj" != "$latest_maj" ] && [ -n "$cur_maj" ] && [ -n "$latest_maj" ]
    }

    while IFS= read -r line; do
      [ -z "$line" ] && continue
      PKG=$(echo "$line"    | awk '{print $1}')
      CUR=$(echo "$line"    | awk '{print $2}')
      LATEST=$(echo "$line" | awk '{print $3}')
      PKG_LOWER=$(echo "$PKG" | tr '[:upper:]' '[:lower:]' | tr '_' '-')
      ENTRY="  ${PKG} (${CUR} → ${LATEST})"

      if in_group "$PKG_LOWER" "$PYTORCH_GROUP"; then
        HOLD_PYTORCH="$HOLD_PYTORCH\n$ENTRY"
      elif [ "$PKG_LOWER" = "numpy" ]; then
        HOLD_NUMPY="$HOLD_NUMPY\n$ENTRY"
      elif in_group "$PKG_LOWER" "$HF_GROUP"; then
        HOLD_HF="$HOLD_HF\n$ENTRY"
      elif in_group "$PKG_LOWER" "$LITELLM_GROUP"; then
        HOLD_LITELLM="$HOLD_LITELLM\n$ENTRY"
      elif in_group "$PKG_LOWER" "$PYDANTIC_GROUP"; then
        HOLD_PYDANTIC="$HOLD_PYDANTIC\n$ENTRY"
      elif in_group "$PKG_LOWER" "$SPACY_GROUP"; then
        HOLD_SPACY="$HOLD_SPACY\n$ENTRY"
      elif in_group "$PKG_LOWER" "$MCP_GROUP"; then
        HOLD_MCP="$HOLD_MCP\n$ENTRY"
      elif is_major_bump "$CUR" "$LATEST"; then
        HOLD_OTHER="$HOLD_OTHER\n$ENTRY  ⚡ major version jump"
      elif in_group "$PKG_LOWER" "$REVIEW_SOLO"; then
        REVIEW_PKGS="$REVIEW_PKGS $PKG"
      else
        SAFE_PKGS="$SAFE_PKGS $PKG"
      fi
    done <<< "$PIP_OUT"

    # ── Print SAFE ───────────────────────────────────────────────
    SAFE_COUNT=$(echo $SAFE_PKGS | wc -w | tr -d ' ')
    echo "  ${GREEN}🟢 SAFE (${SAFE_COUNT}) — patch/minor bumps, no ecosystem ties${RESET}"
    if [ -n "$SAFE_PKGS" ]; then
      echo "$SAFE_PKGS" | tr ' ' '\n' | grep -v '^$' | awk '{printf "    %s\n", $0}'
      echo ""
      echo -e "  ${GREEN}→ Run now:${RESET}"
      echo "    pip3 install -U $(echo $SAFE_PKGS | xargs)"
    fi
    echo ""

    # ── Print REVIEW ─────────────────────────────────────────────
    REVIEW_COUNT=$(echo $REVIEW_PKGS | wc -w | tr -d ' ')
    echo "  ${YELLOW}🟡 REVIEW (${REVIEW_COUNT}) — check changelogs before upgrading${RESET}"
    if [ -n "$REVIEW_PKGS" ]; then
      echo "$REVIEW_PKGS" | tr ' ' '\n' | grep -v '^$' | awk '{printf "    %s\n", $0}'
      echo ""
      echo "  → After reviewing: pip3 install -U $(echo $REVIEW_PKGS | xargs)"
    fi
    echo ""

    # ── Print HOLD groups ────────────────────────────────────────
    echo "  ${RED}🔴 HOLD — coordinate these upgrades carefully${RESET}"
    echo ""

    if [ -n "$HOLD_NUMPY" ]; then
      echo "  ⚓ numpy (ecosystem anchor — upgrade LAST, after all ML packages confirm numpy 2.x support)"
      echo -e "$HOLD_NUMPY"
      echo "     https://numpy.org/doc/stable/release/2.0.0-notes.html"
      echo ""
    fi
    if [ -n "$HOLD_PYTORCH" ]; then
      echo "  🔥 PyTorch ecosystem (upgrade torch + torchaudio + torchvision together)"
      echo -e "$HOLD_PYTORCH"
      echo "     https://pytorch.org/get-started/locally/ — pick compatible versions"
      echo ""
    fi
    if [ -n "$HOLD_HF" ]; then
      echo "  🤗 HuggingFace stack (check transformers migration guide for breaking changes)"
      echo -e "$HOLD_HF"
      echo "     https://github.com/huggingface/transformers/releases"
      echo ""
    fi
    if [ -n "$HOLD_PYDANTIC" ]; then
      echo "  🔧 Pydantic / FastAPI / Starlette (upgrade as a group, check starlette 1.x migration)"
      echo -e "$HOLD_PYDANTIC"
      echo "     https://www.starlette.io/release-notes/"
      echo ""
    fi
    if [ -n "$HOLD_LITELLM" ]; then
      echo "  🔁 LiteLLM stack (keep litellm + enterprise + proxy-extras in sync)"
      echo -e "$HOLD_LITELLM"
      echo "     https://github.com/BerriAI/litellm/releases"
      echo ""
    fi
    if [ -n "$HOLD_SPACY" ]; then
      echo "  🌿 spaCy / curated stack (thinc + curated-tokenizers + curated-transformers must match)"
      echo -e "$HOLD_SPACY"
      echo ""
    fi
    if [ -n "$HOLD_MCP" ]; then
      echo "  🔌 MCP SDK (review protocol changes before upgrading)"
      echo -e "$HOLD_MCP"
      echo "     https://github.com/modelcontextprotocol/python-sdk/releases"
      echo ""
    fi
    if [ -n "$HOLD_OTHER" ]; then
      echo "  ⚡ Other major-version jumps (review manually):"
      echo -e "$HOLD_OTHER"
      echo ""
    fi
  fi
else
  echo "  $INFO  pip not installed"
fi

sep
echo -e "\n${BOLD}${GREEN}✅  Audit complete.${RESET}\n"
