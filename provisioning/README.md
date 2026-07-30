# Auto-create the SharePoint Lists (no manual column building)

Three ways to create the lists from a schema instead of clicking columns by hand.
Pick by how much access you have. All create the same columns described in
`../sharepoint-list-schema.md` and `../four-pillars-sharepoint-schema.md`.

| Route | Who can run it | Column types exact? | Effort |
|-------|----------------|---------------------|--------|
| **A · From Excel/CSV** | Anyone who can create a list | Mostly (fix 2–3 types after) | Easiest, no code |
| **B · PnP PowerShell** (`Create-Lists.ps1`) | Site Member/Owner | Yes | One command |
| **C · Site script** (`site-script-*.json`) | SharePoint **admin** | Yes | Admin setup |

> Note: the Markdown schema docs are for humans — SharePoint can't ingest them
> directly. Use one of the routes below.

---

## Route A — Create list "From Excel" (no code, easiest)

SharePoint can build a list and its columns automatically from a table.

1. In your SharePoint site: **+ New → List → From Excel** (or **From CSV**).
2. Upload:
   - `../data/month-of-connection.csv` for the pilot list, **or**
   - `../data/four-pillars/by-nudge.csv` for the 4×/day list.
3. On the preview screen, **set the column types** SharePoint can't infer:
   - `RevealDate` → **Date and time** (Date only).
   - `Status` (and `Pillar` for the 4-pillar list) → **Choice**.
   - Long text (`ChallengeEN/AR`, `NudgeEN/AR`, `WhyItMatters`, …) → **Multiple
     lines of text**.
   - `Day`, `PillarOrder` → **Number**.
4. Finish. **This also loads the rows**, so you can skip the separate import
   flow. Verify the Arabic renders right-to-left.

Trade-off: types are inferred from the data, so you adjust a few. Fastest path
if you just want it done.

---

## Route B — PnP PowerShell (precise, recommended for a site owner)

`Create-Lists.ps1` creates both lists with the **exact** column types (Choice,
Date-only, Number, Note) and the `Status` default of `Scheduled`. Idempotent —
re-running skips what already exists.

```powershell
# one-time
Install-Module PnP.PowerShell -Scope CurrentUser

# create both lists on your site
./Create-Lists.ps1 -SiteUrl "https://<tenant>.sharepoint.com/sites/<YourSite>"

# or just one:
./Create-Lists.ps1 -SiteUrl "https://<tenant>.sharepoint.com/sites/<YourSite>" -Only FourPillarNudges
```

It signs in interactively (`-Interactive`) and needs only permission to create a
list on that site — **no tenant-admin rights**. After it finishes, load rows via
the import flow (`../import-flow-guide.md`) or Route A step 4.

> If your org blocks the default PnP app registration, an admin may need to
> consent once (or supply a `-ClientId`). See the PnP.PowerShell docs.

---

## Route C — Site script / site design (admin route, reusable template)

`site-script-MonthOfConnection.json` is a SharePoint **site script** that creates
the list with correct types (Choice + date-only via field XML). Register and
apply it with tenant-admin PowerShell:

```powershell
# Requires: Microsoft.Online.SharePoint.PowerShell + SharePoint admin
Connect-SPOService -Url "https://<tenant>-admin.sharepoint.com"

$script = Get-Content ./site-script-MonthOfConnection.json -Raw
$s = Add-SPOSiteScript -Title "AHD MonthOfConnection List" -Content $script
$d = Add-SPOSiteDesign -Title "AHD MonthOfConnection" -SiteScripts $s.Id -WebTemplate "64"

# then apply to your site:
Invoke-SPOSiteDesign -Identity $d.Id -WebUrl "https://<tenant>.sharepoint.com/sites/<YourSite>"
```

Use this when you want a **reusable, governed template** across sites. For the
4-pillar list, mirror the same file with the columns from
`../four-pillars-sharepoint-schema.md` (or just use Route B, which already does
both).

---

## Which should I use?

- Just want it working now, one site → **Route A** (and it loads the data too).
- Want exact types with one command, you own the site → **Route B**.
- Central IT wants a repeatable template → **Route C**.
