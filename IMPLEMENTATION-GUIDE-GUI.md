# Implementation Guide — GUI Only (No PowerShell)

The whole build in the **browser** — SharePoint + Power Automate designer. No
PnP, no PowerShell, and it avoids the "From Excel" wizard (so the **WAC
access-token error can't happen**).

- **4 nudges/day**: 07:00 Social · 09:15 Physical · 11:30 Financial · 13:45
  Mental (UAE), on **AHD working days (Sun–Thu)**.
- **No PC left on** · **$0 beyond existing M365**.
- First-time build: **~90–110 minutes** (the manual columns + flows are the slow
  parts).

Prefer two commands? `IMPLEMENTATION-GUIDE.md` (PnP) is much faster.

---

## Step 1 · Create the recipient group (5 min)

In **Teams**, create/reuse a team or M365 Group with the pilot members
(e.g. `AH-Nudges`) — start with 2–3 test users. Note the group name.

---

## Step 2 · Create the list from Blank + add columns (25–30 min)

No file upload, no WAC.

1. SharePoint site → **+ New → List → Blank list** → name it `FourPillarNudges`.
2. For each column: **+ Add column → pick the type → Next → name → Save**. The
   default `Title` column already exists — leave it.

| Column | Type in the picker | Extra settings |
|--------|--------------------|----------------|
| `Day` | **Number** | — |
| `RevealDate` | **Date and time** | Include time = **No** |
| `DateLabel` | Single line of text | — |
| `Weekday` | Single line of text | — |
| `WeekArc` | Single line of text | — |
| `DailyThemeEN` | Single line of text | — |
| `DailyThemeAR` | Single line of text | — |
| `Pillar` | **Choice** | `Social`, `Physical`, `Financial`, `Mental` |
| `PillarEN` | Single line of text | — |
| `PillarAR` | Single line of text | — |
| `PillarEmoji` | Single line of text | — |
| `PillarOrder` | **Number** | — |
| `SlotTime` | Single line of text | — |
| `NudgeEN` | **Multiple lines of text** | rich text = No (plain) |
| `NudgeAR` | **Multiple lines of text** | plain |
| `SourceRef` | Single line of text | — |
| `Status` | **Choice** | `Scheduled`, `Sent`, `Error`; Default = `Scheduled` |
| `SentDateTime` | Single line of text | — |
| `RunID` | Single line of text | — |

> **"Long text" = "Multiple lines of text"** — there's no separate long-text type.

**Checkpoint:** all columns exist; `RevealDate` is **Date-only**, `Status` and
`Pillar` are **Choice**.

---

## Step 3 · Load the 84 rows — pick ONE (15–20 min)

### Option 1 · Paste in grid view (fastest, no flow)
1. Open `data/four-pillars/by-nudge.xlsx`.
2. Select the **data rows only** (not the header), in the list's column order,
   and **Copy**.
3. In SharePoint: list → **Edit in grid view** → click the first data cell →
   **Paste**. If columns misalign, paste **column by column** (foolproof).
4. Set `Status` to `Scheduled` for all if not already → **Exit grid view**.

### Option 2 · Run-once import flow (all-GUI, robust)
Build the flow in `import-flow-guide.md` (Manually trigger → Parse JSON → Create
item), point it at `data/four-pillars/by-nudge.json`, run once. No WAC, no PnP.

**Checkpoint:** **84 items**, all `Scheduled`, four `Pillar` values, Arabic RTL.

> **Verify column internal names before building flows.** Add a temporary **Get
> items** with **Filter/Order By/Top all empty** and run it. Output keys must be
> `Day`, `Pillar`, `Status`, `NudgeEN` … If they're `field_1`/`field_7`, the list
> came from *From Excel* — rebuild it as a **Blank list + Add column** (Step 2),
> which keeps internal names correct.

---

## Step 4 · Build the four reveal flows (35–45 min)

Open **`make.powerautomate.com` → + Create** (or Teams → Workflows) and follow
`four-pillars-flow-guide.md`. Build one, then **Save As** three times, changing
the **time** and **pillar** each:

| Flow | Time (UAE) | Pillar filter |
|------|-----------|---------------|
| Social | 07:00 | `Pillar eq 'Social'` |
| Physical | 09:15 | `Pillar eq 'Physical'` |
| Financial | 11:30 | `Pillar eq 'Financial'` |
| Mental | 13:45 | `Pillar eq 'Mental'` |

Each flow (all GUI actions):
1. **Recurrence** — Time zone **(UTC+04:00) Abu Dhabi, Muscat**, **Sun–Thu**, at
   the slot time.
2. **Get items** where `Pillar eq '<pillar>' and Status eq 'Scheduled'`, **Order
   By `Day asc`, Top 1**.
3. **Condition** — if none, **Terminate**.
4. **List group members** → **Apply to each** (concurrency 15) → **Post card in a
   chat or channel** as **Flow bot** → recipient = member `mail`. Paste
   `adaptive-card-pillar.json` and map the `${...}` tokens (table in the guide).
5. **Update item** → `Status=Sent`, UAE `SentDateTime`, `RunID` (on success);
   `Status=Error` on failure.

**Checkpoint:** all four flows save with no errors.

---

## Step 5 · Test with 2–3 users (10 min)

1. Point the flows at the **test group**.
2. **Test → Manually → Run** one flow (sends that pillar's Day 1 nudge).
3. Confirm the **bilingual card** arrives and the row flips to **Sent**.
4. Reset that row's `Status` to `Scheduled`.

---

## Step 6 · Go live (5 min)

Point the flows at the **real group**, all rows `Scheduled`, turn **all four**
flows **On** (a Sunday is a good start day).

---

## Step 7 · Monitor & maintain

- **Power Automate → Run history** for failures; reset any `Error` row to
  `Scheduled`.
- Edit content directly in the list.
- **September gate:** review metrics (`IT-handover.md`), load next month's rows.

---

## GUI troubleshooting

| Symptom | Fix |
|---------|-----|
| "Column 'Pillar' does not exist" in Get items | Replace the `PILLAR` placeholder with `'Social'` etc.; if it persists, the column's internal name differs — check List settings → column → URL `Field=`, re-select the list to refresh the action's schema, or recreate with PnP `Create-List.ps1`. Same for `Day`. Building from **Blank list** (Step 2) keeps internal names clean. |
| "Could not obtain a WAC access token" | You're using *From Excel* — don't. Use Step 2 (Blank list) + Step 3 grid paste / import flow. |
| No Date/Number in *From Excel* | Not needed — you set types on the Blank list yourself. |
| "long text" missing | It's **Multiple lines of text**. |
| Arabic left-aligned | Use `adaptive-card-pillar.json` unchanged (`rtl` set). |
| Paste misaligns columns | Paste column-by-column (Step 3 tip). |
| Card didn't post | Check *Post as Flow bot* and recipient = member `mail`; group has members. |

---

## TL;DR
1. Create the group.  2. **Blank list** + add columns.  3. **Grid-paste** the
84 rows.  4. Build 4 flows (Save-As ×3).  5. Test with 2–3 users.  6. Turn all
4 On.  7. Monitor.
