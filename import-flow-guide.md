# One-Off Import Flow — Load 250 Nudges into the SharePoint List

A small, **run-once** Power Automate cloud flow that reads `nudges.json` and
creates all 250 items in the `Nudges` SharePoint List — so nobody pastes rows by
hand. Standard connectors only, **$0**, no PC.

> **Why JSON, not CSV?** Power Automate has no reliable native CSV parser, and a
> few nudges contain commas (e.g. *"Breathe in calm, breathe out tension."*).
> The built-in **Parse JSON** action handles the text safely. Use `nudges.json`
> from this repo.

## Prerequisites

- The `Nudges` SharePoint List already exists with columns from
  `sharepoint-list-schema.md` (`NudgeID` number, `NudgeText` text,
  `Status` choice defaulting to `Pending`).
- `nudges.json` uploaded somewhere the flow can read it. Easiest: upload it to a
  **document library** on the same SharePoint site (e.g. `Shared Documents`).

## Build the flow

### Step 1 — Trigger

- Create an **Instant cloud flow** → **Manually trigger a flow**. (Run-once, so a
  manual trigger is ideal.)

### Step 2 — Get the JSON file content

Pick **one** source:

- **From SharePoint (recommended):** action **Get file content** (SharePoint) →
  Site + File = `/Shared Documents/nudges.json`.
- **Or skip the file entirely:** add a **Compose** action and paste the contents
  of `nudges.json` directly as its input. Then use `outputs('Compose')` wherever
  the guide says the file content. This avoids uploading anything.

### Step 3 — Parse JSON

- Action: **Parse JSON**.
- **Content:** the file content from Step 2
  (`body('Get_file_content')`) — or `outputs('Compose')` if you pasted it.
- **Schema:** paste this (it matches `nudges.json`):

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "NudgeID": { "type": "integer" },
      "NudgeText": { "type": "string" }
    },
    "required": [ "NudgeID", "NudgeText" ]
  }
}
```

### Step 4 — Create the 250 items

- Action: **Apply to each** over the **Body** output of Parse JSON.
  - **Concurrency Control = On, Degree = 8** (fast but stays under SharePoint
    throttling limits for a one-off run of 250).
- Inside, action: **Create item** (SharePoint) into the `Nudges` list:
  - `Title` = `item()?['NudgeID']` (or leave default if you use the built-in ID)
  - `NudgeID` = `item()?['NudgeID']`
  - `NudgeText` = `item()?['NudgeText']`
  - `Status` = `Pending`
  - Leave `SentDateTime` and `RunID` empty.

### Step 5 — Run once

1. **Save**, then **Test → Manually → Run flow**.
2. Wait for it to finish (250 create actions — usually well under a minute).
3. Open the `Nudges` list and confirm **250 items**, all `Pending`,
   `NudgeID` 1–250.

### Step 6 — Retire the import flow

- Once loaded, **turn the import flow Off** (or delete it). It's only needed
  again if you rebuild the list from scratch.

## Safety notes

- **Run it exactly once.** Running twice creates duplicates. If that happens,
  delete all items (list → select all → delete) and re-run once.
- To reload after content changes: clear the list, regenerate `nudges.json`
  (`python3 scripts/gen_nudges.py`), re-upload, and run the import once more.
- This flow only **seeds** data. Day-to-day sending is handled by the separate
  scheduled flow in `flow-build-guide.md`.
