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

This is **the** delivery model: 4 nudges/day, one per pillar, each as its own
bilingual card. (AHD working week = **Sunday–Thursday**.)

## Structure: four small flows (one per slot)

Because the four times have different minutes (07:00, 09:15, 11:30, 13:45), a
single Recurrence trigger can't fire all four. The simplest, most reliable
pattern is **four near-identical flows**, one per pillar/time. Each isolates its
pillar, so a Physical failure never affects Mental.

Build **one** flow, confirm it, then **Save As** three copies and change only the
**time** and the **pillar** in each.

### Steps (parameterised by SLOT = `HH:MM` and PILLAR = Social/Physical/Financial/Mental)

**Step 1 — Trigger: Recurrence (AHD working days, Sun–Thu)**
- Frequency **Week**, Interval **1**; **On these days:** **Sunday, Monday,
  Tuesday, Wednesday, Thursday** (AHD weekend Fri–Sat unchecked).
- **At these hours/minutes:** the SLOT time (e.g. `9` / `15` for Physical).
- **Time zone:** `(UTC+04:00) Abu Dhabi, Muscat`.

**Step 2 — Get this slot's next nudge (by Day order)**
- **Get items** on `FourPillarNudges`, **Filter Query** — **replace `PILLAR`
  with the real pillar name** for this flow (`Social` / `Physical` / `Financial`
  / `Mental`), e.g. for the Social flow:
  ```
  Pillar eq 'Social' and Status eq 'Scheduled'
  ```
  **Order By:** `Day asc` · **Top Count:** `1`.
- This sends the next unsent nudge for that pillar, so the four pillar tracks
  each advance one per working day — independent of the calendar dates in the
  list.

> **Filter/Order By use column INTERNAL names, not display names.** If you get
> *"Column 'Pillar' does not exist"*, the column's internal name differs (common
> when the list was made via *From Excel/CSV*, which can name it `Pillar0` /
> `field_7`). Fixes: (1) **List settings → click the column →** the `Field=` value
> in the URL is the internal name to use; (2) run **Get items with no
> filter/order-by once** and read the exact field names from the output; (3)
> re-select the Site + List in the action to refresh its cached schema; or (4)
> recreate the list with `provisioning/Create-List.ps1`, which sets internal
> names to exactly `Pillar`, `Day`, `Status`. The same applies to `Day` in
> Order By.

**Step 3 — Stop if nothing left**
- **Condition** `length(body('Get_items')?['value'])` equal to `0`
  → **If yes:** Terminate (this pillar's 21 nudges are all sent).
  → **If no:** **Compose** `Nudge` = `first(body('Get_items')?['value'])`.

**Step 4 — Recipients**
- **List group members** (Office 365 Groups) for the pilot group.

**Step 5 — Send the pillar card**
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

**Step 6 — Mark Sent (on success)** — `Configure run after` = succeeded:
- **Update item**: `Status`=`Sent`,
  `SentDateTime`=`convertTimeZone(utcNow(),'UTC','Arabian Standard Time','yyyy-MM-dd HH:mm')`,
  `RunID`=`workflow()?['run']?['name']`.

**Step 7 — On failure** — `Configure run after` = failed/timed out:
- **Update item**: `Status`=`Error`, `RunID`=run name; optional IT alert with
  `Day` + `Pillar`.

**Step 8 — Clone for the other three slots**
- **Save As** → rename (e.g. *Thrive365 – Physical 09:15*) → change the trigger
  time and the `Pillar eq '...'` filter. Repeat for Financial and Mental.

## Optional: one flow instead of four (15-minute gate)

If you'd rather maintain a single flow: Recurrence **every 15 min**
(Sun–Thu 07:00–14:00) + a **Switch** on
`convertTimeZone(utcNow(),'UTC','Arabian Standard Time','HH:mm')` mapping
`07:00→Social, 09:15→Physical, 11:30→Financial, 13:45→Mental`; default →
Terminate; then the same Get-items / send / update steps. Same behaviour as the
four flows, consolidated. Choose whichever your team prefers to maintain.

## Cost & licensing

Same as the pilot: **$0** beyond existing Microsoft 365 — SharePoint, Teams,
Office 365 Groups, Recurrence are all **standard** connectors. No PC.

## Regenerating the data

```bash
python3 scripts/gen_four_pillars.py
```
(Reads the approved Social challenges from `data/month-of-connection.json` and
rebuilds the 84-row dataset.)
