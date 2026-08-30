# Go‑Live Checklist — AHD Wellbeing365 Nudges

Everything to confirm before turning the pilot on for real users. The build is
proven working; this is the production‑readiness pass.

Model: **4 bilingual nudges/day**, one per pillar — 07:00 Social · 09:15 Physical
· 11:30 Financial · 13:45 Mental (UAE), **Sun–Thu**.

---

## A · Content & approvals
- [ ] **Social** nudges confirmed (already the 21 approved Month of Connection challenges).
- [ ] **Physical / Financial / Mental** wording approved by the wellbeing team
      (Dr. Dania) — currently `SourceRef = draft`.
- [ ] **Native‑Arabic review** of all four pillars' `NudgeAR` text.
- [ ] Financial nudges confirmed **educational/awareness only** (no individual advice).

## B · SharePoint list
- [ ] `FourPillarNudges` list exists with **correct internal column names**
      (`Day`, `Pillar`, `Status`, `NudgeEN` … — **not** `field_1/field_7`).
      Verify: Get items with no filter → keys are real names.
- [ ] **84 items** loaded (21 days × 4 pillars); Arabic renders right‑to‑left.

## C · Flows
- [ ] All **four** pillar flows built (Social/Physical/Financial/Mental) — each with
      the right **time** and **`Pillar eq '…'`** filter.
- [ ] Card **populates** correctly (matches the `GetItems` action name).
- [ ] **Update item → Sent** works (nudge advances Day 1 → Day 2), placed **after**
      the Apply‑to‑each (posts once/day).
- [ ] Recipient set to **`userPrincipalName`** (token, not text).

## D · Ownership & connections (critical — see `operations-service-account.md`)
- [ ] Connections re‑authorized under a **dedicated service account**
      (`svc-thrive365@ahdubai.com`), **not** a personal / Tier‑0 admin account.
- [ ] Service account is a **member of the recipient group** and has **Edit** on the list.
- [ ] Each flow has the **service account + an IT group** as co‑owners.

## E · Licences required
See the table below. **Core pilot needs no new paid licences** — standard M365.

## F · Recipient group
- [ ] Flows point at the **real pilot M365 group** (not the test group).
- [ ] All members are **Teams‑licensed** (unlicensed/guest accounts can't receive
      Flow‑bot cards — the `(Dell)` contractor accounts were test‑only).

## G · Reset for launch (everyone starts Day 1 together)
- [ ] All rows `Status = Scheduled`; `SentDateTime` and `RunID` cleared.
      Fastest: `./provisioning/Import-Data.ps1 -SiteUrl "…" -Fresh`
      (or bulk‑edit in grid view).

## H · Go‑live
- [ ] Turn **all four** flows **On** on the intended start day (a **Sunday** opens
      the week cleanly).
- [ ] Send an **executive sponsor / launch** message so staff expect the nudges.

## I · Monitor & maintain
- [ ] Watch **Run history** for failures; reset any `Error` row to `Scheduled`.
- [ ] **September gate (1–3 Sep):** review metrics (`IT-handover.md`), decide next month.
- [ ] Next month: load the new rows (same automation, no rebuild).

## Optional add‑ons (not required to launch)
- [ ] **Branded channel feed** (free, Flow bot) — `branded-channel-feed.md`.
- [ ] **Branded sender "AHD Thrive365"** — Copilot Studio (**paid**, `branded-sender-copilot-studio.md`).
- [ ] **Parallel channel demo** for the 1:1 vs channel comparison — `channel-vs-1to1-comparison.md`.

---

## Licences required

| Who / what | Licence needed | Cost | Notes |
|-----------|----------------|------|-------|
| **Recipients** (get the Teams cards) | Microsoft 365 with **Teams** | Already owned | Standard M365 includes Teams + SharePoint. |
| **Service account** (runs the flows) | One **Microsoft 365** licence | Standard | The seeded "Power Automate for Microsoft 365" use rights cover **standard** connectors — no premium needed. |
| **Core flows** (SharePoint, Teams, Office 365 Groups, Recurrence) | Standard connectors | **$0 extra** | All standard; no Power Automate Premium. |
| **SharePoint list** | M365 (SharePoint) | Included | — |
| **List provisioning** (PnP scripts) | None (interactive sign‑in) | $0 | Needs PowerShell 7 + a maker who can create a list. |
| — Optional — | | | |
| **Branded sender** (Copilot Studio) | **Copilot Studio** licence or **pay‑as‑you‑go** | Paid | ~$0.01/credit PAYG; scales with volume. See `branded-sender-copilot-studio.md`. |
| **Webhook channel sender** | **Power Automate Premium** (HTTP action) | Paid (~$15/user or per‑flow) | Also on a deprecating connector. |

**Bottom line:** the pilot runs on **existing Microsoft 365 licences — no new
paid licences** for the core 4‑nudges‑a‑day program. Paid licences apply **only**
to the optional branded‑sender routes.
