# IT Handover — Wellbeing Nudges Automation

## Project overview

Automatically send **250 wellbeing nudges** to **50 users** via Microsoft Teams
notifications, **4 times per working day** at **07:00, 09:15, 11:30, 13:45
(UAE time)**. One nudge is sent per run to all users, so the list lasts roughly
**63 working days**.

> **Important:** This runs **entirely in the Microsoft 365 cloud**. **No PC or
> server needs to be left on.** The original concern about "a PC needs to be on"
> applies only to Power Automate *Desktop* (RPA) flows — this solution uses a
> *cloud* flow, which Microsoft runs on its own servers on schedule.

## Cost

**$0 beyond existing Microsoft 365 licences.** Every connector used
(SharePoint, Teams, Office 365 Groups, Recurrence) is a **standard** connector,
so **no premium Power Automate licence** is required.

## Components

| Component | Purpose |
|-----------|---------|
| SharePoint List `Nudges` | State store: the 250 nudges + Status/SentDateTime/RunID. Replaces the original Excel file (no file locks, concurrency-safe). |
| Microsoft 365 Group (e.g. `AH-Nudges`) | The 50 recipients. |
| Power Automate cloud flow | Scheduled trigger, picks next pending nudge, sends cards, updates status. |
| Adaptive Card (Teams Flow bot) | The notification users receive in a 1:1 Teams chat. |

## Files in this package

- `nudges.csv` — all 250 nudges, seeded to `Pending`.
- `sharepoint-list-schema.md` — how to create and load the `Nudges` list.
- `flow-build-guide.md` — step-by-step flow build (hardened logic).
- `adaptive-card.json` — the notification card.
- `scripts/gen_nudges.py` — regenerates `nudges.csv` if the wording changes.

## Setup (one time)

1. Create the SharePoint List `Nudges` (see `sharepoint-list-schema.md`) and
   load all 250 rows.
2. Create/confirm the M365 Group with the 50 users.
3. Build the cloud flow (see `flow-build-guide.md`).
4. Pilot with 2–3 test users, then switch to the full group and turn it **On**.

## What was hardened vs. the original design

| Original | Issue | Fix in this package |
|----------|-------|---------------------|
| Excel `tblNudges` as datastore | File locks / throttling → failed runs | SharePoint List (concurrency-safe) |
| `first()` on unordered rows | Could send nudges out of order | `Get items` ordered by `NudgeID asc`, top 1 |
| Status updated after loop, no error path | Partial failures marked as "Sent" | Success/failure branches; `Error` status + IT alert |
| `SentDateTime = utcNow()` | Logged in UTC, not UAE | `convertTimeZone(...,'Arabian Standard Time',...)` |
| 07:00–16:00 window check | Redundant with fixed schedule | Removed (or kept only as a gate for the 15-min pattern) |
| Unbounded send loop | Teams API throttling risk | `Apply to each` concurrency = 15 |

## Maintenance

- **Marketing** edits nudge wording directly in the SharePoint List (or asks IT
  to re-run `scripts/gen_nudges.py` and re-import).
- **IT** manages group membership and monitors flow run history.
- The flow needs **no manual intervention** to send — it runs on schedule.
- When all 250 are `Sent`, the flow terminates cleanly each run. To restart the
  cycle, bulk-reset `Status` to `Pending` (and clear `SentDateTime`/`RunID`).

## Best practices

- Don't change the flow unless the schedule, group, or content changes.
- Keep the SharePoint List accessible to the flow's connection account.
- Provide a support contact for users with notification issues.
- Check Power Automate **run history** periodically for failures (look for
  items marked `Error`).
