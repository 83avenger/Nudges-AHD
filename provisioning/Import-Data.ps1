<#
  Import-Data.ps1
  Loads the challenge rows straight into a SharePoint List via PnP — no Office
  Online / WAC, no Power Automate. Use this when the "From Excel/CSV" wizard
  fails with "Could not obtain a WAC access token".

  Reads the JSON datasets in ../data so Arabic, emoji and commas are preserved.

  Prereqs:
    - Install-Module PnP.PowerShell -Scope CurrentUser
    - The target list already exists (run Create-Lists.ps1 first).
    - Permission to add items to the list.

  Usage:
    ./Import-Data.ps1 -SiteUrl "https://<tenant>.sharepoint.com/sites/<Site>" -List MonthOfConnection
    ./Import-Data.ps1 -SiteUrl "https://<tenant>.sharepoint.com/sites/<Site>" -List FourPillarNudges

  Re-running APPENDS rows. To reload cleanly, pass -Fresh to delete existing
  items first.
#>

param(
  [Parameter(Mandatory = $true)][string]$SiteUrl,
  [Parameter(Mandatory = $true)][ValidateSet('MonthOfConnection', 'FourPillarNudges')][string]$List,
  [switch]$Fresh
)

$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path

if ($List -eq 'MonthOfConnection') {
  $jsonPath = Join-Path $here '..\data\month-of-connection.json'
  $fields = @('Day', 'RevealDate', 'DateLabel', 'Weekday', 'WeekArc', 'ChallengeEN',
    'ChallengeAR', 'WhyItMatters', 'TomorrowTeaser', 'SocialCaption',
    'SourceRef', 'Status', 'SentDateTime', 'RunID')
  $titleField = 'Day'
}
else {
  $jsonPath = Join-Path $here '..\data\four-pillars\by-nudge.json'
  $fields = @('Day', 'RevealDate', 'DateLabel', 'Weekday', 'WeekArc', 'DailyThemeEN',
    'DailyThemeAR', 'Pillar', 'PillarEN', 'PillarAR', 'PillarEmoji',
    'PillarOrder', 'SlotTime', 'NudgeEN', 'NudgeAR', 'SourceRef',
    'Status', 'SentDateTime', 'RunID')
  $titleField = $null  # Title set to "Day-Pillar" below
}

$rows = Get-Content -Raw -Encoding UTF8 $jsonPath | ConvertFrom-Json
Write-Host "Loaded $($rows.Count) rows from $(Split-Path -Leaf $jsonPath)" -ForegroundColor Cyan

Connect-PnPOnline -Url $SiteUrl -Interactive

if ($Fresh) {
  Write-Host "Deleting existing items in '$List'..." -ForegroundColor Yellow
  Get-PnPListItem -List $List -PageSize 500 | ForEach-Object {
    Remove-PnPListItem -List $List -Identity $_.Id -Force | Out-Null
  }
}

$n = 0
foreach ($r in $rows) {
  $values = @{}
  foreach ($f in $fields) {
    $val = $r.$f
    if ($null -eq $val) { $val = '' }
    # empty date must be omitted, not sent as '' (invalid for a Date column)
    if ($f -eq 'RevealDate' -and [string]::IsNullOrWhiteSpace([string]$val)) { continue }
    if (($f -eq 'SentDateTime' -or $f -eq 'RunID') -and [string]::IsNullOrWhiteSpace([string]$val)) { continue }
    $values[$f] = $val
  }
  if ($List -eq 'MonthOfConnection') { $values['Title'] = [string]$r.Day }
  else { $values['Title'] = "$($r.Day)-$($r.Pillar)" }

  Add-PnPListItem -List $List -Values $values | Out-Null
  $n++
  if ($n % 20 -eq 0) { Write-Host "  ...$n added" -ForegroundColor DarkGray }
}

Write-Host "Done. Added $n items to '$List'." -ForegroundColor Green
Disconnect-PnPOnline
