# SharePoint List Schema — `MonthOfConnection`

Create a SharePoint List named **`MonthOfConnection`** to hold the 21 bilingual
daily challenges. It is the state store for the reveal flow — concurrency-safe,
no file locks, and free with your existing Microsoft 365 licence.

Data source: `data/month-of-connection.json` / `.csv`, extracted directly from
the workbook (`August Connection – 21 Days`) so every row stays traceable to
Dr. Dania's Social Wellbeing library via `SourceRef`.

## Columns

| Display name      | Internal type                 | Notes |
|-------------------|-------------------------------|-------|
| `Title`           | Single line of text           | Default column. Store the `Day` number here (e.g. `1`), or ignore it. |
| `Day`             | Number                        | 1–21. |
| `RevealDate`      | **Date only**                 | The working day this challenge is revealed (e.g. `2026-08-03`). **This is the matching key** the flow uses each morning. |
| `DateLabel`       | Single line of text           | Human label, e.g. `3 Aug`. |
| `Weekday`         | Single line of text           | `Mon`…`Fri`. |
| `WeekArc`         | Single line of text           | e.g. `W1 · I See You`, `FINALE · We Are Connected`. |
| `ChallengeEN`     | Multiple lines of text (plain)| English challenge (action title + instruction). |
| `ChallengeAR`     | Multiple lines of text (plain)| Arabic challenge. **Keep RTL text intact** — SharePoint stores it fine; the card renders it right-to-left. |
| `WhyItMatters`    | Multiple lines of text (plain)| The 60-second huddle line. |
| `TomorrowTeaser`  | Multiple lines of text (plain)| Teaser shown on the card. |
| `SocialCaption`   | Multiple lines of text (plain)| Approved WhatsApp / social caption (public-safe). |
| `SourceRef`       | Single line of text           | Trace back to the source library (e.g. `#41`, `finale`). |
| `Status`          | Choice                        | `Scheduled`, `Sent`, `Error`. Default = `Scheduled`. |
| `SentDateTime`    | Single line of text           | UAE local time string `yyyy-MM-dd HH:mm`. |
| `RunID`           | Single line of text           | Power Automate run name for traceability. |

> **Why a real `Date` column for `RevealDate`?** The pilot is a fixed calendar
> (Mon 3 Aug → Mon 31 Aug, working days only). Matching on the date means a
> missed or re-run day never shifts the whole schedule — each challenge fires on
> its own day or not at all.

## Loading the 21 rows

Use the run-once import flow in `import-flow-guide.md` (reads
`data/month-of-connection.json`), or paste from `data/month-of-connection.csv`
via **Edit in grid view**. Leave `SentDateTime` and `RunID` empty; `Status`
starts as `Scheduled`.

## Bilingual note

The Arabic (`ChallengeAR`) is a hard requirement and is already populated for all
21 days. The Adaptive Card renders it in a right-to-left container beneath the
English, so every recipient gets both languages on one card.
