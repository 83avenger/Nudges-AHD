# Branding the Sender Name — "AHD Thrive365" instead of "Workflows"

By default the nudge cards are posted by Microsoft's built-in **Flow bot**, which
shows as **"Workflows"** in Teams — its name and icon **cannot be changed**. The
cards themselves are already branded (header reads *AHD Thrive365 · Pillar*), and
for most pilots that's enough (**Option C — do nothing**).

If leadership wants the **sender name** to read **"AHD Thrive365"**, the lightest
supported way is to post as a **Copilot Studio agent** you name yourself. This
doc covers that. (A full custom Azure Bot / Teams app is the heavier alternative
and usually overkill.)

> Consider doing this **after** the September decision gate — it needs a Copilot
> Studio licence and admin approval, and it doesn't change the nudge behaviour,
> only the sender label.

## Prerequisites

- A **Copilot Studio** licence (or trial) in the tenant.
- Rights to **publish an agent to Microsoft Teams** — usually requires a **Teams
  admin** to approve/allow the custom app.
- The AHD Thrive365 icon (PNG) for the agent avatar.

## Steps

### 1. Open Copilot Studio in the RIGHT environment
1. Go to **https://copilotstudio.microsoft.com** and sign in.
2. **Top‑right → environment picker** → pick a **Ready** environment — ideally the
   **same one your nudges flow lives in** (check Power Automate's environment
   picker). Prefer the **Default** environment (Dataverse = Yes). Avoid Disabled
   and "Microsoft Teams"‑type environments.

### 2. Create the agent
1. Left nav → **Create** (or **Agents → + New agent**).
2. If it opens the "Describe your agent" chat, click **Skip to configure**
   (or **Skip**) to go straight to the setup form.
3. Fill in:
   - **Name:** `AHD Thrive365`
   - **Description:** `Posts the AHD Wellbeing365 daily wellbeing nudges.`
   - **Instructions:** leave blank / minimal — this agent is only a posting
     identity, it won't hold conversations.
4. Click **Create**. Wait for the agent to open.

### 3. Set the display name and icon
1. In the agent → **Settings → Details** (or the **⚙ / Overview** page).
2. Confirm **Name = AHD Thrive365**.
3. Upload the **AHD Thrive365 icon** (PNG). This becomes the sender avatar in Teams.
4. Save.

### 4. (Optional) keep it non‑conversational
- You do **not** need topics, knowledge sources, or generative answers. It's fine
  to leave defaults; the agent is used only as the "Post as" identity.

### 5. Connect the Teams channel
1. In the agent → **Channels** (top menu) → **Microsoft Teams**.
2. Click **Turn on Teams** / **Add channel** → confirm.
3. Choose availability: make it available to your org (an option like
   **"Make agent available to everyone in my org"** or **"Show to everyone once
   admin approves"**).

### 6. Publish
1. Top‑right → **Publish** → **Publish** again to confirm.
2. Wait for the "Published" confirmation.

### 7. Get it approved for Teams (admin)
- Publishing to Teams submits the app to **Teams admin center → Teams apps →
  Manage apps** for approval.
- Ask your **Teams admin** to find **"AHD Thrive365"** and **Allow/Approve** it
  (and, if needed, add it to an **app setup / permission policy** so it can
  message users 1:1).
- Until approved, the "Post as" bot may not deliver to users.

### 8. Point each flow's card at the branded bot
1. Open each of the four pillar flows → the **Post card in a chat or channel**
   action.
2. Change **Post as** from **Flow bot** to **Power Virtual Agents** (or **Copilot
   Studio**) and select **AHD Thrive365**.
3. Keep **Post in = Chat with bot**, recipient = the member's
   `userPrincipalName`, and the same Adaptive Card.
4. **Save → Test** — the sender now shows **AHD Thrive365** with your icon.
   - If the bot isn't listed in "Post as", it isn't published/approved yet, or the
     flow is in a **different environment** than the agent — rebuild the agent in
     the flow's environment (Step 1).

## Caveats

- **Licence + admin gate:** without a Copilot Studio licence and Teams-admin
  approval, this can't be completed by a standard user.
- **First-message consent:** some tenants require the user to have the bot
  installed / accept it before it can message them 1:1; the admin approval
  usually handles this org-wide.
- **No change to logic:** the schedule, list, and card content are identical —
  only the sender identity changes.
- If any of this stalls, fall back to **Option C**: keep "Workflows" as the
  poster; the card header already carries the AHD Thrive365 brand.

## "This environment is turned off" when opening Copilot Studio

Usually it means Copilot Studio opened in a **disabled** environment. **Switch
environments first:** top‑right environment picker → choose a **Ready** one
(prefer your tenant's **Default** environment with Dataverse = Yes, which is
typically where the nudges flow also lives; avoid Disabled and "Microsoft Teams"
‑type environments). Build the agent in the **same environment as the flow** so
the flow's *Post as* can find the bot.

If **all** environments are off, or publishing prompts for a **Copilot Studio
licence** you don't have, that's the admin/licence gate — ask a Power Platform
admin, or fall back to **Option C** (keep "Workflows"; the card is already
branded). This is a cosmetic follow‑up, not a launch blocker.

## "There is a billing issue" on Publish (confirmed gate in this tenant)

Publish is blocked with *"There is a billing issue. Please contact your admin to
confirm the billing capability for this environment and agent."* This means
**Copilot Studio billing is not set up**. To publish, an **admin** must enable one
of (each has a **real cost**):
- a **Copilot Studio licence** assigned to the maker, **or**
- **pay‑as‑you‑go** billing (an Azure subscription linked to the environment), **or**
- a **Copilot Studio message‑capacity pack** for the tenant.

**Decision:** since this incurs cost purely for a **display name** (the card is
already branded AHD Thrive365), launch the pilot on **"Workflows"** (Option C) and
raise Copilot Studio licensing with IT only if leadership wants the branded sender
after the September gate. An unpublished agent costs nothing; you can leave or
delete it.

## Cost under pay-as-you-go (if you choose to publish)

Copilot Studio is billed in **Copilot Credits** (formerly "messages"):
- **Pay-as-you-go:** ~**$0.01 per credit** via Azure, no commitment.
- **Capacity pack:** **$200/month for 25,000 credits** (annual, ~$0.008/credit).
- Consumption per feature: classic answer ~1, generative answer ~2, grounding ~10,
  autonomous action ~25+. This agent does no AI, so a posted card is ~a basic
  interaction (**treat as ~1 credit** until measured).
- **Exemption:** users with **M365 Copilot** licences don't consume credits for
  internal agent interactions.

Estimated volume = 4 nudges/day × ~21 working days (at ~1 credit/card):

| Scope | Cards/month | PAYG @ ~$0.01 | Pack alt. ($200/25k) | Cheaper |
|-------|-------------|---------------|----------------------|---------|
| Pilot – 50 users | ~4,200 | **~$42/mo** | 1 pack = $200 | **PAYG** |
| 250 users | ~21,000 | ~$210/mo | 1 pack = $200 | pack (marginal) |
| 1,000 users | ~84,000 | ~$840/mo | 4 packs = $800 | pack |
| **4,000 users** | **~336,000** | **~$3,360/mo** | **14 packs = $2,800** | **pack** |

PAYG is cheaper up to ~238 users (~20k credits); above that the $200 pack wins.
UAE all‑in: add ~5% VAT + AED FX (pilot ≈ ~$44/mo).

**Cost scales linearly with users** — cheap for the pilot, but potentially
thousands/month at full-org scale, purely for the sender name (the Flow bot is
$0 at any scale).

### PAYG vs pack, and UAE notes
- **Both are available** (2026). PAYG needs an **Azure subscription** linked to the
  environment (admin sets it up); packs are bought via the M365 admin center. No
  UAE‑specific restriction found — PAYG bills through Azure, which operates in the
  UAE (UAE North/Central).
- **Break‑even:** the $200 pack only beats PAYG above **~20,000 credits/month
  (~238 users)**. Below that, **PAYG is cheaper** — so use **PAYG for the pilot**.
- **UAE billing:** Azure PAYG is **USD‑metered**; invoiced in **AED** with FX + **5%
  VAT**. Pilot ≈ **$42 + 5% ≈ ~$44/mo (~AED 162)**.
- PAYG has **no commitment**, so it doubles as the measurement test — turn it on,
  send ~20 cards, read the meter for the real per‑card credit rate.

**Verify before scaling:** it's not clearly documented how many credits a
proactive card posted via Power Automate "Post as" the agent actually consumes.
Publish, send a few test cards, then read the **Azure Cost Management / Copilot
Studio meter** to get the real per-card credit rate before rolling out widely.

Pricing references (verify current figures):
- CloudZero — Copilot Studio pricing: https://www.cloudzero.com/blog/copilot-studio-pricing/
- A Guide to Cloud — Copilot Studio PAYG: https://www.aguidetocloud.com/blog/copilot-studio-pricing/

## Alternative (heaviest) — custom Azure Bot + Teams app

Register an Azure Bot named "AHD Thrive365", build a Teams app manifest, and have
IT sideload/approve it, then post through its messaging endpoint. Most control
(name, avatar, 1:1), but real development + admin effort — not recommended for a
pilot.
