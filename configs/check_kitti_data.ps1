# check_kitti_data.ps1 — Fully PowerShell-safe
# Save and run in: C:\Users\Suzan\Documents\GhostDet-KITTI

Write-Host " KITTI Data Audit — GhostDet Setup" -ForegroundColor Cyan
Write-Host ("=" * 70)

# Verify E: drive
if (-not (Test-Path "E:\")) {
    Write-Host "[FAIL] E: drive not connected." -ForegroundColor Red
    exit 1
}
Write-Host "[Ok]   E: drive connected" -ForegroundColor Green

$KITTI_ROOT = "E:\KITTI"
if (-not (Test-Path $KITTI_ROOT)) {
    Write-Host "[WARN] ${KITTI_ROOT} does not exist." -ForegroundColor Yellow
    exit 1
}

# List top-level folders
Write-Host "`n[INFO] Top-level folders in ${KITTI_ROOT}:" -ForegroundColor Cyan
Get-ChildItem $KITTI_ROOT -Directory | ForEach-Object {
    $count = (Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue).Count
    Write-Host "  $($_.Name) ($count files)"
}

# Check tracking sequences 0000–0020
Write-Host "`n[] Checking tracking sequences (0000–0020):" -ForegroundColor Cyan
$seqFound = @()
foreach ($i in 0..20) {
    $seqName = "{0:D4}" -f $i
    $seqPath = "${KITTI_ROOT}\tracking\${seqName}"
    $imgDir = "${seqPath}\image_02"
    $lblDir = "${seqPath}\label_02"
    
    $imgCount = 0; $lblCount = 0
    if (Test-Path $imgDir) { $imgCount = (Get-ChildItem "${imgDir}\*.png" -ErrorAction SilentlyContinue).Count }
    if (Test-Path $lblDir) { $lblCount = (Get-ChildItem "${lblDir}\*.txt" -ErrorAction SilentlyContinue).Count }
    
    if ($imgCount -gt 0 -or $lblCount -gt 0) {
        $status = if ($imgCount -eq $lblCount -and $imgCount -gt 1000) { "[OK]" } else { "[⚠️]" }
        Write-Host "  ${status} Seq ${seqName}: images=${imgCount}, labels=${lblCount}"
        $seqFound += $seqName
    }
}

if ($seqFound.Count -eq 0) {
    Write-Host "  [!] No full tracking sequences found." -ForegroundColor Red
}

#  Check for common ZIPs
Write-Host "`n[] Checking for unextracted ZIPs:" -ForegroundColor Cyan
$zipPaths = @(
    "${KITTI_ROOT}\data_tracking_image_2.zip",
    "${KITTI_ROOT}\data_tracking_label_2.zip",
    "${env:USERPROFILE}\Downloads\data_tracking_image_06.zip",
    "${env:USERPROFILE}\Downloads\data_tracking_label_06.zip"
)

foreach ($zip in $zipPaths) {
    if (Test-Path $zip) {
        $sizeMB = [Math]::Round((Get-Item $zip).Length / 1MB, 1)
        Write-Host "  [ZIP] ${zip} (${sizeMB} MB)"
    }
}

# Check seq 0006 structure
$seq06 = "${KITTI_ROOT}\tracking\0006"
if (Test-Path $seq06) {
    Write-Host "`n[] Folders in ${seq06}:" -ForegroundColor Cyan
    Get-ChildItem $seq06 -Directory | ForEach-Object { Write-Host "    $($_.Name)" }
    
    # Check for image_2 (wrong) vs image_02 (correct)
    if (Test-Path "${seq06}\image_2") { Write-Host "  [!] Found 'image_2' — should be 'image_02'" -ForegroundColor Red }
    if (Test-Path "${seq06}\label_2") { Write-Host "  [!] Found 'label_2' — should be 'label_02'" -ForegroundColor Red }
}

# Deep check seq 0006 content
$img06 = "${seq06}\image_02"
$lbl06 = "${seq06}\label_02"

if (Test-Path $img06 -and Test-Path $lbl06) {
    $imgCount = (Get-ChildItem "${img06}\*.png" -ErrorAction SilentlyContinue).Count
    $lblCount = (Get-ChildItem "${lbl06}\*.txt" -ErrorAction SilentlyContinue).Count
    
    Write-Host "`n[] Seq 0006 deep check:" -ForegroundColor Cyan
    Write-Host "  Images: ${imgCount} (expected: 1147)"
    Write-Host "  Labels: ${lblCount} (expected: 1147)"
    
    if ($imgCount -gt 0) {
        $sample = "${img06}\000000.png"
        if (Test-Path $sample) {
            $sizeKB = [Math]::Round((Get-Item $sample).Length / 1KB, 1)
            if ($sizeKB -gt 50) {
                Write-Host "  Sample image 000000.png: ${sizeKB} KB (OK)" -ForegroundColor Green
            } else {
                Write-Host "  [!] 000000.png too small (${sizeKB} KB) — may be corrupt" -ForegroundColor Red
            }
        } else {
            Write-Host "  [!] 000000.png missing" -ForegroundColor Red
        }
    }
}

Write-Host ("=" * 70)
Write-Host " Next: Ensure ${seq06}\image_02\ contains 1147 PNGs." -ForegroundColor Cyan