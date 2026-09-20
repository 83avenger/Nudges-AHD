# One-Off Import Flow — Load the 84 Nudges into SharePoint

A **run-once** Power Automate flow that reads `data/four-pillars/by-nudge.json`
and creates the 84 nudge items in `FourPillarNudges` — a **GUI loader** if you
can't run PowerShell. Standard connectors only, **$0**, no PC.

> Easier options exist: **`provisioning/Import-Data.ps1`** (PnP, two commands) or
> **From Excel** with `by-nudge.xlsx`. Use this flow only if you want an all-GUI
> loader without PnP. See `provisioning/README.md`.

> **Why JSON?** Power Automate has no reliable native CSV parser, and the rows
> contain commas, Arabic and emoji. **Parse JSON** handles all of it safely.

## Prerequisites

- The `FourPillarNudges` list exists (see `four-pillars-sharepoint-schema.md` /
  `provisioning/`): `RevealDate` = **Date only**, `Status`/`Pillar` = **Choice**.
- `by-nudge.json` available to the flow — upload it to a document library, **or**
  paste its contents into a Compose action (Step 2, Option B).

## Build the flow

### Step 1 — Trigger
- **Instant cloud flow** → **Manually trigger a flow**.

### Step 2 — Get the JSON
- **Option A (file):** **Get file content** (SharePoint) → `by-nudge.json`.
- **Option B (no upload):** add a **Compose**, paste the file contents, use
  `outputs('Compose')` below.

### Step 3 — Parse JSON
- Action: **Parse JSON**. **Content:** the file content (or `outputs('Compose')`).
- **Schema:**

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Day": { "type": "integer" },
      "RevealDate": { "type": "string" },
      "DateLabel": { "type": "string" },
      "Weekday": { "type": "string" },
      "WeekArc": { "type": "string" },
      "DailyThemeEN": { "type": "string" },
      "DailyThemeAR": { "type": "string" },
      "Pillar": { "type": "string" },
      "PillarEN": { "type": "string" },
      "PillarAR": { "type": "string" },
      "PillarEmoji": { "type": "string" },
      "PillarOrder": { "type": "integer" },
      "SlotTime": { "type": "string" },
      "NudgeEN": { "type": "string" },
      "NudgeAR": { "type": "string" },
      "SourceRef": { "type": "string" },
      "Status": { "type": "string" },
      "SentDateTime": { "type": "string" },
      "RunID": { "type": "string" }
    },
    "required": [ "Day", "Pillar", "NudgeEN", "NudgeAR" ]
  }
}
```

### Step 4 — Create the 84 items
- **Apply to each** over the **Body** of Parse JSON (Concurrency **On, Degree 8**).
- Inside: **Create item** (SharePoint) into `FourPillarNudges`, mapping each
  field: `Title` = `concat(item()?['Day'],'-',item()?['Pillar'])`, then `Day`,
  `RevealDate`, `DateLabel`, `Weekday`, `WeekArc`, `DailyThemeEN`, `DailyThemeAR`,
  `Pillar`, `PillarEN`, `PillarAR`, `PillarEmoji`, `PillarOrder`, `SlotTime`,
  `NudgeEN`, `NudgeAR`, `SourceRef` = the matching `item()?['<field>']`;
  `Status` = `Scheduled`; leave `SentDateTime` / `RunID` empty.

### Step 5 — Run once & verify
1. **Save → Test → Manually → Run flow.**
2. Confirm **84 items**, all `Scheduled`, four `Pillar` values present, Arabic RTL.

### Step 6 — Retire
- Turn the import flow **Off** (or delete). Only needed if you rebuild the list.

## Safety notes

- **Run exactly once** — a second run duplicates. If it happens, delete all items
  and re-run once (or use `Import-Data.ps1 -Fresh`).
- To reload after content edits: regenerate (`python3 scripts/gen_four_pillars.py`),
  re-upload, run once.
- This flow only **seeds** data. Daily sending is `four-pillars-flow-guide.md`.
