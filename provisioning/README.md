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

## ⚠️ If "From Excel/CSV" fails with *"Could not obtain a WAC access token"*

That error is a **SharePoint/Office-Online problem, not your data**. The
From-Excel/CSV wizard hands the file to Office Online (WAC) to parse it, and that
step fails intermittently — **especially with raw `.csv`**. Fixes, best first:

1. **Use PnP to load the data directly → Route B below + `Import-Data.ps1`.**
   This bypasses WAC and Power Automate entirely. Most reliable.
2. **Retry From-Excel with a real `.xlsx` Table** (not CSV): upload
   `../data/month-of-connection.xlsx` or `../data/four-pillars/by-nudge.xlsx`
   (each has a formatted Table). Excel Tables succeed where CSV's WAC step fails.
3. **Create the empty list first** (Route B `Create-Lists.ps1`), then **Edit in
   grid view** and paste the rows from the `.xlsx`/`.csv`. No WAC involved.
4. Retry later / different browser — WAC token errors are sometimes transient.

## Route A — Create list "From Excel" (no code, easiest *when WAC works*)

SharePoint can build a list and its columns automatically from a table.

1. In your SharePoint site: **+ New → List → From Excel**.
2. Upload the **.xlsx** (more reliable than CSV):
   - `../data/month-of-connection.xlsx` for the pilot list, **or**
   - `../data/four-pillars/by-nudge.xlsx` for the 4×/day list.
3. On the preview screen, **set the column types**:
   - `ChallengeEN/AR`, `NudgeEN/AR`, `WhyItMatters`, `TomorrowTeaser`,
     `SocialCaption` → **Multiple lines of text**. *(This is the "long text"
     option — the wizard calls it "Multiple lines of text", there is no separate
     "long text" entry.)*
   - `Status` (and `Pillar` for the 4-pillar list) → **Choice**.
   - `RevealDate` → **Date and time**, `Day`/`PillarOrder` → **Number** — **but
     only if the dropdown offers them.** The wizard shows Date/Number *only* for
     columns it detected as dates/numbers (more likely with the `.xlsx` than the
     `.csv`). If a column's dropdown only lists text/Choice/Title, you cannot set
     Date/Number here — see the note below.
4. Finish. **This also loads the rows**, so you can skip the separate import
   flow. Verify the Arabic renders right-to-left.

> **If Date/Number aren't offered:** either (a) after finishing, go to
> **List settings → the column → change type** to Date-only / Number — the reveal
> flow needs `RevealDate` to be a real **Date** column — or (b) use **Route B**,
> which sets every type correctly up front and avoids this entirely.

If this route errors or the types can't be set, use Route B.

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
list on that site — **no tenant-admin rights**.

### Load the rows the same way (no WAC, no Power Automate)
After the list exists, `Import-Data.ps1` writes every row straight into it via
PnP — the reliable answer to the WAC error:

```powershell
./Import-Data.ps1 -SiteUrl "https://<tenant>.sharepoint.com/sites/<YourSite>" -List MonthOfConnection
./Import-Data.ps1 -SiteUrl "https://<tenant>.sharepoint.com/sites/<YourSite>" -List FourPillarNudges
# reload cleanly (delete existing items first):
./Import-Data.ps1 -SiteUrl "..." -List MonthOfConnection -Fresh
```

It reads the JSON in `../data`, so Arabic, emoji and commas are preserved, and it
skips empty date/text fields correctly. Re-running appends unless you pass
`-Fresh`. This is the end-to-end path that avoids the From-Excel wizard entirely.

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

- **Hit the WAC token error?** → **Route B** (`Create-Lists.ps1` +
  `Import-Data.ps1`) — creates the list *and* loads the rows, no WAC.
- Just want it working now via the UI, WAC works → **Route A** with the **.xlsx**
  (loads the data too).
- Want exact types with one command, you own the site → **Route B**.
- Central IT wants a repeatable template → **Route C**.
