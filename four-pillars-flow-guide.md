# Power Automate — Four-Pillars, 4×/Day (Bilingual, Free / No PC)

Sends **four bilingual nudges per working day** — one per wellbeing pillar, in
Dr. Dania's sequence — each on its own Teams card at its time slot:

| Slot | Time (UAE) | Pillar |
|------|-----------|--------|
| 1 | 07:00 | Social 🤝 |
| 2 | 09:15 | Physical 🏃 |
| 3 | 11:30 | Financial 💡 |
| 4 | 13:45 | Mental 🧠 |

Standard connectors only — **included in Microsoft 365**, no premium licence, no
Azure, **no PC left on** (cloud flows run on Microsoft's servers).

> This is the **4×/day variant**. For the single-hero-challenge pilot see
> `flow-build-guide.md`. For the combined-single-card option see the note at the
> end.

## Recommended structure: four small flows (one per slot)

Because the four times have different minutes (07:00, 09:15, 11:30, 13:45), a
single Recurrence trigger can't fire all four. The simplest, most reliable
pattern is **four near-identical flows**, one per pillar/time. Each isolates its
pillar, so a Physical failure never affects Mental.

Build **one** flow, confirm it, then **Save As** three copies and change only the
**time** and the **pillar** in each.

### Steps (parameterised by SLOT = `HH:MM` and PILLAR = Social/Physical/Financial/Mental)

**Step 1 — Trigger: Recurrence**
- Frequency **Week**, Interval **1**; **On these days:** Mon–Fri.
- **At these hours/minutes:** the SLOT time (e.g. `9` / `15` for Physical).
- **Time zone:** `(UTC+04:00) Abu Dhabi, Muscat`.

**Step 2 — Today's UAE date**
- **Compose** `TodayUAE` = `convertTimeZone(utcNow(),'UTC','Arabian Standard Time','yyyy-MM-dd')`.

**Step 3 — Get this slot's nudge**
- **Get items** on `FourPillarNudges`, **Filter Query:**
  ```
  RevealDate eq '@{outputs('TodayUAE')}' and Pillar eq 'PILLAR' and Status eq 'Scheduled'
  ```
  **Top Count:** `1`.

**Step 4 — Stop if nothing scheduled**
- **Condition** `length(body('Get_items')?['value'])` equal to `0`
  → **If yes:** Terminate (weekend / holiday / pilot over).
  → **If no:** **Compose** `Nudge` = `first(body('Get_items')?['value'])`.

**Step 5 — Recipients**
- **List group members** (Office 365 Groups) for the pilot group.

**Step 6 — Send the pillar card**
- **Apply to each** member (Concurrency **On, Degree 15**):
  - **Post card in a chat or channel** → **Post as Flow bot** →
    **Recipient:** `items('Apply_to_each')?['mail']`.
  - **Adaptive Card:** `adaptive-card-pillar.json`, tokens bound to `Nudge`:
    | Token | Bind to |
    |-------|---------|
    | `${PillarEmoji}` | `outputs('Nudge')?['PillarEmoji']` |
    | `${PillarEN}` | `outputs('Nudge')?['PillarEN']` |
    | `${PillarAR}` | `outputs('Nudge')?['PillarAR']` |
    | `${DailyThemeEN}` | `outputs('Nudge')?['DailyThemeEN']` |
    | `${WeekArc}` | `outputs('Nudge')?['WeekArc']` |
    | `${Day}` | `outputs('Nudge')?['Day']` |
    | `${NudgeEN}` | `outputs('Nudge')?['NudgeEN']` |
    | `${NudgeAR}` | `outputs('Nudge')?['NudgeAR']` |
  - Wrap in a Scope `SendScope`.

**Step 7 — Mark Sent (on success)** — `Configure run after` = succeeded:
- **Update item**: `Status`=`Sent`,
  `SentDateTime`=`convertTimeZone(utcNow(),'UTC','Arabian Standard Time','yyyy-MM-dd HH:mm')`,
  `RunID`=`workflow()?['run']?['name']`.

**Step 8 — On failure** — `Configure run after` = failed/timed out:
- **Update item**: `Status`=`Error`, `RunID`=run name; optional IT alert with
  `Day` + `Pillar`.

**Step 9 — Clone for the other three slots**
- **Save As** → rename (e.g. *Thrive365 – Physical 09:15*) → change the trigger
  time and the `Pillar eq '...'` filter. Repeat for Financial and Mental.

## Alternative: one flow, 15-minute gate

If you prefer a single flow: Recurrence **every 15 min** (Mon–Fri 07:00–14:00) +
a **Switch** on `convertTimeZone(utcNow(),'UTC','Arabian Standard Time','HH:mm')`
mapping `07:00→Social, 09:15→Physical, 11:30→Financial, 13:45→Mental`; default →
Terminate. More logic in one place, but only one flow to maintain.

## Alternative: one combined card per day (Option B)

If the team prefers **all four pillars on one card** (one send/morning) instead
of four sends: use `data/four-pillars/by-day.json` (21 rows, each with all four
pillars), one Recurrence at 08:00, and a card with four labelled bilingual
sections. Say the word and this card + guide can be added.

## Cost & licensing

Same as the pilot: **$0** beyond existing Microsoft 365 — SharePoint, Teams,
Office 365 Groups, Recurrence are all **standard** connectors. No PC.

## Regenerating the data

```bash
python3 scripts/gen_four_pillars.py
```
(Reads the approved Social challenges from `data/month-of-connection.json` and
rebuilds the 84-row dataset.)
