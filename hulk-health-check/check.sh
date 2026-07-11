#!/bin/zsh
# Hulk health scan — read-only. Emits structured lines:
#   <CATEGORY> <STATUS> key=value [key=value ...]
# STATUS is one of: OK | WARN | FAIL | INFO
# Sections: SERVICES, NETWORK, INBOX, RESOURCES, UPDATES, MAINTENANCE.
#
# Designed to run in well under 30 seconds and produce parseable output for
# the hulk-health-check skill to render into a scoreboard.

setopt no_aliases
TS=$(date '+%F %T %Z')
echo "## hulk health report $TS"

# ============================================================ SERVICES
echo "### SERVICES"
LABELS=(com.hulk.proxy com.hulk.watcher com.hulk.command-center com.hulk.orchestrator com.hulk.operator com.hulk.daily-audit com.hulk.desktop-inbox-sync com.hulk.model-discovery com.hulk.prelaunch-repair)
for L in $LABELS; do
  ROW=$(launchctl list 2>/dev/null | awk -v L="$L" '$3==L {print; exit}')
  if [[ -z "$ROW" ]]; then
    echo "SERVICES FAIL label=$L not_loaded=true"; continue
  fi
  PID=$(echo "$ROW" | awk '{print $1}')
  EC=$(echo "$ROW" | awk '{print $2}')
  if [[ "$PID" == "-" ]]; then
    if [[ "$EC" == "0" ]]; then
      echo "SERVICES INFO label=$L loaded_idle=true"
    else
      echo "SERVICES WARN label=$L last_exit=$EC"
    fi
  else
    echo "SERVICES OK label=$L pid=$PID"
  fi
done

# Proxy /health (localhost — avoids hairpin)
PHC=$(curl -sS http://localhost:4000/health -o /dev/null -w "%{http_code}" --max-time 5 2>/dev/null)
[[ "$PHC" == "200" ]] && echo "SERVICES OK proxy_health=$PHC" || echo "SERVICES FAIL proxy_health=${PHC:-noresp}"

# Ollama
OHC=$(curl -sS http://localhost:11434/api/tags -o /dev/null -w "%{http_code}" --max-time 5 2>/dev/null)
[[ "$OHC" == "200" ]] && echo "SERVICES OK ollama=$OHC" || echo "SERVICES FAIL ollama=${OHC:-noresp}"

# Watcher recent errors
WLOG=$HOME/hulk-system/logs/watcher.stderr.log
if [[ -f "$WLOG" ]]; then
  WERR=$(tail -n 500 "$WLOG" 2>/dev/null | grep -ciE "ERROR|Traceback|relocation failed|FAIL" | tr -d '[:space:]')
  if [[ "${WERR:-0}" -eq 0 ]]; then
    echo "SERVICES OK watcher_recent_errors=0"
  else
    LAST=$(tail -n 500 "$WLOG" | grep -iE "ERROR|Traceback|relocation failed|FAIL" | tail -1 | head -c 180)
    echo "SERVICES WARN watcher_recent_errors=$WERR last=\"$LAST\""
  fi
else
  echo "SERVICES INFO watcher_log_missing=true"
fi

# ============================================================ NETWORK
echo "### NETWORK"
TS_BIN=/usr/local/bin/tailscale
if [[ -x "$TS_BIN" ]]; then
  # Peers (skip header-less; tailscale status is already plain rows)
  $TS_BIN status 2>/dev/null | awk 'NF>=4 {print}' | while read -r LN; do
    IP=$(echo "$LN" | awk '{print $1}')
    HOST=$(echo "$LN" | awk '{print $2}')
    REST=$(echo "$LN" | sed -E 's/^[^ ]+ +[^ ]+ +[^ ]+ +[^ ]+ +//')
    case "$REST" in
      *offline*) echo "NETWORK WARN peer=$HOST ip=$IP state=offline detail=\"$REST\"" ;;
      *active*|*idle*) echo "NETWORK OK peer=$HOST ip=$IP state=connected detail=\"$REST\"" ;;
      "-"|"") echo "NETWORK OK peer=$HOST ip=$IP state=self_or_quiet" ;;
      *) echo "NETWORK INFO peer=$HOST ip=$IP detail=\"$REST\"" ;;
    esac
  done
else
  echo "NETWORK FAIL tailscale_cli_missing=true path=$TS_BIN"
fi

# ============================================================ INBOX
echo "### INBOX"
DRIVE_ROOT="$HOME/Library/CloudStorage/GoogleDrive-motocityfix@gmail.com/My Drive/HulkInbox"
STUCK=0
for SUB in NOTES FILES IMAGES LINKS AUDIO PROMPTS; do
  D="$DRIVE_ROOT/$SUB"
  N=$(ls -1A "$D" 2>/dev/null | grep -v "^\.DS_Store$" | wc -l | tr -d ' ')
  STUCK=$((STUCK + N))
  if [[ "$N" -gt 0 ]]; then
    SAMPLE=$(ls -1A "$D" 2>/dev/null | grep -v "^\.DS_Store$" | head -1)
    echo "INBOX WARN drive_feeder=$SUB stuck=$N sample=\"$SAMPLE\""
  fi
done
[[ "$STUCK" -eq 0 ]] && echo "INBOX OK drive_feeders_clean=true"

# Newest 3 ingestions
if [[ -f "$WLOG" ]]; then
  tail -n 200 "$WLOG" | grep "enqueued task_" | tail -3 | while read -r LN; do
    TIME=$(echo "$LN" | awk '{print $1" "$2}')
    FILE=$(echo "$LN" | awk -F' for ' '{print $2}')
    echo "INBOX INFO last_enqueue_time=\"$TIME\" file=\"$FILE\""
  done
fi

# ============================================================ RESOURCES
echo "### RESOURCES"
df -h /Volumes/HULK-STORAGE / 2>/dev/null | awk 'NR>1 {
  pct=$5; gsub("%","",pct);
  status="OK"; if(pct+0>=90) status="FAIL"; else if(pct+0>=80) status="WARN";
  printf "RESOURCES %s mount=%s used_pct=%s avail=%s\n", status, $9, $5, $4
}'
vm_stat | awk '
  /Pages free/ {f=$3+0}
  /Pages active/ {a=$3+0}
  /Pages wired/ {w=$4+0}
  /Pages occupied by compressor/ {c=$5+0}
  END {
    p=4096; fmb=int(f*p/1048576); cmb=int(c*p/1048576);
    s="OK"; if(fmb<50) s="WARN";
    printf "RESOURCES %s mem_free_mb=%d mem_compressed_mb=%d\n", s, fmb, cmb
  }'
LA=$(uptime | awk -F'load averages?: ' '{print $2}' | tr -s ' ')
LA1=$(echo "$LA" | awk '{print $1}')
LA_STAT="OK"; awk -v v="$LA1" 'BEGIN{ if(v+0>=8) exit 1; }' || LA_STAT="WARN"
echo "RESOURCES $LA_STAT load=\"$LA\""
UP=$(uptime | awk -F'up ' '{print $2}' | awk -F',' '{print $1","$2}')
echo "RESOURCES INFO uptime=\"$UP\""

# ============================================================ UPDATES
echo "### UPDATES"
OUT=$(/usr/local/bin/brew outdated --formula 2>/dev/null)
if [[ -z "$OUT" ]]; then
  echo "UPDATES OK brew_outdated=0"
else
  N=$(echo "$OUT" | grep -c .)
  SAFE_COUNT=0; RISKY_COUNT=0
  while read -r F; do
    [[ -z "$F" ]] && continue
    case "$F" in
      ollama|tailscale|python@*|node@*)
        RISKY_COUNT=$((RISKY_COUNT+1))
        echo "UPDATES WARN risky=$F"
        ;;
      *)
        SAFE_COUNT=$((SAFE_COUNT+1))
        echo "UPDATES INFO safe=$F"
        ;;
    esac
  done <<< "$OUT"
  echo "UPDATES INFO brew_outdated_total=$N safe=$SAFE_COUNT risky=$RISKY_COUNT"
fi

# ============================================================ MAINTENANCE
echo "### MAINTENANCE"
RISKY_PLIST="$HOME/Library/LaunchAgents/com.hulk.maintenance.risky-upgrade.plist"
if [[ -f "$RISKY_PLIST" ]]; then
  echo "MAINTENANCE INFO risky_upgrade_scheduled=yes plist=$RISKY_PLIST"
else
  echo "MAINTENANCE INFO risky_upgrade_scheduled=no"
fi
[[ -f /tmp/hulk.stop ]] && echo "MAINTENANCE WARN kill_switch=/tmp/hulk.stop_present"

# Recent maintenance log if any
ML=$HOME/Library/Logs/hulk-risky-upgrade.log
if [[ -f "$ML" ]]; then
  LAST_RUN=$(grep "maintenance start" "$ML" 2>/dev/null | tail -1 | head -c 80)
  [[ -n "$LAST_RUN" ]] && echo "MAINTENANCE INFO last_run=\"$LAST_RUN\""
fi

echo "## end report"
