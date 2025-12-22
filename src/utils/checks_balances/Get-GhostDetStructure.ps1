# Save as: C:\Users\Suzan\Documents\GhostDet-KITTI\Get-GhostDetStructure-Lite.ps1

$ProjectRoot = "C:\Users\Suzan\Documents\GhostDet-KITTI"
$OutputFile  = Join-Path $ProjectRoot ("GhostDet_Structure_Lite_" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".txt")

# Include only human-readable or structural files
$IncludeExtensions = @(
    "*.py", "*.m", "*.ipynb", "*.yaml", "*.yml", "*.json", "*.toml",
    "*.md", "*.txt", "*.cfg", "*.sh", "*.bat", "*.ps1"
)

# Exclude: envs, caches, binaries, logs, datasets, large files
$ExcludePatterns = @(
    "*/.venv/*", "*/venv/*", "*/env/*", "*/site-packages/*",
    "*/__pycache__/*", "*/.git/*", "*/logs/*", "*/cache/*",
    "*/data/*", "*/dataset/*", "*/KITTI/*", "*/calib/*", "*/image_2/*", "*/label_2/*",
    "*.png", "*.jpg", "*.bin", "*.pcd", "*.npy", "*.pth", "*.pt", "*.ckpt", "*.h5"
)

$MaxFileSizeMB = 2  # Be stricter: only small-code files

Write-Host "🔍 Scanning GhostDet-KITTI (lite mode: dev-only structure)" -ForegroundColor Cyan
Write-Host "🚫 Excluding: .venv, site-packages, datasets, binaries, cache" -ForegroundColor Gray

$items = Get-ChildItem -Path $ProjectRoot -Recurse -Force -ErrorAction SilentlyContinue |
    Where-Object {
        $rel = $_.FullName.Replace($ProjectRoot, "").Replace("\", "/").TrimStart("/")
        # Skip exclusions
        foreach ($p in $ExcludePatterns) { if ($rel -like $p) { return $false } }
        # Skip large files
        if (-not $_.PSIsContainer -and $_.Length -gt ($MaxFileSizeMB * 1MB)) { return $false }
        # Keep dirs + allowed extensions
        $_.PSIsContainer -or ($IncludeExtensions -contains "*$($_.Extension.ToLower())")
    }

$tree = @()
foreach ($item in $items) {
    $depth = ($item.FullName.Replace($ProjectRoot, "").Trim("\").Split("\").Count - 1)
    $indent = "│   " * $depth
    $prefix = if ($item.PSIsContainer) { "📁 " } else { "📄 " }
    $tree += "${indent}├── ${prefix}$($item.Name)"
}

$header = @"
GhostDet-KITTI — Developer Structure (Lite)
Generated: $(Get-Date)
Root: $ProjectRoot
Excluded: .venv, site-packages, datasets, binaries (>2MB), cache, logs
Key Interest: 
  → src\model\ghostdet_local.py      (core impl?)
  → src\data_preprocessing\*.py      (seq-0006 prep)
  → runs\detect\ghostdet_local*\     (training artifacts)
───────────────────────────────────────────────────────

"@

$header | Out-File -FilePath $OutputFile -Encoding UTF8
$tree | Out-File -FilePath $OutputFile -Encoding UTF8 -Append

# Locate Notepad++ (standard install paths)
$NotepadPlusPlus = @(
    "${env:ProgramFiles}\Notepad++\notepad++.exe",
    "${env:ProgramFiles(x86)}\Notepad++\notepad++.exe",
    "$env:LOCALAPPDATA\Programs\Notepad++\notepad++.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1

if ($NotepadPlusPlus) {
    Write-Host "📎 Opening in Notepad++..." -ForegroundColor Cyan
    & $NotepadPlusPlus $OutputFile
} else {
    Write-Warning "⚠️  Notepad++ not found. Opening in default Notepad."
    notepad $OutputFile
}