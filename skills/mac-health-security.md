# Mac Health & Security

**Trigger:** When auditing system health, dependencies, security vulnerabilities, or preparing for critical work

**Platforms:** macOS (all versions, Apple Silicon and Intel)

**MCP Required:** No

## What It Does

Full security and dependency audit for Apple Silicon (and Intel) Macs. Checks for outdated packages, vulnerable frameworks, missing system updates, unused services, and disk bloat. Generates a report and suggests fixes. Runs without needing external tools or admin access (mostly).

## How to Use

1. Say: "Run a full Mac security audit"
2. Claude checks: OS version, brew packages, Python environments, security settings, disk usage, running services
3. Claude flags vulnerabilities and generates a cleanup checklist
4. Follow recommendations or have Claude automate fixes

## Notes

- Privilege escalation: some checks need `sudo` (system updates, firewall status) — you'll be prompted
- Brew audit: `brew doctor`, `brew outdated`, `brew cleanup` cover most issues
- Python venvs: check for orphaned virtual environments in ~/.virtualenvs and ~/.venv
- Security: disable unnecessary services (Bluetooth, AirDrop) for better battery life
- Disk bloat: check ~/Library/Caches, ~/Downloads, .git folders (can be 10+ GB each)
- Updates: enable automatic security updates in System Settings → General → Software Update
- Gatekeeper: verify app signing on all mission-critical apps (e.g., crypto, banking)
- Malware: run `malwarebytes` if available (commercial, but worth the investment)
- Backups: Time Machine should run hourly; verify in System Settings → General → Time Machine

---

**Created:** Nate (Ceepeezee), July 2026
**Last updated:** July 2026
**Status:** Production