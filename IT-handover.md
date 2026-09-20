# IT Handover — AHD Wellbeing365 Nudges Automation

## Project overview

Deliver **4 bilingual (English + Arabic) wellbeing nudges per working day**, one
per pillar, to the pilot group in Microsoft Teams:

| Slot (UAE) | Pillar |
|-----------|--------|
| 07:00 | 🤝 Social |
| 09:15 | 🏃 Physical |
| 11:30 | 💡 Financial |
| 13:45 | 🧠 Mental |

AHD's working week is **Sunday–Thursday** (weekend Fri–Sat), and the flows are
scheduled accordingly. Over ~4 working weeks that's **84 nudges** (21 days × 4).

Daily ritual: **Reveal → Huddle → Act → Share → Recognize → Tease Tomorrow.**
The automation covers the **Reveal** (the 4 nudges); the huddle and sharing are
human activities led by Wellbeing Champions.

> **No PC or server needs to stay on.** These are Power Automate **cloud** flows —
> Microsoft runs them on its own servers on schedule. (The "PC must be on"
> concern only applies to Power Automate *Desktop* / RPA, which this is not.)

## Cost

**$0 beyond existing Microsoft 365 licences.** Every connector used (SharePoint,
Teams, Office 365 Groups, Recurrence) is **standard** — **no premium Power
Automate licence** required.

## Bilingual requirement

Each nudge card shows English and Arabic together (English block, then a
right-to-left Arabic block, plus the daily theme). All Arabic is populated;
Social wording is approved (from the workbook), the other three pillars are
drafts pending wellbeing-team approval.

## Components

| Component | Purpose |
|-----------|---------|
| SharePoint List `FourPillarNudges` | The 84 bilingual nudges + pillar/slot + Status/SentDateTime/RunID. |
| Microsoft 365 Group / Teams team | The pilot recipients. |
| Four Power Automate cloud flows (one per slot) | Fire 07:00/09:15/11:30/13:45 UAE on Sun–Thu; each sends its pillar's next nudge in Day order and updates status. |
| Bilingual Adaptive Card (Teams Flow bot) | EN + AR pillar notification. |
| (Optional) poll / preview / pulse flows | Mid-week guess-poll, pre-week Champion preview, end-of-week (Thu) pulse — the anticipation + measurement loop. |

## Files in this package

- `data/four-pillars/by-nudge.json` / `.csv` / `.xlsx` — the 84 nudges, seeded
  `Scheduled`. Social is traceable via `SourceRef`; other pillars = `draft`.
- `source/AHD_Wellbing365_Month_of_Connection_August2026.xlsx` — original workbook.
- `four-pillars-sharepoint-schema.md` — list columns.
- `provisioning/` — auto-create the list + load rows (PnP / From-Excel / site script).
- `import-flow-guide.md` — all-GUI run-once loader alternative.
- `four-pillars-flow-guide.md` — the four reveal flows (hardened, bilingual).
- `adaptive-card-pillar.json` — the EN + AR pillar card.
- `scripts/gen_four_pillars.py` — regenerates the data.

## Setup (one time)

1. Create the `FourPillarNudges` list + load the 84 rows (`provisioning/README.md`).
2. Confirm the pilot M365 Group / Teams team.
3. Build the four per-slot reveal flows (`four-pillars-flow-guide.md`).
4. Pilot with 2–3 test users, then point at the real group and turn all four **On**.

Full step-by-step: `IMPLEMENTATION-GUIDE.md` (PnP) or `IMPLEMENTATION-GUIDE-GUI.md`.

## Roles & governance (from the workbook)

| Role | Responsibility |
|------|----------------|
| Wellbeing team (Bader / Dr. Dania) | Content approval; Dr. Dania credited as author of the source nudge library. |
| Fahad / Health & Innovation Hub | Campaign architecture, AI-assisted selection/adaptation, bilingual workflow, anticipation mechanics, learning loop. |
| Champions (1/dept) | Daily 60-second huddle, approved WhatsApp forwarding, voluntary story/photo collection, weekly feedback. |
| IT / Microsoft 365 | Teams channel, scheduling by work pattern, polls, reactions, aggregate engagement analytics. |
| Marketing / Communications | Brand-approved cards, consent & privacy controls, weekly external recap, social governance. |

## Connection ownership (fix before go-live)

The flows authenticate as whoever built them. Running them under a **personal**
(or Tier‑0 admin) account means they **break when that person leaves** or their
account/MFA changes. **Before launch**, re‑authorize all connections under a
**dedicated service account** and add IT as co‑owners — see
`operations-service-account.md`.

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

- **Wellbeing team / Fahad** approve and edit nudge wording (in the list or by
  re-running `scripts/gen_four_pillars.py` and re-importing). Priority: approve
  the Physical/Financial/Mental drafts and a native-Arabic review before go-live.
- **IT** manages group membership and monitors flow run history (look for items
  marked `Error`).
- The reveal flow needs **no manual intervention** to send.
- After the pilot, the same pattern is reused month-to-month by loading the next
  month's rows — no flow rebuild needed.

## What was hardened vs. a naive build

| Risk | Fix |
|------|-----|
| Excel as datastore (file locks/throttling) | SharePoint List. |
| Wrong working week | Trigger set to **AHD Sun–Thu**; challenges sent in `Day` order, independent of calendar dates — no list edits when the week differs. |
| Weekend sending | Recurrence limited to Sun–Thu; holidays handled by pausing the flow that day. |
| Status updated regardless of send result | Success/failure branches; `Error` status + IT alert. |
| UTC timestamps | UAE-time `SentDateTime`. |
| Teams API throttling | `Apply to each` concurrency = 15. |
| Arabic lost / left-aligned | Stored intact; card renders RTL. |
