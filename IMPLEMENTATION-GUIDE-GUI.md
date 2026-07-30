# Implementation Guide — GUI Only (No PowerShell)

Everything here is done in the **browser** — SharePoint and the Power Automate
designer. No PnP, no PowerShell, and it avoids the "From Excel" wizard entirely
(so the **WAC access-token error can't happen**).

- **No PC left on** · **$0 beyond existing M365** · standard connectors only.
- First-time build: **~75–100 minutes.**

> Prefer two PowerShell commands? See `IMPLEMENTATION-GUIDE.md` (Track A). This
> file is the all-clicks alternative.

---

## Step 0 · Pick the model (5 min)

| | **Model A — Month of Connection** | **Model B — Four pillars 4×/day** |
|---|---|---|
| List name | `MonthOfConnection` | `FourPillarNudges` |
| Rows | 21 | 84 |
| Card file | `adaptive-card-bilingual.json` | `adaptive-card-pillar.json` |
| Flow guide | `flow-build-guide.md` | `four-pillars-flow-guide.md` |
| Data file | `data/month-of-connection.json` | `data/four-pillars/by-nudge.json` |

Use the matching column table in Step 2. *(Unsure? Model A for August, B from Sep.)*

---

## Step 1 · Create the recipient group (5 min)

1. In **Teams**, create (or reuse) a team/M365 Group with the pilot members —
   e.g. `AH-Nudges`. Start with **2–3 test users** for now.
2. Note the group **name** (you'll pick it in the flow later).

---

## Step 2 · Create the list from Blank + add columns (20–25 min)

This is the reliable GUI path — no file upload, no WAC.

1. Go to your SharePoint site → **+ New → List → Blank list**.
2. Name it exactly (`MonthOfConnection` or `FourPillarNudges`) → **Create**.
3. For each column below: **+ Add column → choose the type → Next → fill name →
   Save.** (The default `Title` column already exists — leave it.)

### Columns for Model A · `MonthOfConnection`

| Column name | Type in the picker | Extra settings |
|-------------|--------------------|----------------|
| `Day` | **Number** | — |
| `RevealDate` | **Date and time** | Include time = **No** (date only) |
| `DateLabel` | **Single line of text** | — |
| `Weekday` | **Single line of text** | — |
| `WeekArc` | **Single line of text** | — |
| `ChallengeEN` | **Multiple lines of text** | Use enhanced rich text = **No** (plain) |
| `ChallengeAR` | **Multiple lines of text** | plain |
| `WhyItMatters` | **Multiple lines of text** | plain |
| `TomorrowTeaser` | **Multiple lines of text** | plain |
| `SocialCaption` | **Multiple lines of text** | plain |
| `SourceRef` | **Single line of text** | — |
| `Status` | **Choice** | Choices: `Scheduled`, `Sent`, `Error`; Default = `Scheduled` |
| `SentDateTime` | **Single line of text** | — |
| `RunID` | **Single line of text** | — |

### Columns for Model B · `FourPillarNudges`

| Column name | Type | Extra settings |
|-------------|------|----------------|
| `Day` | Number | — |
| `RevealDate` | Date and time | Include time = No |
| `DateLabel` | Single line of text | — |
| `Weekday` | Single line of text | — |
| `WeekArc` | Single line of text | — |
| `DailyThemeEN` | Single line of text | — |
| `DailyThemeAR` | Single line of text | — |
| `Pillar` | **Choice** | Choices: `Social`, `Physical`, `Financial`, `Mental` |
| `PillarEN` | Single line of text | — |
| `PillarAR` | Single line of text | — |
| `PillarEmoji` | Single line of text | — |
| `PillarOrder` | Number | — |
| `SlotTime` | Single line of text | — |
| `NudgeEN` | **Multiple lines of text** | plain |
| `NudgeAR` | **Multiple lines of text** | plain |
| `SourceRef` | Single line of text | — |
| `Status` | **Choice** | `Scheduled`, `Sent`, `Error`; Default = `Scheduled` |
| `SentDateTime` | Single line of text | — |
| `RunID` | Single line of text | — |

> **"Long text" = "Multiple lines of text"** — there is no separate long-text
> type. Pick "Multiple lines of text" and turn rich text off for clean values.

**Checkpoint:** the list has every column, `RevealDate` is **Date-only**, and
`Status` (and `Pillar`) is a **Choice** with the right options.

---

## Step 3 · Load the rows — pick ONE (15–20 min)

### Option 1 · Paste in grid view (fastest, no flow)
1. Open the matching **.xlsx** on your PC:
   `data/month-of-connection.xlsx` or `data/four-pillars/by-nudge.xlsx`.
2. In the sheet, select the **data rows only** (not the header), matching the
   column order of your list, and **Copy**.
3. In SharePoint, open the list → **Edit in grid view**.
4. Click the first cell under the **first data column** and **Paste**. SharePoint
   fills the rows. Set `Status` to `Scheduled` for all if not already.
5. **Exit grid view** to save.

> Tip: if pasting all columns at once misaligns, paste **column by column**
> (copy one Excel column, paste into the matching grid column). Tedious but
> foolproof. This uses **no WAC**.

### Option 2 · Run-once import flow (robust, all-GUI)
Build the small flow in `import-flow-guide.md` (Manually trigger → Parse JSON →
Create item), point it at `data/…json`, run it once. This is entirely in the
Power Automate designer — no PowerShell, no WAC.

**Checkpoint:** Model A shows **21** items (2026-08-03 → 08-31); Model B shows
**84**. All `Status = Scheduled`. Arabic renders right-to-left.

---

## Step 4 · Build the reveal flow in the designer (25–30 min)

Open **`make.powerautomate.com` → + Create** (or **Teams → Workflows**) and
follow the matching guide click-for-click:

- **Model A:** `flow-build-guide.md`
- **Model B:** `four-pillars-flow-guide.md`

All steps there are GUI actions. In short:
1. **Recurrence** trigger — Time zone **(UTC+04:00) Abu Dhabi, Muscat**, **AHD
   working days Sun–Thu** (Fri–Sat unchecked), at the reveal time(s).
2. **Get items** (SharePoint) where `Status = Scheduled` (+ `Pillar` for Model
   B), **Order By `Day asc`, Top 1** — the next challenge in sequence (no date
   matching, so the calendar dates in the list don't matter).
3. **Condition** — if none, **Terminate**.
4. **List group members** (Office 365 Groups) → your pilot group.
5. **Apply to each** (concurrency 15) → **Post card in a chat or channel** as
   **Flow bot** → recipient = member `mail`. Paste the matching **Adaptive Card
   JSON** and map the `${...}` tokens (tables in each guide).
6. **Update item** → `Status=Sent`, UAE `SentDateTime`, `RunID` (on success);
   `Status=Error` on failure.

**Checkpoint:** the flow saves with no validation errors.

---

## Step 5 · Test with 2–3 users (10 min)

1. Make sure the flow points at your **test group**.
2. **Test → Manually → Run** (it sends Day 1, the next `Scheduled` row).
3. Confirm the **bilingual card** arrives in Teams and the row flips to **Sent**
   with a UAE timestamp + RunID.
4. Reset that row's `Status` to `Scheduled` so the real run starts from Day 1.

---

## Step 6 · Go live (5 min)

1. Point the flow at the **real pilot group**.
2. All rows `Scheduled`, `SentDateTime`/`RunID` empty.
3. Turn the flow **On** (enable all four for Model B).

---

## Step 7 · Monitor & maintain (ongoing)

- **Power Automate → flow → Run history** for failures. Reset any `Error` row to
  `Scheduled` to re-send.
- **Edit content** directly in the SharePoint list (Marketing/wellbeing team).
- **September gate:** review metrics (`IT-handover.md`), load next month's rows.

---

## GUI troubleshooting

| Symptom | Fix |
|---------|-----|
| "Could not obtain a WAC access token" | You're using *From Excel* — don't. Use Step 2 (Blank list) + Step 3 grid paste / import flow. |
| No Date/Number option in *From Excel* | Not needed here — you set types yourself on the Blank list. |
| "long text" missing | It's **Multiple lines of text**. |
| Arabic left-aligned in the card | Use the provided card JSON unchanged (`rtl` is set). |
| Paste misaligns columns | Paste column-by-column (Step 3 tip). |
| Card didn't post | Check *Post as Flow bot* and recipient = member `mail`; confirm the group has members. |

---

## TL;DR (all clicks)
1. Create the Teams group.  2. **Blank list** + add columns (Step 2 table).
3. **Grid-view paste** the .xlsx rows.  4. Build the flow (guide).
5. Test with 2–3 users.  6. Turn On.  7. Monitor.
