# Power Automate Cloud Flow — Daily Reveal (Bilingual, Free / No PC)

Sends the **Month of Connection** daily challenge — **English + Arabic on one
card** — to the pilot group each working morning. Standard connectors only,
**included in Microsoft 365** (no premium licence, no Azure, **no PC left on** —
cloud flows run on Microsoft's servers).

> Build it from **Power Automate** (`make.powerautomate.com`) or from
> **Teams → Workflows** — same engine. Steps below use Power Automate.

## What it does each morning

```
Recurrence: working days at 08:00 UAE  (matches the card's "REVEAL 8:00 AM")
  → Compute today's date in UAE
  → Get the MonthOfConnection item WHERE RevealDate = today AND Status = Scheduled
  → If none (weekend / holiday / pilot over): Terminate
  → Get the pilot group's members
  → For each member (concurrency 15): Post bilingual Adaptive Card as Flow bot
  → On success: item → Status=Sent, SentDateTime (UAE), RunID
  → On failure: item → Status=Error + notify IT
```

**One challenge per working day → 21 days → Mon 3 Aug to Mon 31 Aug 2026.**

Matching on `RevealDate` (not a "next pending" queue) means each challenge fires
on its own calendar day. A missed or re-run day never shifts the rest.

---

## Prerequisites

- SharePoint List `MonthOfConnection` created and loaded with the 21 rows
  (see `sharepoint-list-schema.md` + `import-flow-guide.md`).
- An M365 Group / Teams team containing the pilot recipients.
- Permission to post Adaptive Cards via the Flow bot (default in most tenants).

---

## Step 1 — Trigger: Recurrence on working days

- Add trigger **Recurrence**.
- Frequency: **Week**, Interval **1**.
- **On these days:** Monday, Tuesday, Wednesday, Thursday, Friday.
- **At these hours:** `8`  · **At these minutes:** `0`.
- **Time zone:** `(UTC+04:00) Abu Dhabi, Muscat`.

This fires at 08:00 UAE Mon–Fri. Weekends never run. (Public holidays that fall
on a weekday are handled automatically in Step 3 — there's simply no row whose
`RevealDate` equals that day, so the flow terminates.)

## Step 2 — Compute today's UAE date

- Add **Compose** `TodayUAE`:
  ```
  convertTimeZone(utcNow(), 'UTC', 'Arabian Standard Time', 'yyyy-MM-dd')
  ```

## Step 3 — Get today's challenge

- Action: **Get items** (SharePoint) on `MonthOfConnection`.
- **Filter Query:**
  ```
  RevealDate eq '@{outputs('TodayUAE')}' and Status eq 'Scheduled'
  ```
  (SharePoint date columns compare on the `yyyy-MM-dd` value. If your tenant is
  fussy about date filtering, filter only on `Status eq 'Scheduled'`, order by
  `RevealDate asc`, `Top 1`, then verify the returned `RevealDate` equals
  `TodayUAE` in the next condition.)
- **Top Count:** `1`.

## Step 4 — Stop if nothing scheduled for today

- **Condition:** `length(body('Get_items')?['value'])` is equal to `0`.
  - **If yes** → **Terminate** (Succeeded). Weekend, holiday, or pilot finished.
  - **If no** → continue.
- **Compose** `Challenge` = `first(body('Get_items')?['value'])`. Reference
  fields as `outputs('Challenge')?['ChallengeEN']`,
  `outputs('Challenge')?['ChallengeAR']`, etc., and the item id as
  `outputs('Challenge')?['ID']`.

## Step 5 — Get the pilot recipients

- Action: **List group members** (Office 365 Groups) — standard connector.
- Group Id = your pilot group (e.g. `AH-Nudges` / the Month of Connection team).
- Optionally filter out disabled/guest accounts next.

## Step 6 — Send the bilingual card to each member

- **Apply to each** over `value` from List group members.
  - **Concurrency Control = On, Degree = 15** (avoids Teams throttling).
- Inside: **Post card in a chat or channel** (Microsoft Teams).
  - **Post as:** `Flow bot`
  - **Post in:** `Chat with Flow bot` → **Recipient:**
    `items('Apply_to_each')?['mail']`
  - **Adaptive Card:** paste `adaptive-card-bilingual.json`, then bind the
    tokens to the challenge fields:
    | Card token | Bind to |
    |------------|---------|
    | `${Day}` | `outputs('Challenge')?['Day']` |
    | `${WeekArc}` | `outputs('Challenge')?['WeekArc']` |
    | `${ChallengeEN}` | `outputs('Challenge')?['ChallengeEN']` |
    | `${ChallengeAR}` | `outputs('Challenge')?['ChallengeAR']` |
    | `${WhyItMatters}` | `outputs('Challenge')?['WhyItMatters']` |
    | `${TomorrowTeaser}` | `outputs('Challenge')?['TomorrowTeaser']` |
  - Wrap this send in a **Scope** named `SendScope` for error handling.

> The card shows **English and Arabic together** — English block, then a
> right-to-left Arabic block, then the huddle line and tomorrow's teaser. Arabic
> renders RTL automatically via the card's `rtl` container.
>
> **"Popup" note:** this is a Teams chat message + activity-feed notification,
> not a forced modal — the expected, supported behaviour for a bot.

## Step 7 — Mark Sent (only on success)

- After the loop, **Update item** (SharePoint), set to run only if `SendScope`
  **succeeded** (`Configure run after`):
  - `Status` = `Sent`
  - `SentDateTime` = `convertTimeZone(utcNow(),'UTC','Arabian Standard Time','yyyy-MM-dd HH:mm')`
  - `RunID` = `workflow()?['run']?['name']`

## Step 8 — Handle failures

- A parallel **Update item** set (via `Configure run after`) to run when
  `SendScope` **failed / timed out**:
  - `Status` = `Error`, `RunID` = `workflow()?['run']?['name']`.
- Optional **Post message** to IT/Champions with the failed `Day` + run name so
  the day can be re-sent.

## Step 9 — Save, test, deploy

1. **Test → Manually** once (temporarily relax the Step 3 filter to any
   `Scheduled` row). Confirm the bilingual card arrives and the item flips to
   `Sent` with a UAE timestamp + RunID.
2. Pilot with 2–3 test users first.
3. Point at the real pilot group and turn the flow **On** before Mon 3 Aug.

---

## Optional companion flows (nice-to-have, all free)

- **Thursday "Guess tomorrow's challenge" poll** — a second Recurrence flow
  (Thursdays) posting a Teams Adaptive Card / Forms poll (from the metrics tab).
- **Sunday Champion preview** — a flow that emails Champions the upcoming week's
  rows under embargo.
- **Weekly pulse** — a Friday flow posting the one-question pulse to the channel.

These aren't required for the core reveal; add them if you want the full
anticipation + measurement loop from the workbook's *Pilot Design & Metrics*.

---

## Cost & licensing summary

| Component | Licence | Extra cost |
|-----------|---------|-----------|
| Power Automate cloud flow (standard connectors) | Included in M365 | **$0** |
| SharePoint List | Included in M365 | **$0** |
| Teams Flow-bot cards | Included in M365 | **$0** |
| Office 365 Groups | Included in M365 | **$0** |
| Compute / server / PC | None — Microsoft cloud | **$0** |

No premium Power Automate licence is required — every connector used is
**standard**.
