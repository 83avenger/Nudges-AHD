# Runbook — Azure Cost Management for Copilot Studio PAYG

**Goal:** cap and monitor Copilot Studio pay‑as‑you‑go spend, and measure the
**real per‑card cost** before any wider rollout. Do this **before** publishing the
agent / sending cards.

**Owner:** Azure subscription Owner/Contributor. **Est. time:** 20–30 min.

---

## 1. Create a budget with alerts (the guardrail)
1. **Azure portal → Cost Management + Billing → Cost Management → Budgets → + Add.**
2. **Scope:** the subscription, then narrow to resource group
   **`rg-copilotstudio-wellbeing`** (the one linked in the PAYG billing policy).
3. **Amount:** start conservative — e.g. **$100/month** (pilot est. ~$44).
4. **Reset period:** Monthly.
5. **Alert conditions:** add thresholds at **50%, 80%, 100%** of budget
   (actual cost), and a **forecasted 100%** alert.
6. **Alert recipients:** IT distribution list + Fahad (or an **Action Group** that
   emails/Teams‑notifies them).
7. Save.

> The budget **alerts** you; it does not hard‑stop spend. For a hard stop you'd
> disable the billing policy / unpublish the agent. Keep the threshold low for the
> pilot so any surprise is caught immediately.

## 2. Build a Cost Analysis view for Copilot Studio
1. **Cost Management → Cost analysis.**
2. **Scope:** `rg-copilotstudio-wellbeing` (or the subscription).
3. **Filter:** Service name / Meter category = **Power Platform / Copilot Studio**
   (meter names contain "Copilot Studio" / credits).
4. **Group by:** Meter (or Resource) to see credits consumed.
5. **Granularity:** Daily. **Save** the view as `Copilot Studio - Wellbeing`.
6. (Optional) **Pin to an Azure dashboard** for IT.

## 3. Tagging (attribution)
- Tag `rg-copilotstudio-wellbeing` with e.g. `project=Wellbeing365`,
  `owner=HealthInnovationHub`. Enables cost reports filtered by tag.

## 4. Scheduled cost export (optional)
- **Cost Management → Exports → + Add** → daily/monthly CSV of costs for the
  resource group to a storage account, for finance reporting.

## 5. The measurement test (get the REAL per‑card cost)
1. With the budget/alerts live and the agent published, set the flows' **Post as →
   AHD Thrive365** against a **small test group**.
2. **Send ~20 cards** (run the flows a few times, or lower the schedule for a day).
3. **Wait ~24 hours** — Azure consumption meters lag; same‑day figures are incomplete.
4. In **Cost analysis** (Copilot Studio view), read **credits/cost** for that window.
5. Compute:
   - `credits per card = total credits ÷ number of cards sent`
   - `monthly estimate = credits per card × 4 × 21 × <user count> × $0.01`
   - add **~5% VAT** and AED FX for the UAE all‑in figure.
6. Record the number in the PR / handover; use it to decide rollout.

## 6. Ongoing monitoring
- Review the Cost Analysis view **weekly** during the pilot.
- If costs approach the budget, investigate volume or **pause** the branded sender
  (revert Post as → Flow bot, which is $0).
- Re‑evaluate **PAYG vs the $200 pack** if monthly credits exceed ~20,000
  (~238 users).

## Checklist
- [ ] Budget on `rg-copilotstudio-wellbeing` (~$100/mo) with 50/80/100% + forecast alerts
- [ ] Alert recipients / action group configured
- [ ] Saved Cost Analysis view filtered to Copilot Studio
- [ ] Resource group tagged for attribution
- [ ] 20‑card measurement test run; real per‑card cost recorded
- [ ] Weekly review scheduled during the pilot
