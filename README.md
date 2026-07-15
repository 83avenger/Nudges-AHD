# Wellbeing Nudges Automation

Send 250 wellbeing nudges to 50 users via Microsoft Teams, 4×/day (07:00, 09:15,
11:30, 13:45 UAE). **Runs in the Microsoft 365 cloud — no PC left on, $0 beyond
existing M365 licences** (standard connectors only, no premium Power Automate).

## Contents

| File | What it is |
|------|-----------|
| `flow-build-guide.md` | Step-by-step Power Automate cloud flow build (hardened). |
| `import-flow-guide.md` | Run-once flow that bulk-loads the 250 nudges into the list. |
| `sharepoint-list-schema.md` | The `Nudges` SharePoint List that stores state. |
| `nudges.csv` | All 250 wellbeing nudges, seeded to `Pending`. |
| `nudges.json` | Same 250 nudges as JSON, for the import flow. |
| `adaptive-card.json` | The Teams notification card. |
| `IT-handover.md` | Overview, cost, and maintenance for IT. |
| `scripts/gen_nudges.py` | Regenerates `nudges.csv`. |

## Why this design

- **No computer needs to stay on** — cloud flows run on Microsoft's servers.
- **Free** — every connector is standard (SharePoint, Teams, Office 365 Groups).
- **Reliable** — SharePoint List (not Excel) for state, deterministic nudge
  ordering, per-run error handling. See `IT-handover.md` for the full list of
  fixes over the original spec.

## Quick start

1. Create the `Nudges` SharePoint List (`sharepoint-list-schema.md`).
2. Bulk-load the 250 nudges with the run-once import flow
   (`import-flow-guide.md`, uses `nudges.json`).
3. Confirm your 50-user M365 Group.
4. Build the scheduled flow (`flow-build-guide.md`).
5. Pilot, then go live.

## Alternatives considered

| Option | PC needed? | Cost | Verdict |
|--------|-----------|------|---------|
| **Power Automate cloud flow** | No | $0 (in M365) | ✅ Chosen — low-code, free |
| Teams Workflows | No | $0 | Same engine, fine too |
| Azure Functions + Graph | No | ~free | More setup; only if IT wants code |
| Power Automate Desktop / Task Scheduler | **Yes** | — | ❌ Rejected — needs a machine on |
