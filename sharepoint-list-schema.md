# SharePoint List Schema — `Nudges`

Create a SharePoint List (in the team site of your choice) named **`Nudges`**.
This replaces the Excel `tblNudges` table — it is concurrency-safe, has no file
locks, and is free with your existing Microsoft 365 licence.

## Columns

| Display name    | Internal type            | Notes |
|-----------------|--------------------------|-------|
| `Title`         | Single line of text      | Default column. You may rename it to `NudgeID` display, but keep the internal name `Title`. Store the numeric NudgeID here as text, or use the built-in **ID** column instead (see below). |
| `NudgeID`       | Number                   | 1–250. The stable ordering key. |
| `NudgeText`     | Multiple lines of text (plain) | The full nudge message. |
| `Status`        | Choice                   | Choices: `Pending`, `Sent`, `Error`. Default = `Pending`. |
| `SentDateTime`  | Single line of text      | Stored as UAE local time string `yyyy-MM-dd HH:mm`. (Text avoids timezone reinterpretation by SharePoint.) |
| `RunID`         | Single line of text      | Power Automate run name for traceability. |

> Tip: You can ignore the auto `ID` column and use your own `NudgeID` number
> column for ordering — this keeps IDs stable even if rows are deleted/re-added.

## Loading the 250 rows

1. Open the list → **Edit in grid view**.
2. Open `nudges.csv` (in this repo), copy the `NudgeText` column, paste into the
   grid. Set `NudgeID` 1–250 and `Status = Pending` for all.
   - Alternatively, use the **"Import from CSV"** option or a one-off Power
     Automate flow that reads the CSV and creates items.
3. Leave `SentDateTime` and `RunID` empty.

## Why SharePoint List over Excel

- No file-lock / "file in use" failures when the flow writes back.
- Handles concurrent reads/writes safely.
- Cleaner filtering (`Status eq 'Pending'`) and reliable ordering by `NudgeID`.
- Better run history and permissions.
- Same $0 cost — included in Microsoft 365.
