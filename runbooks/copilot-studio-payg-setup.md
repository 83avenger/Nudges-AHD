# Runbook — Enable Copilot Studio Pay‑As‑You‑Go (branded sender)

**Goal:** enable Copilot Studio **pay‑as‑you‑go** billing so the "AHD Thrive365"
agent can publish and post as the branded sender — with **cost controls in place
first** (see `azure-cost-management-setup.md`).

**Owner:** Power Platform admin + Azure subscription Owner/Contributor.
**Cost:** ~$0.01/credit; pilot ≈ **$42/mo + AED FX + 5% VAT ≈ ~$44/mo**. No commitment.

> **Do the cost‑management setup (budget + alerts) BEFORE publishing** so usage is
> capped and visible from the first card.

---

## 0. Paste‑ready request to IT / Azure admin

> **Subject: Enable Copilot Studio pay‑as‑you‑go for the Wellbeing365 branded sender**
>
> To let the "AHD Thrive365" agent post the daily nudges under its own name,
> please enable **Copilot Studio pay‑as‑you‑go**:
> - Use an existing **Azure subscription** (any) + a dedicated **resource group**
>   `rg-copilotstudio-wellbeing`.
> - In **Power Platform admin center → Billing policies**, create a policy linking
>   that subscription/resource group and **assign the Copilot Studio environment**
>   hosting the agent.
> - Before go‑live, set an **Azure Cost Management budget** (e.g. **$100/month**)
>   on that resource group with alerts at 50/80/100% to IT + Fahad.
>
> This is usage‑based (~$0.01/credit), no upfront commitment; pilot estimate
> ~$44/month incl. VAT. We will run a 20‑card measurement test to confirm the
> real per‑card cost before any wider rollout.

---

## 1. Prerequisites
- An **Azure subscription** in the tenant (any active one).
- **Owner/Contributor** on that subscription (to create a resource group + budget).
- **Power Platform admin** (to create a billing policy and assign the environment).
- The Copilot Studio **environment** hosting the "AHD Thrive365" agent (the same
  environment as the flows — usually the Default environment).

## 2. Create a resource group (for clean cost attribution)
1. **Azure portal → Resource groups → Create.**
2. Name `rg-copilotstudio-wellbeing`, region near you (e.g. UAE North).
3. (Register the **`Microsoft.PowerPlatform`** resource provider on the
   subscription if prompted: Subscription → Resource providers → register.)

## 3. Set the cost guardrails FIRST
- Follow `azure-cost-management-setup.md` now — create the **budget + alerts** on
  `rg-copilotstudio-wellbeing` **before** enabling usage.

## 4. Create the pay‑as‑you‑go billing policy
1. **Power Platform admin center** (admin.powerplatform.microsoft.com) →
   **Billing → Billing policies → New billing policy** *(name/menu wording may
   vary by release)*.
2. Name it `Wellbeing365-PAYG`; select the **Azure subscription** and
   **`rg-copilotstudio-wellbeing`** resource group; pick the region.
3. **Create**, then open the policy → **Environments → Add** → add the
   Copilot Studio environment hosting the agent.
4. This registers the Copilot Studio **pay‑as‑you‑go meter**; usage in that
   environment now bills to the Azure subscription.

## 5. Publish the agent
- Back in Copilot Studio, **Publish** the "AHD Thrive365" agent — the earlier
  *"There is a billing issue"* block should now clear.
- Add the **Teams** channel and get **Teams‑admin approval** (see
  `../branded-sender-copilot-studio.md`).

## 6. Wire the flows + run the measurement test
1. In each pillar flow's **Post card** action, set **Post as → AHD Thrive365**.
2. Point at a **small test group** and send ~**20 cards**.
3. Wait ~24 h (Azure meters lag), then read the cost (see cost‑management runbook)
   → compute **credits per card** and the **real AED cost** before scaling.

## Decision gate
- If measured cost is acceptable **and** leadership wants the branded sender →
  roll out to the pilot group.
- Otherwise → keep the free **"Workflows"** sender (the card is already branded).

## Checklist
- [ ] Azure subscription + `rg-copilotstudio-wellbeing` ready; provider registered
- [ ] Budget + alerts set (cost‑management runbook) **before** usage
- [ ] Billing policy created and Copilot Studio environment assigned
- [ ] Agent published; Teams channel approved
- [ ] Flows set to Post as AHD Thrive365 (test group)
- [ ] 20‑card test run; real per‑card cost captured
