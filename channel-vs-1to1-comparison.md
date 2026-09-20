# Parallel Demo — 1:1 Nudges vs Teams Channel (comparison)

Run **both** delivery models at once to demonstrate, in real conditions, why the
**1:1 nudge** is the stronger design and what the **channel** gives up. The
existing four pillar flows stay **exactly as they are**; the channel demo is a
**separate, read‑only** flow that never changes the list, so nothing about the
1:1 delivery is affected.

## Setup at a glance

```
(unchanged)  Thrive365-Social / Physical / Financial / Mental  → 1:1 cards, mark Sent
(new, added) Thrive365-ChannelDemo                              → mirrors each nudge to a channel, marks nothing
```

---

## Step 1 · Create the demo channel
1. Teams → **Create team** → name **`AHD Thrive365 (Channel Demo)`** → add the
   pilot members → optional channel **`Daily Nudges`**.
2. This is a throwaway demo space — you can delete it after the comparison.

## Step 2 · Build the ChannelDemo flow (read‑only, non‑invasive)
A single new flow that mirrors what the 1:1 flows just sent — **without** marking
anything Sent.

1. **New scheduled cloud flow → Recurrence**, Time zone **Abu Dhabi, Muscat**,
   **Sun–Thu**, at **07:05 / 09:20 / 11:35 / 13:50** (5 min *after* each 1:1 slot
   so it mirrors the nudge already delivered). *(Four times a day — use four
   small copies, or one 15‑min‑gate flow, same as the pillar flows.)*
2. **Compute** which pillar this slot is (or make one copy per pillar, like the
   1:1 flows).
3. **Get items** on `FourPillarNudges`:
   - **Filter:** `Pillar eq '<pillar>' and Status eq 'Sent'`
   - **Order By:** `Modified desc` · **Top Count:** `1`
   - → this returns the nudge the 1:1 flow **just delivered** for that pillar.
4. **Condition:** if none, Terminate.
5. **Post card in a chat or channel** → **Post as Flow bot** → **Post in:
   Channel** → your `AHD Thrive365 (Channel Demo)` channel → paste the pillar card
   (`adaptive-card-pillar.powerautomate.json`, matching your Get items action
   name).
6. **Do NOT add an Update item** — this flow only reads. Status stays owned by the
   1:1 flows.

> Result: the same daily nudges appear **both** as personal 1:1 cards **and** in
> the channel, so leadership sees the two experiences in parallel.

---

## Step 3 · What to observe (the disadvantages surface on their own)

Track these over the demo window — they are exactly the channel weaknesses:

| Dimension | 1:1 nudge | Teams channel | What to show |
|-----------|-----------|---------------|--------------|
| **Guaranteed reach** | ✅ Every recipient gets it; can't "leave" a bot chat | ❌ Members can **leave / hide / mute** the channel and stop seeing posts | Count channel **leaves/mutes** vs 100% 1:1 delivery |
| **Notification** | ✅ Personal ping, hard to miss | ⚠️ Channel posts are easy to overlook; many mute busy channels | Compare read/seen behaviour |
| **Personal feel** | ✅ Private, feels addressed to me | ❌ Broadcast to a group; less personal for a wellbeing message | Qualitative Champion feedback |
| **Membership control** | ✅ Recipient group is managed centrally | ❌ People self‑remove; to prevent it you need org‑wide/dynamic teams (heavy, forced) | Show attrition from the channel |
| **Noise / fatigue** | Each nudge is its own quiet ping | 4 posts/day in one channel can feel like spam → mutes | Track mute rate |
| **Branding (sender)** | "Workflows" (card is branded) | Can be "AHD Thrive365" only via **premium webhook** (deprecating) | Note the cost/risk to gain a label |
| **Cost** | $0 (standard) | $0 with Flow bot; **premium** for a branded sender | — |
| **Privacy** | 1:1 keeps engagement private | Reactions/who's active are visible to all members | Relevant to a wellbeing context |

### Suggested demo metrics (1–2 weeks)
- **Reach:** 1:1 = 100% of the group; channel = members remaining × who actually views.
- **Attrition:** number who **left or muted** the channel (the headline disadvantage).
- **Engagement:** reactions/replies in channel vs. (if measured) 1:1 reactions.
- **Sentiment:** one Champion question — "which felt better, the personal nudge or
  the channel?"

---

## Step 4 · Expected conclusion

The channel will typically show **membership attrition, mutes, and lower personal
resonance**, while the 1:1 delivers to everyone and feels personal — demonstrating
why the pilot should run on **1:1**, optionally with a branded channel as a
*complementary* feed (see `branded-channel-feed.md`), not as the primary channel.

## Cleanup
After the comparison, **turn off / delete the ChannelDemo flow** and the demo
team. The 1:1 flows are untouched and remain the production setup.
