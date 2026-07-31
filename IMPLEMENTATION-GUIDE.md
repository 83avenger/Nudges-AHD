# Implementation Guide — End to End

From zero to a live, automated, bilingual **4-nudges-per-day** program.

- **4 nudges/day**, one per pillar: **07:00 Social · 09:15 Physical · 11:30
  Financial · 13:45 Mental** (UAE), on **AHD working days (Sun–Thu)**.
- **No PC left on** · **$0 beyond existing M365** · standard connectors only.
- First-time build: **~75–90 minutes**.

Prefer all-clicks (no PowerShell)? See `IMPLEMENTATION-GUIDE-GUI.md`.

---

## Step 1 · Prerequisites (10 min)

- [ ] Microsoft 365 with **Teams, SharePoint, Power Automate** (standard).
- [ ] A **SharePoint site** for the list; rights to create a list on it.
- [ ] A **Microsoft 365 Group / Teams team** of recipients (e.g. `AH-Nudges`) —
      start with 2–3 test users. Note its name/ID.
- [ ] PnP module: `Install-Module PnP.PowerShell -Scope CurrentUser`.
- [ ] This repo cloned/downloaded locally.

**Checkpoint:** you can open PowerShell and your SharePoint site.

---

## Step 2 · Create the list + load the 84 rows (10 min)

```powershell
cd provisioning
./Create-List.ps1 -SiteUrl "https://<tenant>.sharepoint.com/sites/<YourSite>"
./Import-Data.ps1 -SiteUrl "https://<tenant>.sharepoint.com/sites/<YourSite>"
```

`Create-List.ps1` builds `FourPillarNudges` with exact column types
(Date-only, Number, Choice, Multiple-lines, `Status` default `Scheduled`).
`Import-Data.ps1` loads all 84 rows — no WAC, no Power Automate, Arabic preserved.

*No PowerShell?* Use `provisioning/README.md` Route A (From Excel with
`data/four-pillars/by-nudge.xlsx`) or the GUI guide.

**Checkpoint:** the list shows **84 items**, all `Status = Scheduled`, four
`Pillar` values, Arabic right-to-left.

---

## Step 3 · Confirm the recipient group (5 min)

- Confirm the pilot members are in the M365 Group / Teams team; copy its **ID**.
- Keep it to 2–3 test users for the first live test, then expand.

---

## Step 4 · Build the four reveal flows (30–40 min)

Open `make.powerautomate.com` (or Teams → Workflows) and follow
`four-pillars-flow-guide.md`. Build **one** flow, confirm it, then **Save As**
three times changing only the **time** and the **pillar**:

| Flow | Time (UAE) | Pillar filter |
|------|-----------|---------------|
| Social 07:00 | 07:00 | `Pillar eq 'Social'` |
| Physical 09:15 | 09:15 | `Pillar eq 'Physical'` |
| Financial 11:30 | 11:30 | `Pillar eq 'Financial'` |
| Mental 13:45 | 13:45 | `Pillar eq 'Mental'` |

Each flow (per the guide):
1. **Recurrence** — Time zone **(UTC+04:00) Abu Dhabi, Muscat**, **Sun–Thu**, at
   the slot time.
2. **Get items** where `Pillar eq '<pillar>' and Status eq 'Scheduled'`, **Order
   By `Day asc`, Top 1** — the next unsent nudge for that pillar.
3. **Condition** — if none, **Terminate**.
4. **List group members** → **Apply to each** (concurrency 15) → **Post card in a
   chat or channel** as **Flow bot** to `member mail`. Paste
   `adaptive-card-pillar.json` and map the `${...}` tokens (table in the guide).
5. On success → **Update item** `Status=Sent`, UAE `SentDateTime`, `RunID`;
   on failure → `Status=Error` + optional IT alert.

> One-flow alternative (15-min gate) is in the guide if you'd rather maintain a
> single flow.

**Checkpoint:** all four flows save without errors.

---

## Step 5 · Test with 2–3 users (10 min)

1. Point the flows at your **test group**.
2. **Test → Manually → Run** one flow — it sends that pillar's Day 1 nudge.
3. Confirm the **bilingual card** arrives (EN + RTL Arabic, pillar badge, day
   counter) and the row flips to **Sent** with UAE timestamp + RunID.
4. Reset that row's `Status` to `Scheduled` so the real run starts at Day 1.

---

## Step 6 · Go live (5 min)

1. Point the flows at the **real pilot group**; all rows `Scheduled`.
2. Turn **all four** flows **On** on your intended start day (a Sunday works well).

---

## Step 7 · Monitor & maintain (ongoing)

- **Power Automate → each flow → Run history**: watch for failures; reset any
  `Error` row to `Scheduled` to re-send.
- **Content edits:** the wellbeing team edits wording in the list, or re-run
  `python3 scripts/gen_four_pillars.py` and reload
  (`./provisioning/Import-Data.ps1 -SiteUrl "..." -Fresh`).
- **Group membership:** IT manages who's in the recipient group.
- **September gate (1–3 Sep):** review metrics in `IT-handover.md`, then load
  next month's rows — no flow rebuild needed.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| "Column 'Pillar' does not exist" in Get items | Filter/Order By use **internal** names. Replace the `PILLAR` placeholder with the real value (`'Social'` …); if it persists, the column's internal name differs (From-Excel can make `Pillar0`) — check List settings → column → URL `Field=`, re-select the list to refresh schema, or recreate with `Create-List.ps1`. Same for `Day`. |
| "Could not obtain a WAC access token" | From-Excel wizard problem. Use Step 2 (PnP) — it doesn't touch WAC. |
| No Date/Number option in From-Excel | Set type after import in List settings, or use PnP (exact types up front). |
| "long text" missing | It's **Multiple lines of text**. |
| Card arrives but Arabic left-aligned | Use `adaptive-card-pillar.json` unchanged (it sets `rtl`). |
| Flow sends on the weekend | Set Recurrence to **Sun–Thu**; pause the flow on public holidays. |
| Row marked Sent but some users missed it | Ensure the success/failure branches from the flow guide. |
| Premium licence prompt | Use only SharePoint/Teams/Office 365 Groups (standard). |

---

## TL;DR
1. `Create-List.ps1` + `Import-Data.ps1`.  2. Confirm group.
3. Build 4 flows (Save-As ×3).  4. Test with 2–3 users.  5. Turn all 4 On.
6. Monitor / reload monthly.
