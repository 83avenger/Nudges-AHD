# Nudge Delivery Logic — Decision Record (FINAL)

Status: **DECIDED and built.** The automation implements this model. The earlier
open questions are resolved; kept here as the record.

## 1. The model

- **4 nudges per working day**, one for each wellbeing pillar, in this sequence:
  1. **Social** wellbeing — 07:00
  2. **Physical** wellbeing — 09:15
  3. **Financial** wellbeing — 11:30
  4. **Mental** wellbeing — 13:45  (UAE)
- All four sit **under one daily theme**.
- **Four separate bilingual cards** (not one combined) — one per pillar at its
  time slot.
- Every nudge is **bilingual (English + Arabic)**; Arabic renders RTL.
- **AHD working week = Sunday–Thursday**; each pillar's flow sends the next unsent
  nudge in `Day` order, independent of calendar dates.
- Source-traceable to Dr. Dania's library (`SourceRef`).

## 2. Resolved decisions

- **Delivery format → four separate cards** (Option A). The combined single-card
  option is archived (`archive/option-b-combined-card/`).
- **Scope → the whole program runs 4 pillars/day.** The one-challenge-per-day
  layout is archived (`archive/model-a-one-per-day/`). The 21 approved connection
  challenges are reused as the **Social** pillar.

## 3. Data model (4-nudges/day)

**One row per send** (= one pillar on one day): 21 days × 4 pillars = 84 rows.
Per-row delivery tracking means a single failed slot can be re-sent without
touching the others. See `four-pillars-sharepoint-schema.md` for the full column
list. Key fields:

| Field | Notes |
|-------|-------|
| `Day`, `RevealDate`, `Weekday`, `WeekArc` | `Day` is the ordering key; `RevealDate` informational. |
| `DailyThemeEN` / `DailyThemeAR` | The day's theme. |
| `Pillar`, `SlotTime` | Social/Physical/Financial/Mental and its time. |
| `NudgeEN` / `NudgeAR` | The bilingual nudge. |
| `SourceRef` | Library ref (Social) or `draft`. |
| `Status`, `SentDateTime`, `RunID` | Per-send delivery tracking. |

## 4. Schedule

Four small flows (one per slot), or one flow with a 15-minute gate. Times:
**07:00 Social / 09:15 Physical / 11:30 Financial / 13:45 Mental** (UAE), on AHD
working days **Sun–Thu**. Each pillar advances in `Day` order.

## 5. Worked example (one day)

> Theme: **Connection — "See People."**

| Pillar | English | Arabic |
|--------|---------|--------|
| Social | Use their name — greet one colleague by name today. | استخدم اسمه - حيِّ زميلاً واحداً باسمه اليوم. |
| Physical | Stand and stretch for one minute before your next task. | قِف وتمدّد لمدة دقيقة قبل مهمتك التالية. |
| Financial | Note one small expense you can plan for this week. | دوّن مصروفاً بسيطاً يمكنك التخطيط له هذا الأسبوع. |
| Mental | Take three slow breaths before you start. | خذ ثلاثة أنفاس بطيئة قبل أن تبدأ. |

*(Social line is from the existing library; the other three are placeholders to
show the shape — real wording comes from Dr. Dania's library, approved by the
wellbeing team.)*

## 6. Design principles (unchanged)

- Bilingual EN + AR, Arabic right-to-left on the card.
- Free / no-PC: Power Automate cloud flows + SharePoint List, standard connectors.
- SharePoint List as state store; per-send error handling; UAE-time stamps;
  Sun–Thu scheduling; `Day`-order sequencing (no date coupling).
- Source traceability to Dr. Dania's library.

---

## What's built

- Data: `data/four-pillars/by-nudge.json` / `.csv` / `.xlsx` — **84 sends**.
- Card: `adaptive-card-pillar.json`. Flow: `four-pillars-flow-guide.md`.
- Schema: `four-pillars-sharepoint-schema.md`. List provisioning: `provisioning/`.
- Generator: `scripts/gen_four_pillars.py`.

**Open content item (not a logic decision):** Social pillar = the 21 approved
connection challenges; **Physical / Financial / Mental** are bilingual **drafts**
(`SourceRef = draft`) for the wellbeing team (Dr. Dania) to approve and map to the
source library, with a native-Arabic review before go-live.
