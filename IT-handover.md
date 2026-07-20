# IT Handover — AHD Wellbeing365 · Month of Connection (August 2026 Pilot)

## Project overview

Deliver the **Month of Connection** pilot: **one bilingual (English + Arabic)
connection challenge per working day**, revealed each morning in Microsoft Teams
to the pilot group, across **21 working days (Mon 3 Aug → Mon 31 Aug 2026)**.

Daily ritual: **Reveal → Huddle → Act → Share → Recognize → Tease Tomorrow.**
The automation covers the **Reveal** (and optionally the poll/preview/pulse); the
huddle and sharing are human activities led by Wellbeing Champions.

> **No PC or server needs to stay on.** This is a Power Automate **cloud** flow —
> Microsoft runs it on its own servers on schedule. (The "PC must be on" concern
> only applies to Power Automate *Desktop* / RPA, which this is not.)

## Cost

**$0 beyond existing Microsoft 365 licences.** Every connector used (SharePoint,
Teams, Office 365 Groups, Recurrence) is **standard** — **no premium Power
Automate licence** required.

## Bilingual requirement

English and Arabic are both delivered on **one Adaptive Card**: English block,
then a right-to-left Arabic block, then the huddle line and tomorrow's teaser.
All 21 days already have approved Arabic wording (from the workbook).

## Components

| Component | Purpose |
|-----------|---------|
| SharePoint List `MonthOfConnection` | The 21 bilingual challenges + reveal dates + Status/SentDateTime/RunID. |
| Microsoft 365 Group / Teams team | The pilot recipients. |
| Power Automate cloud flow (daily reveal) | Fires 08:00 UAE on working days, matches today's challenge by date, sends the card, updates status. |
| Bilingual Adaptive Card (Teams Flow bot) | EN + AR notification each morning. |
| (Optional) poll / preview / pulse flows | Thursday guess-poll, Sunday Champion preview, Friday pulse — the anticipation + measurement loop. |

## Files in this package

- `data/month-of-connection.json` / `.csv` — the 21 challenges (traceable to the
  source library via `SourceRef`), seeded to `Scheduled`.
- `source/AHD_Wellbing365_Month_of_Connection_August2026.xlsx` — the original
  workbook (authoritative source).
- `sharepoint-list-schema.md` — list columns and loading.
- `import-flow-guide.md` — run-once bulk import.
- `flow-build-guide.md` — the daily reveal flow (hardened, bilingual).
- `adaptive-card-bilingual.json` — the EN + AR card.
- `scripts/extract_pilot.py` — regenerates the data from the workbook.

## Setup (one time, before Mon 3 Aug)

1. Create the `MonthOfConnection` list (`sharepoint-list-schema.md`).
2. Bulk-load the 21 rows (`import-flow-guide.md`, uses the JSON).
3. Confirm the pilot M365 Group / Teams team.
4. Build the daily reveal flow (`flow-build-guide.md`).
5. Pilot with 2–3 test users, then point at the real group and turn it **On**.

## Roles & governance (from the workbook)

| Role | Responsibility |
|------|----------------|
| Wellbeing team (Bader / Dr. Dania) | Content approval; Dr. Dania credited as author of the source nudge library. |
| Fahad / Health & Innovation Hub | Campaign architecture, AI-assisted selection/adaptation, bilingual workflow, anticipation mechanics, learning loop. |
| Champions (1/dept) | Daily 60-second huddle, approved WhatsApp forwarding, voluntary story/photo collection, weekly feedback. |
| IT / Microsoft 365 | Teams channel, scheduling by work pattern, polls, reactions, aggregate engagement analytics. |
| Marketing / Communications | Brand-approved cards, consent & privacy controls, weekly external recap, social governance. |

## Privacy & sharing

- Cards are **public-safe**; captions are pre-approved. No internal screenshots
  or personal/patient data in shared assets.
- Story/photo sharing is **voluntary and consent-based**.
- WhatsApp forwarding uses the same approved bilingual card to approved groups.

## Metrics & the September decision gate

- **Daily:** Teams reach, reactions, completions, role-adaptation requests,
  voluntary submissions.
- **Weekly:** one-question pulse + Champion feedback.
- **Fatigue signals:** channel mutes/leaves, declining reactions, "not relevant"
  feedback.
- **Decision gate (1–3 Sep):** review relevance, action, huddle adoption,
  shareability, sentiment, privacy, feedback — tune September before launch.
  *Future months are earned, not pre-committed.*

## Maintenance

- **Wellbeing team / Fahad** approve and edit challenge wording (in the list or
  by re-running `extract_pilot.py` against an updated workbook and re-importing).
- **IT** manages group membership and monitors flow run history (look for items
  marked `Error`).
- The reveal flow needs **no manual intervention** to send.
- After the pilot, the same pattern is reused month-to-month by loading the next
  month's rows — no flow rebuild needed.

## What was hardened vs. a naive build

| Risk | Fix |
|------|-----|
| Excel as datastore (file locks/throttling) | SharePoint List. |
| "Next pending" queue drifting if a day is missed | Match by `RevealDate` — each challenge fires on its own day or not at all. |
| Weekends/holidays sending | Working-day trigger + no row for that date → clean terminate. |
| Status updated regardless of send result | Success/failure branches; `Error` status + IT alert. |
| UTC timestamps | UAE-time `SentDateTime`. |
| Teams API throttling | `Apply to each` concurrency = 15. |
| Arabic lost / left-aligned | Stored intact; card renders RTL. |
