# Operations — Connection Ownership & Service Account

**Problem to fix before go‑live:** the four pillar flows currently authenticate
their Teams / Office 365 Groups / SharePoint connections as a **personal account**
(the person who built them). If that account is **disabled, deleted, password/MFA
changed, or leaves the organization**, the connections stop authenticating, the
flows fail, and **nudges stop** — and if that person is the sole flow owner, the
flows can be orphaned and deleted.

Additionally, if the builder account is a **privileged/Tier‑0 admin** (e.g. a
`t0-*` account), running a wellbeing automation under it is **over‑privileged**
and a security concern.

## Fix — run everything under a dedicated service account

### 1. Create a service account
- e.g. **`svc-thrive365@ahdubai.com`** — a **non‑personal**, licensed account.
- Licence must include **Teams** and **SharePoint** (standard M365 is enough).
- Store its credentials in the IT password vault; enable it for unattended use
  per your tenant's policy (it still needs to satisfy MFA/conditional access —
  work with IT on an appropriate exclusion or a managed identity).

### 2. Grant it the access the flows need
- **Recipient M365 group:** add the service account as a **member/owner** so it
  can read group members.
- **SharePoint `FourPillarNudges` list:** give it **Edit** access (read the
  nudges, write Status/SentDateTime/RunID).
- **Teams:** it must be able to post via the Flow bot (default in most tenants).

### 3. Re‑authorize each connection as the service account
In **each** of the four flows, for **each** connector (Microsoft Teams, Office 365
Groups, SharePoint):
- Open the action → connection menu (**⋯ → + Add new connection**) → **sign in as
  `svc-thrive365`**.
- Confirm all connections now show the **service account**, not a person.

### 4. Add co‑owners (no single‑person ownership)
- Each flow → **Details / Share → Owners → +** → add the **service account** and
  an **IT team / security group**.
- Now the flows survive any individual leaving, and IT can maintain them.

## Notes

- **This does not change the sender name.** Cards still post as the Flow bot
  ("Workflows"); the connection identity is about **reliability and ownership**,
  not branding.
- **Better still (optional, for IT/ALM):** move the flows into a **solution** in a
  shared **Production environment** and use **connection references** bound to the
  service account. That makes ownership, export/import, and environment promotion
  clean. Overkill for the pilot, recommended for the 12‑month rollout.
- **Ongoing:** whoever owns the recipient group and the SharePoint list should be
  a team/role, not one person, for the same reason.

## Pre‑launch checklist (ownership)
- [ ] Service account created and licensed.
- [ ] Service account added to the recipient group + SharePoint list.
- [ ] All connections in all four flows re‑authorized as the service account.
- [ ] Each flow has the service account **and** an IT group as co‑owners.
- [ ] No connection or owner is a personal / Tier‑0 admin account.
