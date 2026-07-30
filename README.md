# AHD Wellbeing365 — Month of Connection (August 2026 Pilot)

Automates the **daily reveal** of the *Month of Connection* pilot: **one
bilingual (English + Arabic) connection challenge per working day**, delivered
each morning in Microsoft Teams to the pilot group, across **21 working days
(Mon 3 Aug → Mon 31 Aug 2026)**.

**Runs entirely in the Microsoft 365 cloud — no PC left on, $0 beyond existing
M365 licences** (standard connectors only, no premium Power Automate).

Daily ritual: **Reveal → Huddle → Act → Share → Recognize → Tease Tomorrow.**
This package automates the **Reveal**; the huddle, action and sharing are led by
Wellbeing Champions.

## Start here

**→ `IMPLEMENTATION-GUIDE.md`** is the end-to-end, step-by-step running order
(create list → load data → build flow → test → go live → maintain). The files
below are the references it points to.

## Contents

| Path | What it is |
|------|-----------|
| `data/month-of-connection.json` / `.csv` | The 21 bilingual challenges (EN + AR + huddle line + teaser + caption + source ref), seeded to `Scheduled`. |
| `adaptive-card-bilingual.json` | The Teams notification card — English + right-to-left Arabic on one card. |
| `sharepoint-list-schema.md` | The `MonthOfConnection` SharePoint List (state store). |
| `import-flow-guide.md` | Run-once flow that bulk-loads the 21 challenges. |
| `flow-build-guide.md` | The daily reveal flow (date-matched, working-day, bilingual, hardened). |
| `IT-handover.md` | Overview, cost, roles, privacy, metrics, maintenance. |
| `provisioning/` | Auto-create the SharePoint Lists from the schema (From-Excel, PnP PowerShell, or site script) — no manual columns. |
| `scripts/extract_pilot.py` | Regenerates the data from the source workbook. |
| `source/…August2026.xlsx` | The original AHD workbook (authoritative source). |
| `archive/generic-250/` | Superseded English-only 250-nudge draft (reference only). |

## Why this design

- **Bilingual by default** — every card shows English and Arabic together; Arabic
  renders RTL.
- **No computer stays on** — cloud flows run on Microsoft's servers.
- **Free** — SharePoint, Teams, Office 365 Groups, Recurrence are all standard.
- **Calendar-accurate** — challenges are matched to their `RevealDate`, so a
  missed or re-run day never shifts the rest; weekends/holidays simply don't fire.
- **Traceable** — each challenge keeps its `SourceRef` back to Dr. Dania's Social
  Wellbeing library.

## Quick start (before Mon 3 Aug 2026)

1. Auto-create the `MonthOfConnection` SharePoint List (`provisioning/README.md`
   — From-Excel, PnP script, or site script; no manual columns).
2. Bulk-load the 21 challenges (`import-flow-guide.md`, uses the JSON) — or skip
   this if you used the *From Excel* route, which loads rows too.
3. Confirm the pilot M365 Group / Teams team.
4. Build the daily reveal flow (`flow-build-guide.md`).
5. Pilot with 2–3 test users, then go live.

## Regenerating the data

```bash
python3 scripts/extract_pilot.py source/AHD_Wellbing365_Month_of_Connection_August2026.xlsx
```

## Alternatives considered (all cloud, no PC)

| Option | PC needed? | Cost | Verdict |
|--------|-----------|------|---------|
| **Power Automate cloud flow** | No | $0 (in M365) | ✅ Chosen — low-code, free, Champion-friendly |
| Teams Workflows | No | $0 | Same engine, fine too |
| Azure Functions + Graph | No | ~free | More setup; only if IT wants code |
| Power Automate Desktop / Task Scheduler | **Yes** | — | ❌ Rejected — needs a machine on |

## Two delivery models in this repo

Management confirmed the operating logic is **4 nudges/day** (one per pillar,
under one daily theme). Both models are built and documented — see
`nudge-logic-design.md` for the decision context:

| Model | Files | When to use |
|-------|-------|-------------|
| **1 hero challenge/day** (Connection pilot) | `data/month-of-connection.*`, `adaptive-card-bilingual.json`, `flow-build-guide.md`, `sharepoint-list-schema.md` | The tested August pilot; cleanest single measure at the Sep gate. |
| **4 pillars, 4×/day** (Social→Physical→Financial→Mental) | `data/four-pillars/*`, `adaptive-card-pillar.json`, `four-pillars-flow-guide.md`, `four-pillars-sharepoint-schema.md` | The confirmed operating model for full rollout. |

### Four-pillars variant at a glance
- **84 sends** = 21 working days × 4 pillars, all **bilingual (EN + AR)**.
- Times: **07:00 Social · 09:15 Physical · 11:30 Financial · 13:45 Mental** (UAE).
- **Social** = the 21 approved connection challenges (traceable). **Physical /
  Financial / Mental** are drafted in EN + AR (`SourceRef = draft`) pending
  wellbeing-team approval.
- Same free/no-PC footprint; build via four small per-slot flows (or one gated
  flow). A **single-combined-card** option is included too (`by-day.json`).

## Scaling to the 12-month journey

The workbook defines a 12-month *Wellbeing365* journey (Connection → Trust →
Calm → Movement → …). The same automation is reused each month: load the next
month's rows and the flow runs unchanged.
