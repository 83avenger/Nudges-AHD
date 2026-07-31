<#
  Create-List.ps1
  Creates the SharePoint List for the 4-nudges/day model (four pillars) with
  exact column types — no manual column clicking. Idempotent: safe to re-run.

  Creates: FourPillarNudges  (84 rows = 21 working days x 4 pillars)

  Requirements:
    - PnP.PowerShell module:  Install-Module PnP.PowerShell -Scope CurrentUser
    - Permission to create a list on the target site (site Member/Owner is
      enough; no tenant-admin rights needed).

  Usage:
    ./Create-List.ps1 -SiteUrl "https://<tenant>.sharepoint.com/sites/<YourSite>"

  Then load rows with ./Import-Data.ps1 (or the From-Excel / grid-paste routes
  in README.md).
#>

param(
  [Parameter(Mandatory = $true)][string]$SiteUrl
)

$ErrorActionPreference = 'Stop'
Connect-PnPOnline -Url $SiteUrl -Interactive

$Title = 'FourPillarNudges'
$list = Get-PnPList -Identity $Title -ErrorAction SilentlyContinue
if (-not $list) {
  Write-Host "Creating list '$Title'..." -ForegroundColor Cyan
  $list = New-PnPList -Title $Title -Template GenericList -OnQuickLaunch
  Set-PnPList -Identity $Title -Description 'Four-pillars 4x/day nudges (Social/Physical/Financial/Mental), bilingual.' | Out-Null
}
else { Write-Host "List '$Title' already exists - reusing." -ForegroundColor Yellow }

function Ensure-Field {
  param(
    [string]$Internal, [string]$Display, [string]$Type,
    [string[]]$Choices, [string]$Default, [switch]$DateOnly
  )
  if (Get-PnPField -List $Title -Identity $Internal -ErrorAction SilentlyContinue) {
    Write-Host "  field '$Internal' exists - skip" -ForegroundColor DarkGray; return
  }
  Write-Host "  + $Internal ($Type)" -ForegroundColor Green
  if ($Type -eq 'Choice') {
    Add-PnPField -List $Title -DisplayName $Display -InternalName $Internal -Type Choice -Choices $Choices -AddToDefaultView | Out-Null
    if ($Default) { Set-PnPField -List $Title -Identity $Internal -Values @{ DefaultValue = $Default } | Out-Null }
  }
  else {
    Add-PnPField -List $Title -DisplayName $Display -InternalName $Internal -Type $Type -AddToDefaultView | Out-Null
    if ($DateOnly) { Set-PnPField -List $Title -Identity $Internal -Values @{ DisplayFormat = 0 } | Out-Null } # 0 = Date only
  }
}

Ensure-Field 'Day'           'Day'           'Number'
Ensure-Field 'RevealDate'    'RevealDate'    'DateTime' -DateOnly
Ensure-Field 'DateLabel'     'DateLabel'     'Text'
Ensure-Field 'Weekday'       'Weekday'       'Text'
Ensure-Field 'WeekArc'       'WeekArc'       'Text'
Ensure-Field 'DailyThemeEN'  'DailyThemeEN'  'Text'
Ensure-Field 'DailyThemeAR'  'DailyThemeAR'  'Text'
Ensure-Field 'Pillar'        'Pillar'        'Choice' -Choices 'Social', 'Physical', 'Financial', 'Mental'
Ensure-Field 'PillarEN'      'PillarEN'      'Text'
Ensure-Field 'PillarAR'      'PillarAR'      'Text'
Ensure-Field 'PillarEmoji'   'PillarEmoji'   'Text'
Ensure-Field 'PillarOrder'   'PillarOrder'   'Number'
Ensure-Field 'SlotTime'      'SlotTime'      'Text'
Ensure-Field 'NudgeEN'       'NudgeEN'       'Note'
Ensure-Field 'NudgeAR'       'NudgeAR'       'Note'
Ensure-Field 'SourceRef'     'SourceRef'     'Text'
Ensure-Field 'Status'        'Status'        'Choice' -Choices 'Scheduled', 'Sent', 'Error' -Default 'Scheduled'
Ensure-Field 'SentDateTime'  'SentDateTime'  'Text'
Ensure-Field 'RunID'         'RunID'         'Text'

Write-Host "`nFourPillarNudges ready. Next: ./Import-Data.ps1 -SiteUrl '$SiteUrl'" -ForegroundColor Green
Disconnect-PnPOnline
