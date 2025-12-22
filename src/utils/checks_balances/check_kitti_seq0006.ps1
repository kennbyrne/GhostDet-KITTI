# check_kitti_seq0006.ps1
# Checks common KITTI paths on E:\ for seq-0006 (full: ≥1000 frames)
param(
    [string]$Drive = "E"
)

$candidates = @(
    "$($Drive):\KITTI\tracking\0006\image_02",        
    "$($Drive):\KITTI\_temp_extract\img\training\image_02\0006",
    "$($Drive):\KITTI\training\image_02\0006"
)

Write-Host " Scanning ${Drive}:\ for KITTI seq-0006 (full sequence)..." -ForegroundColor Cyan

$found = $null
foreach ($path in $candidates) {
    if (Test-Path $path) {
        $count = (Get-ChildItem $path -Filter "*.png" | Measure-Object).Count
        Write-Host "  ✅ $path → $count frames" -ForegroundColor Green
        if ($count -ge 1000) {
            $found = $path
            break
        }
    } else {
        Write-Host "   $path → Not found" -ForegroundColor DarkGray
    }
}

if ($found) {
    Write-Host "`n Full seq-0006 found at:`n$found" -ForegroundColor Magenta
    # Output to file for Python consumption
    $found | Set-Content -Path "src/utils/checks_balances/kitti_seq0006_path.txt" -Encoding UTF8
    Write-Host "`n Path saved to: src/utils/checks_balances/kitti_seq0006_path.txt"
} else {
    Write-Host "`n  No full seq-0006 found. Expected ≥1000 frames." -ForegroundColor Yellow
    Write-Host "   Searched paths:"
    $candidates | ForEach-Object { Write-Host "   - $_" }
}

exit ($null -eq $found)  # Exit 0 = found, 1 = not found