# bulk_rename_v1.0.ps1
# Safely rename eval scripts to _v1.0.py
# Dry-run mode first — no files changed until confirmed.

$evalDir = "src/evaluation"
$filesToRename = @(
    "demo_video_local.py",
    "demo_video_full.py",
    "jitter_showcase.py",
    "compute_jitter_score.py",
    "yolo_jitter_demo.py",
    "yolo_jitter_only.py"
)

$dryRun = $false    

Write-Host " Dry-run: Proposed renames in $evalDir" -ForegroundColor Cyan
Write-Host ("-" * 60)

$renamePlans = @()
foreach ($file in $filesToRename) {
    $src = Join-Path $evalDir $file
    $dst = Join-Path $evalDir ($file -replace '\.py$', '_v1.0.py')

    if (Test-Path $src) {
        if (Test-Path $dst) {
            Write-Host "⚠  SKIP (already exists): $dst" -ForegroundColor Yellow
        } else {
            $renamePlans += @{Source = $src; Destination = $dst}
            Write-Host " RENAME: $file → $($file -replace '\.py$', '_v1.0.py')" -ForegroundColor Green
        }
    } else {
        Write-Host " MISSING: $file" -ForegroundColor Red
    }
}

Write-Host ("-" * 60)
if ($renamePlans.Count -eq 0) {
    Write-Host "  No files to rename." -ForegroundColor Gray
    exit
}

if ($dryRun) {
    Write-Host " Dry-run complete. To execute, edit this script and set `$dryRun = `$false" -ForegroundColor Magenta
} else {
    Write-Host " Executing renames..." -ForegroundColor Green
    foreach ($plan in $renamePlans) {
        Rename-Item -Path $plan.Source -NewName (Split-Path $plan.Destination -Leaf)
        Write-Host " Renamed: $($plan.Source) → $($plan.Destination)" -ForegroundColor DarkGreen
    }
    Write-Host " Bulk rename completed." -ForegroundColor Green
}