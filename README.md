# AHD Wellbeing365 — Nudges Automation

Delivers **4 bilingual (English + Arabic) wellbeing nudges per working day** —
one for each wellbeing pillar, under one daily theme — to the pilot group in
Microsoft Teams. AHD working week = **Sunday–Thursday**.

**The daily logic (confirmed with management):**

| Slot (UAE) | Pillar | |
|-----------|--------|---|
| 07:00 | 🤝 Social | one nudge |
| 09:15 | 🏃 Physical | one nudge |
| 11:30 | 💡 Financial | one nudge |
| 13:45 | 🧠 Mental | one nudge |

**Runs entirely in the Microsoft 365 cloud — no PC left on, $0 beyond existing
M365 licences** (standard connectors only, no premium Power Automate).

Daily ritual: **Reveal → Huddle → Act → Share → Recognize → Tease Tomorrow.**
This package automates the **Reveal** (the 4 nudges); the huddle, action and
sharing are led by Wellbeing Champions.

## Start here

- **`IMPLEMENTATION-GUIDE.md`** — end-to-end running order (PowerShell path;
  fastest).
- **`IMPLEMENTATION-GUIDE-GUI.md`** — the same, all in the browser (no
  PowerShell; avoids the "From Excel" WAC error).

## Contents

| Path | What it is |
|------|-----------|
| `data/four-pillars/by-nudge.json` / `.csv` / `.xlsx` | **84 nudges** = 21 working days × 4 pillars (EN + AR + theme + slot + source ref), seeded `Scheduled`. |
| `adaptive-card-pillar.powerautomate.json` | **Paste this into Power Automate** — pillar card with inline `@{…}` expressions (assumes a Compose named `Nudge`). |
| `adaptive-card-pillar.json` | The clean `${…}` template (reference / other renderers). Power Automate does NOT process `${}` — use the `.powerautomate.json` version there. |
| `four-pillars-sharepoint-schema.md` | The `FourPillarNudges` SharePoint List (state store). |
| `provisioning/` | Auto-create the list from the schema (From-Excel, PnP, or site script) + load the rows — no manual columns. |
| `import-flow-guide.md` | All-GUI alternative loader (Power Automate, no PnP). |
| `four-pillars-flow-guide.md` | The 4×/day reveal flow (Sun–Thu, per-pillar, hardened). |
| `IT-handover.md` | Overview, cost, roles, privacy, metrics, maintenance. |
| `branded-sender-copilot-studio.md` | Optional: make the Teams sender show "AHD Thrive365" instead of "Workflows". |
| `scripts/gen_four_pillars.py` | Regenerates the dataset. |
| `data/month-of-connection.json` | Source of the **Social** pillar (the 21 approved connection challenges). |
| `source/…August2026.xlsx` | The original AHD workbook (authoritative source). |
| `nudge-logic-design.md` | The decision record (why 4/day, one per pillar). |
| `archive/` | Superseded approaches, kept for reference only. |

## The logic

- **4 nudges/day, one per pillar**, in Dr. Dania's sequence: **Social → Physical
  → Financial → Mental**, each on its own bilingual Teams card at its time slot.
- **Bilingual by default** — every card shows English and Arabic together (Arabic
  RTL).
- **AHD week (Sun–Thu)** — the four flows fire only on working days and send the
  **next unsent nudge per pillar in `Day` order**, so the schedule doesn't depend
  on calendar dates and the list needs no date edits. A skipped day self-heals.
- **No PC, free** — cloud flows on Microsoft's servers; SharePoint, Teams, Office
  365 Groups, Recurrence are all standard connectors.
- **Traceable** — Social keeps its `SourceRef` back to Dr. Dania's library;
  Physical/Financial/Mental are marked `draft` pending wellbeing-team approval.

## Quick start

1. Create the `FourPillarNudges` list + load the 84 rows — `provisioning/README.md`
   (PnP: `Create-List.ps1` then `Import-Data.ps1`; or From-Excel `.xlsx`).
2. Confirm the pilot M365 Group / Teams team.
3. Build the four per-slot reveal flows — `four-pillars-flow-guide.md`.
4. Test with 2–3 users, then turn all four **On**.

Full step-by-step: `IMPLEMENTATION-GUIDE.md` (or `-GUI.md`).

## Content status

The **Social** pillar = the 21 approved *Month of Connection* challenges. The
**Physical / Financial / Mental** nudges are bilingual **drafts** (`SourceRef =
draft`) for the wellbeing team (Dr. Dania) to review, approve, and map to the
source library. Financial nudges are educational/awareness only (no
individualized advice), per the workbook's governance note. A native-Arabic
reviewer should do a final pass before go-live.

## Regenerating the data

```bash
python3 scripts/gen_four_pillars.py   # rebuilds data/four-pillars/by-nudge.*
python3 scripts/make_xlsx.py          # rebuilds the .xlsx
```

## Scaling to the 12-month journey

The workbook defines a 12-month *Wellbeing365* journey (Connection → Trust →
Calm → Movement → …). Each month reuses the same automation: load the next
month's four-pillar rows and the flows run unchanged.

## Alternatives considered (all cloud, no PC)

| Option | PC needed? | Cost | Verdict |
|--------|-----------|------|---------|
| **Power Automate cloud flow** | No | $0 (in M365) | ✅ Chosen — low-code, free, Champion-friendly |
| Teams Workflows | No | $0 | Same engine, fine too |
| Azure Functions + Graph | No | ~free | More setup; only if IT wants code |
| Power Automate Desktop / Task Scheduler | **Yes** | — | ❌ Rejected — needs a machine on |
