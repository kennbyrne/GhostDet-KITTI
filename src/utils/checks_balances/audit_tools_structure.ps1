# audit_tools_structure.ps1
# Recursively lists full structure of GhostDet-KITTI/tools/
# Highlights TrackEval files, detects clone errors.

$toolsRoot = "tools"
$absRoot = Join-Path $PWD $toolsRoot

if (-not (Test-Path $absRoot)) {
    Write-Error "❌ tools/ not found at: $absRoot"
    exit 1
}

Write-Host "🔍 Full structure of: $absRoot" -ForegroundColor Cyan
Write-Host ("=" * 60)

function Get-Tree {
    param(
        [string]$Path,
        [string]$Prefix = ""
    )
    $items = Get-ChildItem -Path $Path | Sort-Object Name
    for ($i = 0; $i -lt $items.Count; $i++) {
        $item = $items[$i]
        $isLast = ($i -eq $items.Count - 1)
        $connector = if ($isLast) { "└── " } else { "├── " }
        $newPrefix = $Prefix + (if ($isLast) { "    " } else { "│   " })

        # File/directory name
        $name = $item.Name
        $relPath = $item.FullName.Replace($absRoot, "").TrimStart("\").Replace("\", "/")

        # Highlight critical TrackEval files
        $highlight = $false
        $color = if ($item.PSIsContainer) { "White" } else { "DarkGray" }
        if ($name -eq "run_kitti.py" -and $relPath -like "*/scripts/*") {
            $color = "Green"; $highlight = $true
        } elseif ($name -eq "run.py" -and $relPath -like "*/scripts/*") {
            $color = "Green"; $highlight = $true
        } elseif ($name -eq "__init__.py" -and $relPath -like "*/trackeval/*") {
            $color = "Green"; $highlight = $true
        } elseif ($name -match "\.(py|ps1|yaml|txt|md)$") {
            $color = "Cyan"
        }

        $line = "${Prefix}${connector}${name}"
        if ($highlight) { $line += "  ← 🔑 CRITICAL" }
        Write-Host $line -ForegroundColor $color

        # Recurse into directories
        if ($item.PSIsContainer) {
            Get-Tree -Path $item.FullName -Prefix $newPrefix
        }
    }
}

# Start from tools/
Get-Tree -Path $absRoot

# Final summary
$trackEvalDirs = Get-ChildItem -Path $absRoot -Recurse -Directory | Where-Object { $_.Name -eq "TrackEval" }
$runKitti = Get-ChildItem -Path $absRoot -Recurse -Filter "run_kitti.py"
$runPy = Get-ChildItem -Path $absRoot -Recurse -Filter "run.py"
$initPy = Get-ChildItem -Path $absRoot -Recurse -Filter "__init__.py" | Where-Object { $_.Directory.Name -eq "trackeval" }

Write-Host ("=" * 60)
Write-Host "📊 Summary:" -ForegroundColor Cyan
Write-Host "  TrackEval dirs found: $($trackEvalDirs.Count)" -ForegroundColor White
foreach ($d in $trackEvalDirs) {
    Write-Host "    → $($d.FullName.Replace($PWD, '').TrimStart('\'))" -ForegroundColor DarkGray
}
Write-Host "  run_kitti.py: $($runKitti.Count) found" -ForegroundColor $(if ($runKitti.Count -gt 0) { "Green" } else { "Red" })
Write-Host "  run.py: $($runPy.Count) found" -ForegroundColor $(if ($runPy.Count -gt 0) { "Green" } else { "Red" })
Write-Host "  trackeval/__init__.py: $($initPy.Count) found" -ForegroundColor $(if ($initPy.Count -gt 0) { "Green" } else { "Red" })

if ($runKitti.Count -eq 0 -or $runPy.Count -eq 0 -or $initPy.Count -eq 0) {
    Write-Host "`n⚠️  TrackEval appears incomplete. Recommended fix:" -ForegroundColor Yellow
    Write-Host "   cd $PWD"
    Write-Host "   Remove-Item -Recurse -Force tools/TrackEval"
    Write-Host "   git clone https://github.com/JonathonLuiten/TrackEval.git tools/TrackEval"
} else {
    Write-Host "`n✅ TrackEval structure complete." -ForegroundColor Green
}