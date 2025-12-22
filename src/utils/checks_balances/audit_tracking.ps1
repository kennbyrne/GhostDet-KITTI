# audit_tracking.ps1 — Full KITTI tracking structure audit
Write-Host " Scanning E:\KITTI\tracking\ for sequences..." -ForegroundColor Cyan

$root = "E:\KITTI\tracking"
if (-not (Test-Path $root)) {
    Write-Host "[] $root not found" -ForegroundColor Red
    exit 1
}

# Find all seq dirs (supports 0000, 0006, 6, etc.)
$seqDirs = Get-ChildItem $root -Directory | Where-Object {
    $_.Name -match '^\d{1,4}$'  # Matches 6, 06, 0006
}

if ($seqDirs.Count -eq 0) {
    Write-Host "[] No sequence folders found. Checking flat structure..." -ForegroundColor Yellow
    # Try flat image_02/0006/
    $seqDirs = Get-ChildItem "$root\image_02" -Directory -ErrorAction SilentlyContinue | 
               Where-Object { $_.Name -match '^\d{1,4}$' } |
               ForEach-Object { [PSCustomObject]@{ Name = $_.Name; FullName = "$root\image_02\$($_.Name)" } }
}

if ($seqDirs.Count -eq 0) {
    Write-Host "[] No sequences detected. Listing all folders:" -ForegroundColor Red
    Get-ChildItem $root -Recurse -Directory | Select-Object FullName
    exit 1
}

Write-Host "`n[] Found $($seqDirs.Count) sequences:" -ForegroundColor Green

# Check each sequence
$summary = @()
foreach ($seq in $seqDirs) {
    $seqName = $seq.Name
    $seqPath = $seq.FullName
    
    # Try common image paths
    $imgPaths = @(
        "$seqPath\image_02",
        "$seqPath\image_2",
        "$root\image_02\$seqName",
        "$root\training\image_02\$seqName"
    ) | Where-Object { Test-Path $_ }

    $lblPaths = @(
        "$seqPath\label_02",
        "$seqPath\label_2",
        "$root\label_02\$seqName",
        "$root\training\label_02\$seqName"
    ) | Where-Object { Test-Path $_ }

    $imgCount = 0; $lblCount = 0
    if ($imgPaths) {
        $imgCount = (Get-ChildItem "$($imgPaths[0])\*.png" -ErrorAction SilentlyContinue).Count
    }
    if ($lblPaths) {
        $lblCount = (Get-ChildItem "$($lblPaths[0])\*.txt" -ErrorAction SilentlyContinue).Count
    }

    $status = if ($imgCount -ge 1000) { "" } elseif ($imgCount -gt 0) { "" } else { "" }
    Write-Host "  ${status} Seq ${seqName}: ${imgCount} images, ${lblCount} labels"

    $summary += [PSCustomObject]@{
        Sequence = $seqName
        Images = $imgCount
        Labels = $lblCount
        ImagePath = if ($imgPaths) { $imgPaths[0] } else { "" }
        LabelPath = if ($lblPaths) { $lblPaths[0] } else { "" }
    }
}

# Final report
Write-Host ("=" * 50)
Write-Host "[] Summary:" -ForegroundColor Cyan
$summary | Format-Table Sequence, Images, Labels -AutoSize

$fullSeqs = $summary | Where-Object { $_.Images -ge 1000 -and [Math]::Abs($_.Images - $_.Labels) -le 5 }
if ($fullSeqs.Count -gt 0) {
    Write-Host " Full sequences (≥1000 frames): $($fullSeqs.Sequence -join ', ')" -ForegroundColor Green
} else {
    Write-Host " No full sequences found. Top candidate: $($summary | Sort-Object Images -Descending | Select-Object -First 1).Sequence" -ForegroundColor Yellow
}