# Power Automate Cloud Flow — Build Guide (Free / No PC)

This builds the Wellbeing Nudges automation using **only standard connectors**
that are **included in Microsoft 365** — no premium licence, no Azure, and
**no computer needs to be left on**. Cloud flows run on Microsoft's servers.

> You can build this either from **Power Automate** (`make.powerautomate.com`)
> or from **Teams → Workflows** — they are the same engine. Steps below use
> Power Automate.

## Architecture at a glance

```
Recurrence (4x/day, UAE time)
  → Get items where Status = Pending, ordered by NudgeID, top 1
  → If none: Terminate (all 250 sent)
  → Get M365 group members (the 50 users)
  → For each member (concurrency 15): Post Adaptive Card as Flow bot in 1:1 chat
  → On success: Update the SharePoint item → Status=Sent, SentDateTime, RunID
  → On failure: Update item → Status=Error and notify IT
```

**One nudge per run → 4 nudges/day → 250 nudges ≈ 63 working days.**

---

## Prerequisites

- SharePoint List `Nudges` created and loaded with 250 rows (see
  `sharepoint-list-schema.md`).
- An M365 Group containing the 50 recipients (e.g. `AH-Nudges`).
- Permission to post Adaptive Cards via the Flow bot (default in most tenants).

---

## Step 1 — Trigger: Recurrence

- Add trigger **Recurrence**.
- Frequency: **Day**, Interval **1**.
- **Time zone:** `(UTC+04:00) Abu Dhabi, Muscat`.
- **At these hours/minutes** — set four schedules. The cleanest way is one
  Recurrence with these start times, or split into explicit trigger times:
  - 07:00, 09:15, 11:30, 13:45.
  - If your Recurrence UI only allows whole hours + minutes lists, create the
    flow with 4 separate Recurrence triggers is **not** possible in one flow;
    instead either (a) use 4 copies of the flow, or (b) run every 15 min and
    gate with a condition, or **(recommended)** use the schedule below.

> **Recommended schedule setup:** Frequency = Day, and add the specific times
> under advanced options if available. If not, the simplest robust pattern is:
> Recurrence **every 15 minutes** + a **Condition** that only proceeds when the
> current UAE time is exactly one of the four slots. See Step 2.

## Step 2 — (If gating) Time check

Only needed if you used the "every 15 min" pattern. Otherwise the redundant
07:00–16:00 window check from the original doc can be **removed** — the fixed
schedule already guarantees the window.

- Add **Compose** `nowUAE`:
  ```
  convertTimeZone(utcNow(), 'UTC', 'Arabian Standard Time', 'HH:mm')
  ```
- Add **Condition**: `nowUAE` is one of `07:00, 09:15, 11:30, 13:45`
  (use an `or` of four equals, or a `contains` against an array).
- If not a slot → **Terminate** (Succeeded).

## Step 3 — Get the next pending nudge (deterministic order)

- Action: **Get items** (SharePoint).
- Site + List = `Nudges`.
- **Filter Query:** `Status eq 'Pending'`
- **Order By:** `NudgeID asc`
- **Top Count:** `1`

This replaces the fragile `first()` on an unordered Excel result. Ordering by
`NudgeID asc` guarantees you always send the lowest-numbered pending nudge.

## Step 4 — If none left, stop

- Add **Condition:** `length(body('Get_items')?['value'])` is equal to `0`.
  - **If yes** → **Terminate** (Succeeded) — all nudges sent.
  - **If no** → continue.
- Add **Compose** `Nudge` = `first(body('Get_items')?['value'])`.
  - `NudgeText` = `outputs('Nudge')?['NudgeText']`
  - `NudgeID`   = `outputs('Nudge')?['NudgeID']`
  - `ItemId`    = `outputs('Nudge')?['ID']`

## Step 5 — Get the 50 recipients

- Action: **List group members** (Office 365 Groups) — standard connector.
- Group Id = your `AH-Nudges` group.
- (Optional) Filter out disabled/guest accounts in the next step.

## Step 6 — Send the Adaptive Card to each user

- Action: **Apply to each** over `value` from List group members.
  - Set **Concurrency Control = On, Degree = 15** (avoids Teams throttling; not
    unbounded).
- Inside, action: **Post card in a chat or channel** (Microsoft Teams).
  - **Post as:** `Flow bot`
  - **Post in:** `Chat with Flow bot` → **Recipient:** `items('Apply_to_each')?['mail']`
  - **Adaptive Card:** paste `adaptive-card.json`, but replace the two tokens
    with dynamic values:
    - `${NudgeText}` → `outputs('Nudge')?['NudgeText']`
    - `${NudgeID}`   → `outputs('Nudge')?['NudgeID']`
- **Error handling:** wrap this send in a **Scope** named `SendScope`.

> Note on "popup": this produces a Teams chat message + activity-feed
> notification badge. Teams does not support a forced modal popup from a bot —
> this is the expected, supported behaviour.

## Step 7 — Mark the nudge Sent (only on success)

- After `Apply to each`, add action **Update item** (SharePoint), configured to
  run only if the loop scope **succeeded** (`Configure run after`).
  - `Status` = `Sent`
  - `SentDateTime` = `convertTimeZone(utcNow(),'UTC','Arabian Standard Time','yyyy-MM-dd HH:mm')`
  - `RunID` = `workflow()?['run']?['name']`

## Step 8 — Handle failures (don't silently lose a nudge)

- Add a parallel **Update item** configured (via `Configure run after`) to run
  when the send scope **has failed / timed out**:
  - `Status` = `Error`
  - `RunID`  = `workflow()?['run']?['name']`
- Add an optional **Post message in a chat** to your IT support user/channel
  with the failed `NudgeID` and run name.

This means a partly-failed run is visible and re-sendable, rather than being
marked `Sent` when 20 of 50 users missed it.

## Step 9 — Save, test, deploy

1. **Test → Manually** once. Confirm one card arrives and the item flips to
   `Sent` with a UAE timestamp + RunID.
2. Pilot with a small group first (point the flow at a 2–3 person test group).
3. Switch to the real 50-user group and turn the flow **On**.

---

## Cost & licensing summary

| Component            | Licence                         | Extra cost |
|----------------------|---------------------------------|-----------|
| Power Automate cloud flow (standard connectors) | Included in M365 | **$0** |
| SharePoint List      | Included in M365                | **$0** |
| Teams Flow-bot cards | Included in M365                | **$0** |
| Office 365 Groups    | Included in M365                | **$0** |
| Compute / server / PC| None — runs in Microsoft cloud  | **$0** |

No premium Power Automate licence is required because every connector used is
**standard**.
