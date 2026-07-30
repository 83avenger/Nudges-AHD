# Implementation Guide — AHD Wellbeing365 Nudges (End to End)

Follow this in order to go from zero to a live, automated, bilingual nudge
program. It covers **both** delivery models — pick one at Step 0.

- **No PC left on** — everything runs in the Microsoft 365 cloud.
- **$0 beyond existing M365** — standard connectors only.
- Estimated time: **~60–90 minutes** the first time.

Detailed references are linked at each step; this page is the running order.

---

## Step 0 · Decide the delivery model (5 min)

| | **Model A — Month of Connection pilot** | **Model B — Four pillars, 4×/day** |
|---|---|---|
| Sends | 1 bilingual challenge/working day | 4 nudges/day (Social→Physical→Financial→Mental) |
| List | `MonthOfConnection` (21 rows) | `FourPillarNudges` (84 rows) |
| Card | `adaptive-card-bilingual.json` | `adaptive-card-pillar.json` |
| Flow guide | `flow-build-guide.md` | `four-pillars-flow-guide.md` |
| Best for | Clean, measurable pilot for the Sep gate | The confirmed full operating model |

> If unsure, run **Model A** for August (it's the approved, tested pilot) and
> switch to **Model B** from September. The steps below work for either — just
> use the list/card/flow from the matching column.

**Checkpoint:** you know which list, card and flow guide you're using.

---

## Step 1 · Prerequisites (10 min)

- [ ] A Microsoft 365 account with **Teams, SharePoint, Power Automate** (standard).
- [ ] A **SharePoint site** to hold the list (a team site is fine).
- [ ] Rights to **create a list** on that site (site Member/Owner).
- [ ] A **Microsoft 365 Group / Teams team** containing the pilot recipients
      (create one now if needed — e.g. `AH-Nudges`). Note its name/ID.
- [ ] For the PnP route: **PowerShell** with the PnP module:
      ```powershell
      Install-Module PnP.PowerShell -Scope CurrentUser
      ```
- [ ] The files from this repo on your machine (clone or download the branch).

**Checkpoint:** you can open PowerShell and your SharePoint site in a browser.

---

## Step 2 · Create the SharePoint list (10 min)

Pick **one** track. Track A is the most reliable (it avoids the "From Excel"
wizard's WAC-token error and column-type limits).

### Track A — PnP PowerShell (recommended)
```powershell
cd provisioning
./Create-Lists.ps1 -SiteUrl "https://<tenant>.sharepoint.com/sites/<YourSite>"
# creates BOTH lists with exact types; add -Only MonthOfConnection to do just one
```
Sign in when prompted. This builds every column with the correct type
(Date-only, Number, Choice, Multiple-lines) and sets `Status` default `Scheduled`.

### Track B — UI, "From Excel"
1. Site → **+ New → List → From Excel**.
2. Upload the **.xlsx** (not CSV — CSV triggers the WAC error more often):
   `data/month-of-connection.xlsx` **or** `data/four-pillars/by-nudge.xlsx`.
3. Set column types: long fields → **Multiple lines of text** (that *is* the
   "long text" option); `Status`/`Pillar` → **Choice**; `RevealDate` → **Date**,
   `Day`/`PillarOrder` → **Number** *if offered*.
4. If Date/Number aren't offered, or you get **"Could not obtain a WAC access
   token"**, stop and use Track A — it's the intended fix. (See
   `provisioning/README.md` for all fallbacks.)

**Checkpoint:** the list exists with the right columns. Confirm `RevealDate` is a
**Date** column and `Status` is a **Choice** — the flow depends on both.

---

## Step 3 · Load the challenge rows (10 min)

If you used **Track B / From Excel**, the rows are already loaded — **skip to
Step 4** (just verify the count and that Arabic shows right-to-left).

If you used **Track A**, load the data via PnP (no WAC, no Power Automate):
```powershell
./Import-Data.ps1 -SiteUrl "https://<tenant>.sharepoint.com/sites/<YourSite>" -List MonthOfConnection
# Model B: -List FourPillarNudges
# reload cleanly if needed: add -Fresh
```

**Checkpoint:** Model A shows **21** items (dates 2026-08-03 → 08-31); Model B
shows **84** items. `Status` = `Scheduled` on all. Arabic renders RTL.

---

## Step 4 · Confirm the recipient group (5 min)

- Open your M365 Group / Teams team and confirm the **pilot members** are in it.
- Copy the **Group ID** (or name) — the flow needs it.
- Keep the pilot small for the first live test (2–3 people), then expand.

**Checkpoint:** you have the group and its ID, with test users in it.

---

## Step 5 · Build the Power Automate flow (20–30 min)

Open `make.powerautomate.com` (or Teams → Workflows) and follow the matching
guide step by step:

- **Model A:** `flow-build-guide.md` — daily reveal, matches today's `RevealDate`,
  08:00 UAE, working days.
- **Model B:** `four-pillars-flow-guide.md` — four per-slot flows (07:00 Social,
  09:15 Physical, 11:30 Financial, 13:45 Mental), each matched by `RevealDate` +
  `Pillar`.

Key points the guides cover:
- Recurrence trigger, **time zone = (UTC+04:00) Abu Dhabi, Muscat**, working days.
- **Get items** filtered to today's date (+ pillar for Model B) and
  `Status eq 'Scheduled'`, top 1.
- **List group members** → **Apply to each** (concurrency 15) →
  **Post card in a chat or channel** as **Flow bot** to `member mail`.
- Paste the matching **Adaptive Card JSON** and bind the `${...}` tokens to the
  challenge fields (token→field tables are in each guide).
- On success → **Update item** `Status=Sent`, UAE `SentDateTime`, `RunID`.
  On failure → `Status=Error` + optional IT alert.

**Checkpoint:** the flow saves without errors.

---

## Step 6 · Test (10 min)

1. Temporarily point the flow at your **2–3 person test group**.
2. To test off-schedule, relax the Step-3 filter to any `Scheduled` row (or set
   one row's `RevealDate` to today), then **Test → Manually → Run**.
3. Confirm:
   - The **bilingual card** arrives in Teams (English + Arabic, RTL, day counter).
   - The list item flips to **`Sent`** with a **UAE timestamp** and a **`RunID`**.
4. Restore the real filter and reset that test row's `Status` to `Scheduled`.

**Checkpoint:** a real card was received and the row updated correctly.

---

## Step 7 · Go live (5 min)

1. Point the flow at the **real pilot group**.
2. Make sure all rows are `Status = Scheduled` and `SentDateTime`/`RunID` empty.
3. Turn the flow **On**.
4. For Model B, enable **all four** slot flows.

**Checkpoint:** flow(s) On, first reveal will fire on the next scheduled slot
(Model A: 08:00 UAE next working day; the pilot starts Mon 3 Aug 2026).

---

## Step 8 · Monitor & maintain (ongoing)

- **Power Automate → the flow → Run history**: watch for failures; any row left
  `Error` can be reset to `Scheduled` to re-send.
- **Content edits:** the wellbeing team edits wording directly in the list, or
  re-run the generators and re-import:
  ```powershell
  # from repo root
  python3 scripts/extract_pilot.py source/AHD_...August2026.xlsx   # Model A data
  python3 scripts/gen_four_pillars.py                              # Model B data
  ./provisioning/Import-Data.ps1 -SiteUrl "..." -List <List> -Fresh
  ```
- **Group membership:** IT manages who's in the recipient group.
- **September gate (1–3 Sep):** review the metrics in `IT-handover.md`, then load
  next month's rows — no flow rebuild needed.

---

## Troubleshooting quick table

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Could not obtain a WAC access token" | From-Excel wizard / Office Online | Use Track A (PnP) — Steps 2–3. |
| Dropdown has no Date/Number | Wizard read column as text | Fix type in List settings after import, or use Track A. |
| "long text" missing | It's named **Multiple lines of text** | Choose that option. |
| Card arrives but Arabic left-aligned | RTL container | Use the provided card JSON unchanged; it sets `rtl`. |
| Flow sends on a weekend | Trigger days | Set Recurrence to Mon–Fri; holidays skip via no matching row. |
| Row marked Sent but some users missed it | Loop error not caught | Ensure Step 7/8 success/failure branches from the flow guide. |
| Premium licence prompt | A premium connector slipped in | Use only SharePoint/Teams/Office 365 Groups (standard). |

---

## The essential order (TL;DR)

1. Pick Model A or B.  2. `Create-Lists.ps1`.  3. `Import-Data.ps1`.
4. Confirm group.  5. Build flow (matching guide).  6. Test with 2–3 users.
7. Turn On.  8. Monitor / reload monthly.
