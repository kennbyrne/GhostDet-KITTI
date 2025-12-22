# audit_full.ps1 
# Scans E:\KITTI\_temp_extract for usable KITTI sequences

Write-Host " Scanning extracted KITTI data..." -ForegroundColor Cyan

# Paths
$imgRoot = "E:\KITTI\_temp_extract\img"
$lblRoot = "E:\KITTI\_temp_extract\lbl"

# Check existence
if (-not (Test-Path $imgRoot)) { 
    Write-Host "[!] Image extraction not found at $imgRoot" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path $lblRoot)) { 
    Write-Host "[!] Label extraction not found at $lblRoot" -ForegroundColor Red
    exit 1
}

# Find seq 0006 explicitly
$seqId = "0006"

# Try common image paths
$imgPaths = @(
    "$imgRoot\training\$seqId\image_02",
    "$imgRoot\training\image_02\$seqId",
    "$imgRoot\$seqId\image_02"
)
$lblPaths = @(
    "$lblRoot\training\$seqId\label_02",
    "$lblRoot\training\label_02\$seqId",
    "$lblRoot\$seqId\label_02"
)

$imgCount = 0; $lblCount = 0; $foundImg = $null; $foundLbl = $null

foreach ($p in $imgPaths) {
    if (Test-Path $p) {
        $cnt = (Get-ChildItem "$p\*.png" -ErrorAction SilentlyContinue).Count
        if ($cnt -gt $imgCount) {
            $imgCount = $cnt
            $foundImg = $p
        }
    }
}

foreach ($p in $lblPaths) {
    if (Test-Path $p) {
        $cnt = (Get-ChildItem "$p\*.txt" -ErrorAction SilentlyContinue).Count
        if ($cnt -gt $lblCount) {
            $lblCount = $cnt
            $foundLbl = $p
        }
    }
}

# Report
Write-Host "`n[] Sequence $seqId status:" -ForegroundColor Green
Write-Host "  Images: $imgCount" -NoNewline
if ($foundImg) { Write-Host " (found at: $foundImg)" -ForegroundColor Gray }
else { Write-Host " (not found)" -ForegroundColor Red }

Write-Host "  Labels: $lblCount" -NoNewline
if ($foundLbl) { Write-Host " (found at: $foundLbl)" -ForegroundColor Gray }
else { Write-Host " (not found)" -ForegroundColor Red }

# Summary
if ($imgCount -ge 100 -and $lblCount -ge 100) {
    Write-Host "`n Full sequence ready for GhostDet!" -ForegroundColor Green
} elseif ($imgCount -gt 0) {
    Write-Host "`n Partial sequence — usable for local demo (e.g., 270 frames)" -ForegroundColor Yellow
} else {
    Write-Host "`n No frames found. Check extraction." -ForegroundColor Red
}

Write-Host "`n Tip: Even 100+ frames enable GhostDet's motion-stabilization demo." -ForegroundColor Cyan