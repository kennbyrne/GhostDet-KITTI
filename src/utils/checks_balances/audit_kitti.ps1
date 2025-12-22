# audit_kitti.ps1
# Recursively checks E:\KITTI\ for correct KITTI structure — GhostDet-ready

Write-Host " FULL KITTI AUDIT — Recursive Folder Scan" -ForegroundColor Cyan
Write-Host ("=" * 70)

# Verify E: drive
if (-not (Test-Path "E:\")) {
    Write-Host " E: drive not connected." -ForegroundColor Red
    exit 1
}
Write-Host " E: drive connected" -ForegroundColor Green

$KITTI_ROOT = "E:\KITTI"
if (-not (Test-Path $KITTI_ROOT)) {
    Write-Host " $KITTI_ROOT does not exist." -ForegroundColor Red
    exit 1
}

# List all folders recursively (depth 3 — enough for KITTI)
Write-Host "`n Top-level & key subfolders (depth ≤ 3):" -ForegroundColor Cyan
Get-ChildItem $KITTI_ROOT -Recurse -Directory -Depth 3 | ForEach-Object {
    $relPath = $_.FullName.Substring($KITTI_ROOT.Length + 1)
    Write-Host "  $relPath"
}

# Check for common problematic patterns
Write-Host "`n Diagnostic Checks:" -ForegroundColor Cyan

# a) Is there a top-level image_02 or label_02? (sign of flat extraction)
$flatImage = Test-Path "$KITTI_ROOT\image_02"
$flatLabel = Test-Path "$KITTI_ROOT\label_02"
if ($flatImage -or $flatLabel) {
    Write-Host "  Top-level 'image_02' or 'label_02' found — likely flat extraction (should be in seq folders)"
}

# b) Is tracking\ empty or shallow?
$trackingDir = "$KITTI_ROOT\tracking"
if (Test-Path $trackingDir) {
    $trackingSubs = Get-ChildItem $trackingDir -Directory
    Write-Host "   tracking\ has $($trackingSubs.Count) subfolders"
    if ($trackingSubs.Count -eq 0) {
        Write-Host "   tracking\ is empty — sequences not moved in"
    } elseif ($trackingSubs.Count -lt 5) {
        # Check if any are seq-style (0000–0020)
        $seqDirs = $trackingSubs | Where-Object { $_.Name -match '^\d{4}$' }
        if ($seqDirs.Count -eq 0) {
            Write-Host "  No numbered sequence folders (e.g., 0006) in tracking\"
        } else {
            Write-Host "  Found $($seqDirs.Count) sequence folders: $($seqDirs.Name -join ', ')"
        }
    }
} else {
    Write-Host "  tracking\ folder missing"
}

# c) Check data_tracking_*\training\ for sequences
$trainImg = "$KITTI_ROOT\data_tracking_image_2\training"
$trainLbl = "$KITTI_ROOT\data_tracking_label_2\training"

if (Test-Path $trainImg) {
    $trainSeqs = Get-ChildItem $trainImg -Directory | Where-Object { $_.Name -match '^\d{4}$' }
    Write-Host " data_tracking_image_2\training\ has $($trainSeqs.Count) seq folders"
    if ($trainSeqs.Count -gt 0) {
        Write-Host "      Sample: $($trainSeqs[0..2].Name -join ', ')..."
    }
} else {
    Write-Host " data_tracking_image_2\training\ not found"
}

# d) Deep check seq 0006 (if exists anywhere)
$seqCandidates = @()
# Search in common places
@(
    "$KITTI_ROOT\tracking\0006",
    "$KITTI_ROOT\training\0006",
    "$KITTI_ROOT\data_tracking_image_2\training\0006",
    "$KITTI_ROOT\0006"
) | ForEach-Object {
    if (Test-Path "$_\image_02") { $seqCandidates += $_ }
}

if ($seqCandidates.Count -gt 0) {
    Write-Host "`n Found seq 0006 candidates:" -ForegroundColor Green
    foreach ($cand in $seqCandidates) {
        $imgCnt = (Get-ChildItem "$cand\image_02\*.png" -ErrorAction SilentlyContinue).Count
        $lblCnt = (Get-ChildItem "$cand\label_02\*.txt" -ErrorAction SilentlyContinue).Count
        Write-Host "  $cand → images: $imgCnt, labels: $lblCnt"
        if ($imgCnt -ge 1000 -and $imgCnt -eq $lblCnt) {
            Write-Host "     FULL sequence ready!" -ForegroundColor Green
        } elseif ($imgCnt -gt 0) {
            Write-Host "     Partial — needs labels or more frames" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "`n No seq 0006 found. Expected locations checked." -ForegroundColor Yellow
}

# 4. Final recommendation
Write-Host ("=" * 70)
Write-Host " Guidance:" -ForegroundColor Cyan
Write-Host "• Full KITTI tracking needs 21 sequences (0000–0020) in E:\KITTI\tracking\"
Write-Host "• Each seq must have: \image_02\ (PNGs) + \label_02\ (TXTs)"
Write-Host "• GhostDet demo sequence: 0006 (urban, 1147 frames)"
Write-Host "• If data is in data_tracking_*\training\, move it:"
Write-Host "    mkdir E:\KITTI\tracking"
Write-Host "    move E:\KITTI\training\* E:\KITTI\tracking\"