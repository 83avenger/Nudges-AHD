<#
  Import-Data.ps1
  Loads the 84 nudge rows straight into the FourPillarNudges list via PnP — no
  Office Online / WAC, no Power Automate. Use this when the "From Excel/CSV"
  wizard fails with "Could not obtain a WAC access token".

  Reads data/four-pillars/by-nudge.json so Arabic, emoji and commas are preserved.

  Prereqs:
    - Install-Module PnP.PowerShell -Scope CurrentUser
    - The list already exists (run Create-List.ps1 first).
    - Permission to add items to the list.

  Usage:
    ./Import-Data.ps1 -SiteUrl "https://<tenant>.sharepoint.com/sites/<Site>"
    ./Import-Data.ps1 -SiteUrl "..." -Fresh   # delete existing items first
#>

param(
  [Parameter(Mandatory = $true)][string]$SiteUrl,
  [string]$ClientId,   # see Create-List.ps1 / provisioning/README.md
  [switch]$Fresh
)

$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$List = 'FourPillarNudges'
$jsonPath = Join-Path $here '..\data\four-pillars\by-nudge.json'
$fields = @('Day', 'RevealDate', 'DateLabel', 'Weekday', 'WeekArc', 'DailyThemeEN',
  'DailyThemeAR', 'Pillar', 'PillarEN', 'PillarAR', 'PillarEmoji',
  'PillarOrder', 'SlotTime', 'NudgeEN', 'NudgeAR', 'SourceRef',
  'Status', 'SentDateTime', 'RunID')

$rows = Get-Content -Raw -Encoding UTF8 $jsonPath | ConvertFrom-Json
Write-Host "Loaded $($rows.Count) rows from by-nudge.json" -ForegroundColor Cyan

if ($ClientId) { Connect-PnPOnline -Url $SiteUrl -Interactive -ClientId $ClientId }
else { Connect-PnPOnline -Url $SiteUrl -Interactive }

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
    if ($f -eq 'RevealDate' -and [string]::IsNullOrWhiteSpace([string]$val)) { continue }
    if (($f -eq 'SentDateTime' -or $f -eq 'RunID') -and [string]::IsNullOrWhiteSpace([string]$val)) { continue }
    $values[$f] = $val
  }
  $values['Title'] = "$($r.Day)-$($r.Pillar)"
  Add-PnPListItem -List $List -Values $values | Out-Null
  $n++
  if ($n % 20 -eq 0) { Write-Host "  ...$n added" -ForegroundColor DarkGray }
}

Write-Host "Done. Added $n items to '$List'." -ForegroundColor Green
Disconnect-PnPOnline
