# check_setup.ps1 — ASCII-only, no special chars
# Save to: C:\Users\<USRTNAME>\Documents\GhostDet-KITTI\check_setup.ps1

Write-Host ">>> GhostDet Setup Checker -- $(Get-Date)" -ForegroundColor Cyan
Write-Host "============================================================"

# Check E: drive
if (-not (Test-Path "E:\")) {
    Write-Host "[FAIL] E: drive not connected. Plug in KITTI drive." -ForegroundColor Red
    exit 1
}
Write-Host "[OK]   E: drive connected" -ForegroundColor Green

# Check KITTI data
$trackingDir = "E:\KITTI\tracking\06\image_02"
$objectDir = "E:\KITTI\data_object_image_2\training"

if (Test-Path $trackingDir) {
    $count = (Get-ChildItem "$trackingDir\*.png" -ErrorAction SilentlyContinue).Count
    Write-Host "[OK]   KITTI tracking/06 found ($count frames)" -ForegroundColor Green
} elseif (Test-Path $objectDir) {
    $count = (Get-ChildItem "$objectDir\*.png" -ErrorAction SilentlyContinue).Count
    Write-Host "[WARN] Object data only ($count images). Tracking preferred." -ForegroundColor Yellow
} else {
    Write-Host "[FAIL] No KITTI data found at:" -ForegroundColor Red
    Write-Host "       $trackingDir"
    Write-Host "       $objectDir"
    exit 1
}

# Check local structure
$root = "$env:USERPROFILE\Documents\GhostDet-KITTI"
$required = @(
    "configs\paths.yaml",
    "requirements.txt",
    ".venv\Scripts\python.exe",
    "data\.gitkeep",
    "src\models",
    "src\datasets",
    "src\utils",
    "logs",
    "assets"
)

$allOK = $true
foreach ($item in $required) {
    if (Test-Path "$root\$item") {
        Write-Host "[OK]   $item" -ForegroundColor Green
    } else {
        Write-Host "[MISS] $item" -ForegroundColor Red
        $allOK = $false
    }
}

if (-not $allOK) {
    Write-Host "[INFO] Run .\setup_ghostdet.ps1 to fix." -ForegroundColor Yellow
    exit 1
}

# Check Python
$venvPy = "$root\.venv\Scripts\python.exe"
if (-not (Test-Path $venvPy)) {
    Write-Host "[FAIL] .venv missing. Run: python -m venv .venv" -ForegroundColor Red
    exit 1
}

# Test import
try {
    $result = & $venvPy -c "import torch; print('torch ok')"
    if ($result -eq "torch ok") {
        Write-Host "[OK]   Python (torch) working" -ForegroundColor Green
    } else {
        Write-Host "[WARN] Python import test inconclusive" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[WARN] Python test failed. Try reinstalling deps." -ForegroundColor Yellow
}

# Check config points to E:
$config = "$root\configs\paths.yaml"
if (-not (Test-Path $config)) {
    Write-Host "[FAIL] configs\paths.yaml missing" -ForegroundColor Red
    exit 1
}

$content = Get-Content $config -Raw
if ($content -match "E:/KITTI/tracking") {
    Write-Host "[OK]   paths.yaml uses tracking path" -ForegroundColor Green
} elseif ($content -match "E:/KITTI") {
    Write-Host "[OK]   paths.yaml references E:\KITTI" -ForegroundColor Green
} else {
    Write-Host "[WARN] paths.yaml may not point to E:\. Please verify." -ForegroundColor Yellow
}

# Final
Write-Host "============================================================"
Write-Host "[DONE] Setup check complete." -ForegroundColor Cyan
Write-Host "Next: "
Write-Host "  .venv\Scripts\Activate.ps1"
Write-Host "  python data\preprocess_kitti.py"