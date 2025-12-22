# audit_trackeval.ps1
# Audits TrackEval installation in GhostDet-KITTI/tools/TrackEval/
# Detects structure, required files, and common setup issues.

$trackEvalRoot = "tools/TrackEval"
$absRoot = Join-Path $PWD $trackEvalRoot

Write-Host " Auditing TrackEval at: $absRoot" -ForegroundColor Cyan
if (-not (Test-Path $absRoot)) {
    Write-Error "❌ TrackEval not found. Expected: $absRoot"
    exit 1
}

# 1. Core directories
$requiredDirs = @("scripts", "trackeval", "data")
$missingDirs = @()
foreach ($d in $requiredDirs) {
    $path = Join-Path $absRoot $d
    if (Test-Path $path) {
        Write-Host " $d/" -ForegroundColor Green
    } else {
        Write-Host "  $d/ → MISSING (optional for KITTI, but scripts expect it)" -ForegroundColor Yellow
        $missingDirs += $d
    }
}

# 2. Required scripts
$requiredScripts = @(
    "scripts/run_kitti.py",
    "scripts/run.py",
    "trackeval/__init__.py"
)
$missingScripts = @()
foreach ($s in $requiredScripts) {
    $path = Join-Path $absRoot $s
    if (Test-Path $path) {
        Write-Host " $s" -ForegroundColor Green
    } else {
        Write-Host " $s → MISSING (critical)" -ForegroundColor Red
        $missingScripts += $s
    }
}

# 3. Check data layout (for KITTI: gt/ and trackers/)
$dataDir = Join-Path $absRoot "data"
if (Test-Path $dataDir) {
    $gtPath = Join-Path $dataDir "gt/kitti/kitti_train/label_02"
    $trackerPath = Join-Path $dataDir "trackers/kitti/kitti_train/ghostdet/data"
    
    if (Test-Path $gtPath) {
        $gtCount = (Get-ChildItem $gtPath -Filter "*.txt" | Measure-Object).Count
        Write-Host " GT data: $gtCount label files in $gtPath" -ForegroundColor DarkGray
    } else {
        Write-Host " GT not in TrackEval/data/ (expected: you'll use --gt_path E:/KITTI/...)" -ForegroundColor Blue
    }

    if (Test-Path $trackerPath) {
        $trackerCount = (Get-ChildItem $trackerPath -Filter "*.txt" | Measure-Object).Count
        Write-Host " Tracker data: $trackerCount results in $trackerPath" -ForegroundColor DarkGray
    } else {
        Write-Host " Tracker results not yet generated (run generate_trackeval_results.py first)" -ForegroundColor Blue
    }
} else {
    Write-Host " data/ dir not used — you'll point to E:/KITTI/ directly" -ForegroundColor Blue
}

# 4. Python environment check
Write-Host "`n Python environment:" -ForegroundColor Cyan
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pyVer = python --version 2>&1
    Write-Host " Python: $pyVer"
} else {
    Write-Warning " python not in PATH"
}

# Check .venv activation
$venvPython = ".venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    $venvVer = & $venvPython --version 2>&1
    $hasTrackEval = & $venvPython -c "import trackeval; print('✔')" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host " .venv: $venvVer + trackeval importable" -ForegroundColor Green
    } else {
        Write-Host "  .venv: $venvVer but trackeval not importable" -ForegroundColor Yellow
    }
} else {
    Write-Warning " .venv\Scripts\python.exe not found"
}

# 5. Summary
Write-Host "`n Summary:" -ForegroundColor Cyan
if ($missingScripts.Count -eq 0) {
    Write-Host " TrackEval structure complete." -ForegroundColor Green
    Write-Host " Next: Generate results → Run eval" -ForegroundColor Magenta
} else {
    Write-Error " Critical files missing. Re-clone TrackEval:"
    Write-Host "   git clone https://github.com/JonathonLuiten/TrackEval.git tools/TrackEval"
}

Write-Host "`nℹ  Note: KITTI MOT uses --benchmark MOT and seqmap for train/val split." -ForegroundColor Gray