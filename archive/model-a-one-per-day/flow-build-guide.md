# Power Automate Cloud Flow — Daily Reveal (Bilingual, Free / No PC)

Sends the **Month of Connection** daily challenge — **English + Arabic on one
card** — to the pilot group each working morning. Standard connectors only,
**included in Microsoft 365** (no premium licence, no Azure, **no PC left on** —
cloud flows run on Microsoft's servers).

> Build it from **Power Automate** (`make.powerautomate.com`) or from
> **Teams → Workflows** — same engine. Steps below use Power Automate.

## What it does each morning

```
Recurrence: AHD working days (Sun–Thu) at 08:00 UAE  ("REVEAL 8:00 AM")
  → Get the next MonthOfConnection item WHERE Status = Scheduled, ordered by Day (top 1)
  → If none (pilot finished): Terminate
  → Get the pilot group's members
  → For each member (concurrency 15): Post bilingual Adaptive Card as Flow bot
  → On success: item → Status=Sent, SentDateTime (UAE), RunID
  → On failure: item → Status=Error + notify IT
```

**One challenge per working day → 21 challenges → ~4 AHD working weeks.**

> **AHD works Sunday–Thursday** (weekend Fri–Sat). The flow fires only on those
> days and sends the **next unsent challenge in `Day` order**, so it never
> depends on the specific calendar dates in the workbook (which were laid out on
> a Mon–Fri calendar). **Nothing in the list needs to change** — the `RevealDate`
> column simply becomes informational. If a day is skipped (holiday, pause), the
> next working day just picks up the next challenge — the sequence self-heals.

---

## Prerequisites

- SharePoint List `MonthOfConnection` created and loaded with the 21 rows
  (see `sharepoint-list-schema.md` + `import-flow-guide.md`).
- An M365 Group / Teams team containing the pilot recipients.
- Permission to post Adaptive Cards via the Flow bot (default in most tenants).

---

## Step 1 — Trigger: Recurrence on AHD working days (Sun–Thu)

- Add trigger **Recurrence**.
- Frequency: **Week**, Interval **1**.
- **On these days:** **Sunday, Monday, Tuesday, Wednesday, Thursday**
  (AHD weekend is Fri–Sat — leave those unchecked).
- **At these hours:** `8`  · **At these minutes:** `0`.
- **Time zone:** `(UTC+04:00) Abu Dhabi, Muscat`.

This fires at 08:00 UAE Sun–Thu. The Fri–Sat weekend never runs. On a public
holiday you can either pause the flow that day or add an optional holiday check
(see note at the end).

## Step 2 — Get the next challenge (by Day order)

- Action: **Get items** (SharePoint) on `MonthOfConnection`.
- **Filter Query:** `Status eq 'Scheduled'`
- **Order By:** `Day asc`
- **Top Count:** `1`.

This always returns the lowest-numbered unsent challenge, so the sequence
advances one per working day regardless of the calendar. No date matching, so the
workbook's Mon–Fri `RevealDate` values don't matter.

## Step 3 — Stop if nothing left

- **Condition:** `length(body('Get_items')?['value'])` is equal to `0`.
  - **If yes** → **Terminate** (Succeeded). All 21 challenges sent.
  - **If no** → continue.
- **Compose** `Challenge` = `first(body('Get_items')?['value'])`. Reference
  fields as `outputs('Challenge')?['ChallengeEN']`,
  `outputs('Challenge')?['ChallengeAR']`, etc., and the item id as
  `outputs('Challenge')?['ID']`.

## Step 4 — Get the pilot recipients

- Action: **List group members** (Office 365 Groups) — standard connector.
- Group Id = your pilot group (e.g. `AH-Nudges` / the Month of Connection team).
- Optionally filter out disabled/guest accounts next.

## Step 5 — Send the bilingual card to each member

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

## Step 6 — Mark Sent (only on success)

- After the loop, **Update item** (SharePoint), set to run only if `SendScope`
  **succeeded** (`Configure run after`):
  - `Status` = `Sent`
  - `SentDateTime` = `convertTimeZone(utcNow(),'UTC','Arabian Standard Time','yyyy-MM-dd HH:mm')`
  - `RunID` = `workflow()?['run']?['name']`

## Step 7 — Handle failures

- A parallel **Update item** set (via `Configure run after`) to run when
  `SendScope` **failed / timed out**:
  - `Status` = `Error`, `RunID` = `workflow()?['run']?['name']`.
- Optional **Post message** to IT/Champions with the failed `Day` + run name so
  the day can be re-sent.

## Step 8 — Save, test, deploy

1. **Test → Manually** once. Confirm the bilingual card arrives and the item
   flips to `Sent` with a UAE timestamp + RunID (it will send Day 1 first).
2. Pilot with 2–3 test users first. (Reset the sent row's `Status` to
   `Scheduled` afterwards so the real run starts from Day 1.)
3. Point at the real pilot group and turn the flow **On** on the intended start
   day (a Sunday works well as the week opener).

---

## Optional companion flows (nice-to-have, all free)

- **Mid-week "Guess tomorrow's challenge" poll** — a second Recurrence flow
  (e.g. Wednesday) posting a Teams Adaptive Card / Forms poll (from the metrics tab).
- **Champion preview** — a flow that emails Champions the upcoming week's rows
  under embargo the day before the week opens (e.g. Saturday, ahead of Sunday).
- **Weekly pulse** — a flow on the **last working day (Thursday)** posting the
  one-question pulse to the channel.

These aren't required for the core reveal; add them if you want the full
anticipation + measurement loop from the workbook's *Pilot Design & Metrics*.
Adjust the days to your team's rhythm (AHD week = Sun–Thu).

## Optional: skip public holidays

The sequential model simply advances on the next working day, so a one-off
holiday is handled by **pausing the flow that day** (turn Off, turn back On). If
you'd rather automate it, add a small **Condition** after the trigger that checks
`convertTimeZone(utcNow(),'UTC','Arabian Standard Time','yyyy-MM-dd')` against a
short list of holiday dates and Terminates on a match.

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
