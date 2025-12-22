# src/utils/checks_balances/check_kitti_structure.ps1
param(
    [string]$BasePath = "E:\KITTI"
)

Write-Host "🔍 Deep scan for '0006' in $BasePath..." -ForegroundColor Cyan

# Recursively find all directories containing "0006"
$dirs = Get-ChildItem -Path $BasePath -Recurse -Directory | 
        Where-Object { $_.Name -like "*0006*" -or $_.Parent.Name -like "*0006*" }

if ($dirs.Count -eq 0) {
    Write-Host "⚠️  No directories with '0006' found in $BasePath" -ForegroundColor Yellow
    return
}

# Scan each candidate dir for PNGs and label files
foreach ($dir in $dirs) {
    # Count PNGs (direct + recursive)
    $pngs = Get-ChildItem -Path $dir -Filter "*.png" -Recurse -ErrorAction SilentlyContinue
    $pngCount = $pngs.Count

    if ($pngCount -gt 0) {
        Write-Host "📁 $dir" -ForegroundColor Green
        Write-Host "  → $pngCount PNGs" -ForegroundColor DarkGreen
    }

    # Look for label files in same or parent dirs
    $labelCandidates = @(
        "$dir\0006.txt",
        "$dir\label_02\0006.txt",
        "$($dir.Parent)\label_02\0006.txt",
        "$($dir.Parent.Parent)\label_02\0006.txt"
    ) | Where-Object { Test-Path $_ }

    foreach ($label in $labelCandidates) {
        $lines = (Get-Content $label | Measure-Object -Line).Lines
        Write-Host "  🏷️  $label → $lines lines" -ForegroundColor Magenta
    }
}

# Bonus: Check for standard KITTI MOT paths explicitly
$standardPaths = @(
    "E:\KITTI\tracking\0006\image_02",
    "E:\KITTI\training\image_02\0006",
    "E:\KITTI\data_tracking_image_2\training\image_02\0006"
)
Write-Host "`n🔍 Standard KITTI MOT paths:" -ForegroundColor Cyan
foreach ($path in $standardPaths) {
    if (Test-Path $path) {
        $count = (Get-ChildItem $path -Filter "*.png" -Recurse | Measure-Object).Count
        Write-Host "  ✅ $path → $count PNGs" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $path → Not found" -ForegroundColor DarkGray
    }
}