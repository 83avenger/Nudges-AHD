<#
  Create-Lists.ps1
  Creates the SharePoint Lists for the AHD Wellbeing365 automation with exact
  column types — no manual column clicking. Idempotent: safe to re-run (it skips
  lists/fields that already exist).

  Creates:
    - MonthOfConnection   (one hero challenge/day pilot)
    - FourPillarNudges    (four-pillars 4x/day variant)

  Requirements:
    - PnP.PowerShell module:  Install-Module PnP.PowerShell -Scope CurrentUser
    - Permission to create lists on the target site (site Member/Owner is enough;
      no tenant-admin rights needed for this script).

  Usage:
    Connect once, then run. Example:
      ./Create-Lists.ps1 -SiteUrl "https://<tenant>.sharepoint.com/sites/<YourSite>"
    You can create only one list with -Only MonthOfConnection  (or FourPillarNudges).

  After the lists exist, load rows with the import flow (import-flow-guide.md)
  or the "From Excel/CSV" quick path in provisioning/README.md.
#>

param(
  [Parameter(Mandatory = $true)][string]$SiteUrl,
  [ValidateSet('Both', 'MonthOfConnection', 'FourPillarNudges')]
  [string]$Only = 'Both'
)

$ErrorActionPreference = 'Stop'
Connect-PnPOnline -Url $SiteUrl -Interactive

function Ensure-List {
  param([string]$Title, [string]$Description)
  $list = Get-PnPList -Identity $Title -ErrorAction SilentlyContinue
  if (-not $list) {
    Write-Host "Creating list '$Title'..." -ForegroundColor Cyan
    $list = New-PnPList -Title $Title -Template GenericList -OnQuickLaunch
    if ($Description) { Set-PnPList -Identity $Title -Description $Description | Out-Null }
  }
  else { Write-Host "List '$Title' already exists - reusing." -ForegroundColor Yellow }
  return $Title
}

function Ensure-Field {
  param(
    [string]$List, [string]$Internal, [string]$Display, [string]$Type,
    [string[]]$Choices, [string]$Default, [switch]$DateOnly
  )
  $existing = Get-PnPField -List $List -Identity $Internal -ErrorAction SilentlyContinue
  if ($existing) { Write-Host "  field '$Internal' exists - skip" -ForegroundColor DarkGray; return }
  Write-Host "  + $Internal ($Type)" -ForegroundColor Green
  if ($Type -eq 'Choice') {
    Add-PnPField -List $List -DisplayName $Display -InternalName $Internal -Type Choice -Choices $Choices -AddToDefaultView | Out-Null
    if ($Default) { Set-PnPField -List $List -Identity $Internal -Values @{ DefaultValue = $Default } | Out-Null }
  }
  else {
    Add-PnPField -List $List -DisplayName $Display -InternalName $Internal -Type $Type -AddToDefaultView | Out-Null
    if ($DateOnly) { Set-PnPField -List $List -Identity $Internal -Values @{ DisplayFormat = 0 } | Out-Null } # 0 = Date only
  }
}

# --------------------------------------------------------------------------
if ($Only -in @('Both', 'MonthOfConnection')) {
  $L = Ensure-List -Title 'MonthOfConnection' -Description 'Month of Connection - one bilingual challenge per working day.'
  Ensure-Field $L 'Day'            'Day'             'Number'
  Ensure-Field $L 'RevealDate'     'RevealDate'      'DateTime' -DateOnly
  Ensure-Field $L 'DateLabel'      'DateLabel'       'Text'
  Ensure-Field $L 'Weekday'        'Weekday'         'Text'
  Ensure-Field $L 'WeekArc'        'WeekArc'         'Text'
  Ensure-Field $L 'ChallengeEN'    'ChallengeEN'     'Note'
  Ensure-Field $L 'ChallengeAR'    'ChallengeAR'     'Note'
  Ensure-Field $L 'WhyItMatters'   'WhyItMatters'    'Note'
  Ensure-Field $L 'TomorrowTeaser' 'TomorrowTeaser'  'Note'
  Ensure-Field $L 'SocialCaption'  'SocialCaption'   'Note'
  Ensure-Field $L 'SourceRef'      'SourceRef'       'Text'
  Ensure-Field $L 'Status'         'Status'          'Choice' -Choices 'Scheduled', 'Sent', 'Error' -Default 'Scheduled'
  Ensure-Field $L 'SentDateTime'   'SentDateTime'    'Text'
  Ensure-Field $L 'RunID'          'RunID'           'Text'
  Write-Host "MonthOfConnection ready.`n" -ForegroundColor Cyan
}

# --------------------------------------------------------------------------
if ($Only -in @('Both', 'FourPillarNudges')) {
  $L = Ensure-List -Title 'FourPillarNudges' -Description 'Four-pillars 4x/day nudges (Social/Physical/Financial/Mental), bilingual.'
  Ensure-Field $L 'Day'           'Day'           'Number'
  Ensure-Field $L 'RevealDate'    'RevealDate'    'DateTime' -DateOnly
  Ensure-Field $L 'DateLabel'     'DateLabel'     'Text'
  Ensure-Field $L 'Weekday'       'Weekday'       'Text'
  Ensure-Field $L 'WeekArc'       'WeekArc'       'Text'
  Ensure-Field $L 'DailyThemeEN'  'DailyThemeEN'  'Text'
  Ensure-Field $L 'DailyThemeAR'  'DailyThemeAR'  'Text'
  Ensure-Field $L 'Pillar'        'Pillar'        'Choice' -Choices 'Social', 'Physical', 'Financial', 'Mental'
  Ensure-Field $L 'PillarEN'      'PillarEN'      'Text'
  Ensure-Field $L 'PillarAR'      'PillarAR'      'Text'
  Ensure-Field $L 'PillarEmoji'   'PillarEmoji'   'Text'
  Ensure-Field $L 'PillarOrder'   'PillarOrder'   'Number'
  Ensure-Field $L 'SlotTime'      'SlotTime'      'Text'
  Ensure-Field $L 'NudgeEN'       'NudgeEN'       'Note'
  Ensure-Field $L 'NudgeAR'       'NudgeAR'       'Note'
  Ensure-Field $L 'SourceRef'     'SourceRef'     'Text'
  Ensure-Field $L 'Status'        'Status'        'Choice' -Choices 'Scheduled', 'Sent', 'Error' -Default 'Scheduled'
  Ensure-Field $L 'SentDateTime'  'SentDateTime'  'Text'
  Ensure-Field $L 'RunID'         'RunID'         'Text'
  Write-Host "FourPillarNudges ready.`n" -ForegroundColor Cyan
}

Write-Host "Done. Next: load rows via import-flow-guide.md or the From-Excel path." -ForegroundColor Green
Disconnect-PnPOnline
