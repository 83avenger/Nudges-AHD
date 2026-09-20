# Runbooks — AHD Wellbeing365

Operational runbooks for launch and for the optional branded sender. Each has a
paste‑ready IT request and a checklist.

| Runbook | Purpose | Owner |
|---------|---------|-------|
| `service-account-setup.md` | **Required before go‑live.** Move flow connections to a dedicated service account (fixes the Tier‑0 `AADSTS135010` token errors). | IT Identity + Power Platform |
| `copilot-studio-payg-setup.md` | *Optional.* Enable Copilot Studio pay‑as‑you‑go so the "AHD Thrive365" agent can post as the branded sender. | Power Platform + Azure admin |
| `azure-cost-management-setup.md` | *Optional (with the above).* Budget, alerts, and the per‑card cost measurement test. | Azure admin |

Order: **service account first** (launch‑blocking), then — only if leadership
wants the branded sender — **cost management → PAYG enablement → publish → measure**.
