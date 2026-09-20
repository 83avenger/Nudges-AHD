# Runbook — Service Account for the Wellbeing365 Flows

**Goal:** run the four pillar flows' connections under a dedicated, non‑personal
account so the program survives staff changes and isn't blocked by Tier‑0 admin
policies. Replaces the current `t0-mayub` (privileged admin) connections.

**Owner:** IT (Identity + Power Platform). **Est. time:** 45–60 min + security sign‑off.

---

## 0. Paste‑ready request to IT Security / Identity

> **Subject: Service account for AHD Wellbeing365 Power Automate flows**
>
> Please provision a **dedicated service account** for the Wellbeing365 nudge
> automation:
> - **UPN:** `svc-thrive365@ahdubai.com` (non‑personal, cloud‑only is fine)
> - **Licence:** one **Microsoft 365** licence that includes **Teams + SharePoint**
>   (standard; no premium Power Automate needed — flows use standard connectors).
> - **Access:** member of the recipient M365 group; **Edit** on the
>   `FourPillarNudges` SharePoint list.
> - **Conditional Access:** exclude this account from the **Tier‑0 / interactive**
>   policies that block unattended token refresh (sign‑in frequency, token
>   protection / device‑bound tokens, device‑compliance) — these currently cause
>   `AADSTS135010` and break the SharePoint connection. Apply a **service‑account
>   CA policy** instead (e.g. restrict to named locations/IPs, no token binding).
> - **Password:** long, vaulted, **excluded from forced rotation** (rotation breaks
>   the stored connection token and requires manual re‑auth).
>
> Purpose: unattended cloud flows posting daily wellbeing nudges in Teams.

---

## 1. Create the account
1. **M365 admin center → Users → Active users → Add a user.**
2. UPN `svc-thrive365@ahdubai.com`; display name `AHD Thrive365 Service`.
3. Set a **long random password**; store in the IT password vault.
4. Uncheck "require password change at next sign‑in" (a service account).

## 2. Licence it
- Assign a **Microsoft 365** licence with **Teams** and **SharePoint** enabled.
- (Standard connectors only — **no** Power Automate Premium required.)

## 3. Conditional Access (security)
- **Exclude** the account from Tier‑0 / interactive‑only CA policies that stop
  unattended token refresh (the cause of `AADSTS135010`).
- Put it under a **service‑account CA policy**: allow from named locations / a
  fixed egress IP, block legacy auth, no token‑protection binding.
- Decide MFA approach with security: either exclude with compensating controls
  (named‑location + long password) or use a supported workload‑identity pattern.
  The account must be able to complete an **interactive sign‑in once** to
  authorize the Power Automate connections, and keep a **refreshable token**.

## 4. Grant access
- **Recipient M365 group:** add `svc-thrive365` as a **member**.
- **SharePoint list:** site → `FourPillarNudges` → (or the site) grant **Edit**.
- **Teams:** confirm the Teams licence/service plan is on.

## 5. Re‑authorize the flow connections
For **each** of the four pillar flows, and **each** connector (Microsoft Teams,
Office 365 Groups, SharePoint):
1. Sign into Power Automate **as the service account** (private browser window),
   or edit each flow and, on each action, **⋯ → + Add new connection → sign in as
   `svc-thrive365`**.
2. Confirm every action now uses the **service‑account** connection.
3. Delete the old `t0-mayub` connections and any **duplicate** connections.

## 6. Co‑owners (no single‑person ownership)
- Each flow → **Details / Share → Owners → +** → add **`svc-thrive365`** and an
  **IT team / security group**.

## 7. Test & verify
- **Run each flow** once (or wait for a slot). Confirm success under the service
  account and that the nudge posts + the row flips to `Sent`.
- Check **Run history** for any auth errors over 24–48 h.

## 8. Document & maintain
- Record the account, its licence, group/list access, CA policy, and owners in the
  IT runbook/vault.
- **Rotation caveat:** if the password is rotated, the connections break and must
  be **re‑authorized**. Prefer exclusion from forced rotation, or schedule a
  planned re‑auth window.

## Rollback
If a connection fails after the switch, temporarily **Fix connection** on the old
account to restore service, then resolve the service‑account CA/licence issue and
re‑switch.

## Checklist
- [ ] Account created + vaulted password
- [ ] M365 (Teams+SharePoint) licence assigned
- [ ] Excluded from Tier‑0 CA; service‑account policy applied
- [ ] Member of recipient group + Edit on the list
- [ ] All connections in all 4 flows = service account (old/duplicates removed)
- [ ] Service account + IT group are co‑owners of each flow
- [ ] Test run green; 24–48 h clean run history
