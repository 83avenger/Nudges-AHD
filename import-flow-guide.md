# One-Off Import Flow — Load the 21 Challenges into SharePoint

A **run-once** cloud flow that reads `data/month-of-connection.json` and creates
the 21 challenge items in the `MonthOfConnection` SharePoint List — so nobody
retypes bilingual rows by hand. Standard connectors only, **$0**, no PC.

> **Why JSON?** Power Automate has no reliable native CSV parser, and the rows
> contain commas, Arabic text, and emoji. **Parse JSON** handles all of it
> safely. Use `data/month-of-connection.json`.

## Prerequisites

- The `MonthOfConnection` list exists with the columns in
  `sharepoint-list-schema.md` (note `RevealDate` is a **Date only** column,
  `Status` a Choice defaulting to `Scheduled`).
- `month-of-connection.json` available to the flow. Easiest: upload it to a
  document library on the site (e.g. `Shared Documents`), **or** paste its
  contents into a Compose action (Step 2 option B).

## Build the flow

### Step 1 — Trigger
- **Instant cloud flow** → **Manually trigger a flow**.

### Step 2 — Get the JSON
- **Option A (file):** **Get file content** (SharePoint) → `month-of-connection.json`.
- **Option B (no upload):** add a **Compose**, paste the file contents, and use
  `outputs('Compose')` below.

### Step 3 — Parse JSON
- Action: **Parse JSON**.
- **Content:** the file content (`body('Get_file_content')`) or `outputs('Compose')`.
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
      "ChallengeEN": { "type": "string" },
      "ChallengeAR": { "type": "string" },
      "WhyItMatters": { "type": "string" },
      "TomorrowTeaser": { "type": "string" },
      "SocialCaption": { "type": "string" },
      "SourceRef": { "type": "string" },
      "Status": { "type": "string" },
      "SentDateTime": { "type": "string" },
      "RunID": { "type": "string" }
    },
    "required": [ "Day", "RevealDate", "ChallengeEN", "ChallengeAR" ]
  }
}
```

### Step 4 — Create the 21 items
- **Apply to each** over the **Body** of Parse JSON (Concurrency **On, Degree 8**).
- Inside: **Create item** (SharePoint) into `MonthOfConnection`:
  - `Title` = `item()?['Day']`
  - `Day` = `item()?['Day']`
  - `RevealDate` = `item()?['RevealDate']`  *(the `yyyy-MM-dd` string maps to the Date column)*
  - `DateLabel` = `item()?['DateLabel']`
  - `Weekday` = `item()?['Weekday']`
  - `WeekArc` = `item()?['WeekArc']`
  - `ChallengeEN` = `item()?['ChallengeEN']`
  - `ChallengeAR` = `item()?['ChallengeAR']`
  - `WhyItMatters` = `item()?['WhyItMatters']`
  - `TomorrowTeaser` = `item()?['TomorrowTeaser']`
  - `SocialCaption` = `item()?['SocialCaption']`
  - `SourceRef` = `item()?['SourceRef']`
  - `Status` = `Scheduled`
  - Leave `SentDateTime` and `RunID` empty.

### Step 5 — Run once & verify
1. **Save → Test → Manually → Run flow.**
2. Open the list: confirm **21 items**, `RevealDate` 2026-08-03 → 2026-08-31,
   all `Scheduled`, and the **Arabic text renders correctly** (RTL).

### Step 6 — Retire
- Turn the import flow **Off** (or delete). Only needed again if you rebuild the
  list.

## Safety notes

- **Run exactly once** — a second run creates duplicates. If it happens, delete
  all items and re-run once.
- To reload after content edits: clear the list, regenerate the data
  (`python3 scripts/extract_pilot.py source/AHD_...August2026.xlsx`), re-upload,
  run once.
- This flow only **seeds** data. Daily sending is the separate reveal flow in
  `flow-build-guide.md`.
