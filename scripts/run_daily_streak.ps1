# Run Daily Streak & Refresh Profile Locally
# Can be run manually anytime or scheduled via Windows Task Scheduler

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RepoDir = Split-Path -Parent $ScriptDir
Set-Location $RepoDir

Write-Host "Syncing with GitHub..." -ForegroundColor Cyan
git pull origin main --quiet

Write-Host "Updating daily activity..." -ForegroundColor Green
& "$RepoDir\.venv\Scripts\python.exe" "$RepoDir\scripts\daily_log.py"

Write-Host "Fetching contributions and refreshing heatmap..." -ForegroundColor Green
& "$RepoDir\.venv\Scripts\python.exe" "$RepoDir\scripts\fetch_contributions.py"
& "$RepoDir\.venv\Scripts\python.exe" "$RepoDir\scripts\render_heatmap_svg.py"

Write-Host "Committing and pushing to GitHub..." -ForegroundColor Cyan
git add data/activity.log data/contributions.json contrib-heatmap.svg

$changes = git status --porcelain
if ($changes) {
    git commit -m "activity: daily developer log and profile refresh [skip ci]"
    git push origin main
    Write-Host "Successfully pushed today's streak to GitHub!" -ForegroundColor Green
} else {
    Write-Host "No changes to commit." -ForegroundColor Yellow
}
