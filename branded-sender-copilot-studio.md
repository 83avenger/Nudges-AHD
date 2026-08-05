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

### 1. Create the agent
1. Go to **copilotstudio.microsoft.com** → sign in.
2. **+ Create → New agent** (you can skip the AI description prompts).
3. **Name:** `AHD Thrive365`. Add a short description and the **icon**.
4. Save. You don't need any topics/knowledge — this agent only acts as the
   branded sender for cards posted from the flow.

### 2. Turn off unnecessary AI features (optional, keeps it simple)
- In **Settings → Generative AI**, you can leave defaults; the agent won't be
  used conversationally, just as the posting identity.

### 3. Add the Teams channel
1. In the agent → **Channels** (or **Settings → Channels**) → **Microsoft Teams**.
2. **Turn on Teams** / **Add channel**.
3. **Publish** the agent (top-right **Publish**).

### 4. Get it approved for Teams
- Publishing a Copilot Studio agent to Teams typically submits it to the
  **Teams admin center → Manage apps** for approval.
- Ask your **Teams admin** to **approve/allow** the "AHD Thrive365" app so it can
  message users in the tenant.
- (Depending on tenant policy, the admin may also need to add it to an app
  setup/permission policy.)

### 5. Point the flow's card at the branded bot
1. Open each of the four pillar flows → the **Post card in a chat or channel**
   action.
2. Change **Post as** from **Flow bot** to your **Power Virtual Agents / Copilot
   Studio bot** and select **AHD Thrive365**.
3. Keep **Post in = Chat with bot**, recipient = the member's
   `userPrincipalName`, and the same Adaptive Card.
4. Save and test — the sender now shows **AHD Thrive365** with your icon.

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

This means your tenant's **Power Platform environment is disabled** (or you have no
Copilot Studio licence) — an **admin‑only** gate. You cannot self‑serve past it.
Ask a **Power Platform admin** to enable/create an environment and assign you a
**Copilot Studio** licence, or fall back to **Option C** (keep "Workflows"; the
card is already branded). This is a cosmetic follow‑up, not a launch blocker.

## Alternative (heaviest) — custom Azure Bot + Teams app

Register an Azure Bot named "AHD Thrive365", build a Teams app manifest, and have
IT sideload/approve it, then post through its messaging endpoint. Most control
(name, avatar, 1:1), but real development + admin effort — not recommended for a
pilot.
