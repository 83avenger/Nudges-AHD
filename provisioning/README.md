# Auto-create the `FourPillarNudges` SharePoint List (no manual columns)

Three ways to create the list from a schema instead of clicking columns by hand.
All create the same columns described in `../four-pillars-sharepoint-schema.md`.

| Route | Who can run it | Column types exact? | Effort |
|-------|----------------|---------------------|--------|
| **A · From Excel** | Anyone who can create a list | Mostly (fix 2–3 types after) | Easiest, no code |
| **B · PnP PowerShell** (`Create-List.ps1` + `Import-Data.ps1`) | Site Member/Owner | Yes | Two commands, creates **and** loads |
| **C · Site script** (`site-script-FourPillarNudges.json`) | SharePoint **admin** | Yes | Reusable template |

---

## ⚠️ If "From Excel" fails with *"Could not obtain a WAC access token"*

That's a **SharePoint/Office-Online problem, not your data** — the wizard hands
the file to Office Online to parse it and that step fails intermittently
(worse with raw `.csv`). Fixes, best first:

1. **Route B** — `Create-List.ps1` + `Import-Data.ps1`. Bypasses WAC entirely.
2. Retry From-Excel with the **.xlsx** (`../data/four-pillars/by-nudge.xlsx`),
   which has a real Table — more reliable than CSV.
3. Create the empty list (Route B `Create-List.ps1`), then **Edit in grid view**
   and paste rows from the `.xlsx`.

---

> **⚠️ From-Excel renames your columns internally.** Importing from a spreadsheet
> keeps your headers as *display* names but sets the permanent **internal** names
> to `field_1`, `field_2`, … . Power Automate filters use **internal** names, so
> you'll hit *"Column 'Pillar' does not exist"* even though the list shows
> `Pillar`. **Route B (PnP) or a Blank list + Add column keep internal names = the
> real names** (`Pillar`, `Day`, `Status`). Prefer those if you'll query the list
> from a flow — which this project does.

## Route A — From Excel (no code, easiest when WAC works)

1. Site → **+ New → List → From Excel**.
2. Upload **`../data/four-pillars/by-nudge.xlsx`** (not CSV).
3. Set column types:
   - `NudgeEN`, `NudgeAR` → **Multiple lines of text** (this *is* the "long text"
     option — there is no separate "long text").
   - `Status`, `Pillar` → **Choice**.
   - `RevealDate` → **Date**, `Day`/`PillarOrder` → **Number** — **only if the
     dropdown offers them**. If a column shows only text/Choice/Title, set it
     after import in **List settings → column → change type** (the flow needs
     `Day` as **Number** for ordering), or use Route B.
4. Finish. This also loads the rows. Verify Arabic renders right-to-left.

---

## Route B — PnP PowerShell (recommended: exact types + loads data)

**Prerequisites (one-time):**
```powershell
Install-Module PnP.PowerShell -Scope CurrentUser -Force -AllowClobber
$PSVersionTable.PSVersion    # PnP.PowerShell needs PowerShell 7
```
- If `Connect-PnPOnline is not recognized` → the module isn't installed; run the
  Install line above.
- If `$PSVersionTable.PSVersion` **Major is 5** (classic Windows PowerShell) →
  **PnP.PowerShell does not run on 5.1 at any version.** Install **PowerShell 7**
  (`winget install --id Microsoft.PowerShell --source winget`, then reopen the
  *PowerShell 7* / `pwsh` app) and run the module install + scripts there. If you
  can't install PS7, use the **no-install GUI route** below instead.
- **PnP.PowerShell 2.x needs your own Entra ID app** (Microsoft retired the
  built-in one). If login warns *"Please specify a valid client id"* /
  *"Specified method is not supported"*, register an app once:
  ```powershell
  Register-PnPEntraIDAppForInteractiveLogin -ApplicationName "PnP-Nudges" -Tenant <tenant>.onmicrosoft.com
  ```
  (No `-Interactive` switch — it opens a browser by default. Requires rights to
  register an app **and** admin consent to the requested permissions.)
  Copy the **Client Id** it prints, then pass it to the scripts via `-ClientId`.
  (Registering needs rights to create an app registration; if that's blocked, use
  the GUI route below.)

**Run** (add `-ClientId <id>` if you registered an app above):
```powershell
./Create-List.ps1 -SiteUrl "https://<tenant>.sharepoint.com/sites/<YourSite>" -ClientId <app-id>
./Import-Data.ps1 -SiteUrl "https://<tenant>.sharepoint.com/sites/<YourSite>" -ClientId <app-id>
# reload cleanly: add -Fresh to Import-Data
```

Signs in interactively; needs only permission to create/add on that site — **no
tenant-admin rights**. No WAC, no Power Automate. Arabic/emoji/commas preserved.

> Not worth the install? Use the **Blank list + Add column** GUI route
> (`../IMPLEMENTATION-GUIDE-GUI.md` Steps 2–3) — no PowerShell, and it keeps
> column internal names correct (unlike *From Excel*).

---

## Route C — Site script (admin, reusable template)

`site-script-FourPillarNudges.json` creates the list with correct types via a
site script. Register and apply with tenant-admin PowerShell:

```powershell
Connect-SPOService -Url "https://<tenant>-admin.sharepoint.com"
$script = Get-Content ./site-script-FourPillarNudges.json -Raw
$s = Add-SPOSiteScript -Title "AHD FourPillarNudges List" -Content $script
$d = Add-SPOSiteDesign -Title "AHD FourPillarNudges" -SiteScripts $s.Id -WebTemplate "64"
Invoke-SPOSiteDesign -Identity $d.Id -WebUrl "https://<tenant>.sharepoint.com/sites/<YourSite>"
```

Then load rows with Route B's `Import-Data.ps1`, the From-Excel `.xlsx`, or
grid-paste.

---

## Which should I use?

- **Hit the WAC error?** → **Route B** (creates the list *and* loads the rows).
- Want the UI, WAC works → **Route A** with the **.xlsx**.
- Central IT wants a repeatable template → **Route C** (+ Import-Data for rows).
