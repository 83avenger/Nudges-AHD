# Branded "AHD Thrive365" Channel Feed (alongside the 1:1 nudges)

Keep the **1:1 nudges** (reliable, personal — recipients can't "leave" a bot
chat) and **add a shared feed** in a Teams channel you name **AHD Thrive365**, so
there's a community space people can see and react to.

Two ways to post to the channel — pick based on whether you need the **sender
name** branded:

| Option | Sender shows as | Cost | Future-proof? |
|--------|-----------------|------|---------------|
| **1 · Flow bot → channel** *(recommended)* | "Workflows" (inside the AHD Thrive365 channel) | **Free** (standard) | ✅ Yes |
| **2 · Incoming Webhook** | **"AHD Thrive365"** (custom name + icon) | Premium (HTTP action) | ⚠️ Office 365 webhooks are being **retired** |

> Reality check: the *channel* is branded either way. Option 2 only changes the
> **author label** — at the cost of a premium Power Automate plan and building on
> a deprecating connector. For most teams **Option 1 is the right call**.

---

## Step 1 · Create the branded channel (both options)

1. In **Teams → Teams → + → Create team** (or use an existing team).
2. Name it **`AHD Thrive365 · Wellbeing`**, add the icon, add the pilot members.
3. (Optional) create a channel inside it named **`Daily Nudges`**.
4. Note the **Team** and **Channel** you'll post to.

> Members *can* leave a team/channel or mute it — so treat this feed as a
> **complement** to the 1:1 nudges, not a replacement. The 1:1 send guarantees
> reach; the channel adds visibility and reactions (and "mutes/leaves" are a
> useful fatigue signal per the pilot metrics).

---

## Option 1 · Post to the channel with Flow bot (free)

Add **one** channel post per day (once per pillar, **outside** the Apply‑to‑each
so it posts once, not per member). In each pillar flow, after **Update item**:

1. **+ Add action → Microsoft Teams → Post card in a chat or channel.**
2. **Post as:** `Flow bot` · **Post in:** `Channel`.
3. Select your **Team** and **Channel** (`AHD Thrive365 · Wellbeing` / `Daily Nudges`).
4. **Adaptive Card:** paste the same `adaptive-card-pillar.powerautomate.json`
   (match the `Get_items`/`GetItems` action name to yours).
5. Save. Now each pillar's nudge also lands in the shared channel.

Sender shows as "Workflows", but the **channel** is clearly AHD Thrive365 and the
**card header** is branded. $0, standard connector, no deprecation risk.

---

## Option 2 · Incoming Webhook (branded sender, premium + deprecating)

### 2a. Create the webhook
1. In Teams, go to the target **channel → ⋯ → Connectors** (or **Manage channel →
   Connectors**).
2. Find **Incoming Webhook → Configure/Add.**
3. **Name:** `AHD Thrive365` · upload the **icon** (this is the sender identity).
4. **Create** → **copy the webhook URL** (keep it secret — anyone with it can post).

> If **Connectors** is missing, Office 365 connectors are disabled/retired in your
> tenant — use Option 1 instead.

### 2b. Post to it from the flow (needs the premium HTTP action)
In each pillar flow, after **Update item**, add:
1. **+ Add action → HTTP** (premium).
2. **Method:** `POST` · **URI:** the webhook URL.
3. **Headers:** `Content-Type: application/json`.
4. **Body:** paste **`webhook-card-payload.json`** — it wraps the pillar card in
   the required webhook envelope:
   ```json
   { "type": "message",
     "attachments": [
       { "contentType": "application/vnd.microsoft.card.adaptive",
         "content": { ...pillar card... } } ] }
   ```
   Match the `Get_items` action name inside it to your flow's Get items action.
5. Save. The card now posts to the channel from **"AHD Thrive365"** with your icon.

**Caveats:** the HTTP action requires a **premium Power Automate plan**; Office 365
incoming‑webhook connectors are being **retired** by Microsoft (timelines keep
shifting) — don't build long‑term on this.

---

## Recommended shape

- **Keep 1:1 nudges** as the reliable core (four pillar flows).
- **Add Option 1** (Flow bot → `AHD Thrive365 · Wellbeing` channel) for the shared
  feed — free and future‑proof.
- Consider the **branded sender** (Option 2 or Copilot Studio) only if leadership
  decides it's worth the cost/risk after the September gate.
