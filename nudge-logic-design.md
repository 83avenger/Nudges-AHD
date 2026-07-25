# Nudge Delivery Logic — Design for Confirmation

Status: **for review / confirmation before build.** This captures the logic as
clarified with management (4 nudges/day across the 4 wellbeing pillars, under one
daily theme, bilingual). It deliberately does **not** change the automation yet —
two points below need a team decision first.

## 1. Confirmed logic

- **4 nudges per working day**, one for each wellbeing pillar, in this sequence:
  1. **Social** wellbeing
  2. **Physical** wellbeing
  3. **Financial** wellbeing
  4. **Mental** wellbeing
- All four sit **under one daily theme**.
- Every nudge is **bilingual (English + Arabic)**.
- Source-traceable to Dr. Dania's wellbeing nudge library.

## 2. Two decisions needed before build

### Decision A — Delivery format
- **Option A · Four separate cards** at four times a day
  (e.g. 07:00 Social, 09:15 Physical, 11:30 Financial, 13:45 Mental — the
  original schedule).
- **Option B · One combined card** per day with four labelled sections
  (Mohammed's "4 messages under one nudge").

*Recommendation:* start the pilot with **Option A** (paced touchpoints match the
original design and give cleaner per-pillar engagement metrics); Option B is easy
to switch to later if four cards feel too frequent.

### Decision B — Scope for August
The *Month of Connection* workbook is currently **one connection nudge/day** (all
Social, 21 days). "4 pillars/day" means either:
- **B1 · August stays 1/day** (pure Connection) and 4/day begins **September**, or
- **B2 · August is rebuilt as 4/day** — each day keeps a connection theme but adds
  Physical, Financial and Mental nudges (needs 3 more nudges/day from the library).

*Recommendation:* **B1** — keep the tested August pilot as-is for a clean measure
at the September decision gate, and launch the full 4-pillar model from September.
Choose **B2** only if leadership wants all four pillars visible from day one.

## 3. Data model (4-nudges/day)

One row per **day**, with four bilingual pillar nudges. (If Option B / one card,
this is one send; if Option A / four cards, the flow sends each pillar at its
time slot.)

| Field | Notes |
|-------|-------|
| `Day`, `RevealDate`, `Weekday` | Calendar key. |
| `DailyTheme` | The one theme for the day (EN + AR). |
| `SocialEN` / `SocialAR` | Social pillar nudge. |
| `PhysicalEN` / `PhysicalAR` | Physical pillar nudge. |
| `FinancialEN` / `FinancialAR` | Financial pillar nudge. |
| `MentalEN` / `MentalAR` | Mental pillar nudge. |
| `WhyItMatters`, `TomorrowTeaser`, `SocialCaption` | Huddle line, teaser, caption. |
| `Source_Social/Physical/Financial/Mental` | One source ref per pillar. |
| `Status`, `SentDateTime`, `RunID` | Delivery tracking. |

For **Option A**, delivery tracking is per pillar (e.g. `Status_Social`,
`Status_Physical`, …) so a single failed slot can be re-sent without resending
the others.

## 4. Schedule

- **Option A:** one flow that runs at each of the four times and sends the
  matching pillar for today's row — or four small flows, one per time slot.
  Times per the original design: **07:00 / 09:15 / 11:30 / 13:45 UAE**, working
  days only.
- **Option B:** one flow at the morning reveal time (e.g. 08:00 UAE) sending the
  single combined card.

## 5. Worked example (illustrative — one day, Option A)

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

## 6. What stays the same regardless of the decisions

- Bilingual EN + AR, Arabic right-to-left on the card.
- Free / no-PC: Power Automate cloud flow + SharePoint List, standard connectors.
- SharePoint List as state store; run-once import; per-send error handling;
  UAE-time stamps; working-day scheduling.
- Source traceability to Dr. Dania's library.

---

### Next step
Confirm **Decision A** (four cards vs one card) and **Decision B** (August 1/day
vs 4/day). On confirmation, the data files, Adaptive Card(s) and flow guide are
updated to match — the current one-per-day pilot package remains valid for B1.
