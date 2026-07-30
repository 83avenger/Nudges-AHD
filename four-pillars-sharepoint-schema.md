# SharePoint List Schema — `FourPillarNudges` (4×/day variant)

Holds every **send** for the four-pillars model: **one row per nudge** =
21 working days × 4 pillars = **84 rows**. One row per send keeps delivery
tracking and time-slot matching simple, and lets a single failed slot be
re-sent without touching the others.

Data source: `data/four-pillars/by-nudge.json` / `.csv`.

> **Auto-create it** instead of building columns by hand:
> `provisioning/Create-Lists.ps1 -Only FourPillarNudges`, or *Create list → From
> CSV* with `by-nudge.csv`. See `provisioning/README.md`.

## Columns

| Display name    | Internal type                 | Notes |
|-----------------|-------------------------------|-------|
| `Title`         | Single line of text           | Default. Store `${Day}-${Pillar}` (e.g. `1-Social`). |
| `Day`           | Number                        | 1–21. |
| `RevealDate`    | **Date only**                 | Working day (e.g. `2026-08-03`). Matching key #1. |
| `DateLabel`     | Single line of text           | `3 Aug`. |
| `Weekday`       | Single line of text           | `Mon`…`Fri`. |
| `WeekArc`       | Single line of text           | e.g. `W1 · I See You`. |
| `DailyThemeEN`  | Single line of text           | The one theme for the day (English). |
| `DailyThemeAR`  | Single line of text           | Daily theme (Arabic). |
| `Pillar`        | Choice                        | `Social`, `Physical`, `Financial`, `Mental`. Matching key #2. |
| `PillarEN`      | Single line of text           | e.g. `Physical Wellbeing`. |
| `PillarAR`      | Single line of text           | e.g. `الرفاه البدني`. |
| `PillarEmoji`   | Single line of text           | 🤝 / 🏃 / 💡 / 🧠. |
| `PillarOrder`   | Number                        | 1–4 (delivery order). |
| `SlotTime`      | Single line of text           | `07:00` / `09:15` / `11:30` / `13:45`. |
| `NudgeEN`       | Multiple lines of text (plain)| English nudge. |
| `NudgeAR`       | Multiple lines of text (plain)| Arabic nudge (renders RTL on the card). |
| `SourceRef`     | Single line of text           | `#41` for Social (traceable); `draft` for the other pillars until the wellbeing team approves final wording. |
| `Status`        | Choice                        | `Scheduled`, `Sent`, `Error`. Default `Scheduled`. |
| `SentDateTime`  | Single line of text           | UAE local `yyyy-MM-dd HH:mm`. |
| `RunID`         | Single line of text           | Power Automate run name. |

## Delivery model

Four sends per working day, in Dr. Dania's pillar sequence:

| Slot | Time (UAE) | Pillar |
|------|-----------|--------|
| 1 | 07:00 | Social 🤝 |
| 2 | 09:15 | Physical 🏃 |
| 3 | 11:30 | Financial 💡 |
| 4 | 13:45 | Mental 🧠 |

Each send is picked by **`RevealDate = today` AND `Pillar = <slot's pillar>`**.

## Loading

Use the import flow (`import-flow-guide.md`, point it at
`data/four-pillars/by-nudge.json` and add the extra columns), or paste from
`by-nudge.csv` via grid view.

## Note on the Social pillar vs the others

The **Social** rows are the 21 approved Month of Connection challenges (source
refs intact). **Physical / Financial / Mental** are drafted here to complete the
model and are marked `SourceRef = draft` — the wellbeing team (Dr. Dania) should
review/approve final wording, ideally mapping each to its library entry. Arabic
is provided for all 84.
