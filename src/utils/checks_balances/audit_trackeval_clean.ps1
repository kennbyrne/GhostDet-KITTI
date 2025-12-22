# audit_trackeval_clean.ps1
$trackEvalRoot = "tools\TrackEval"
if (-not (Test-Path $trackEvalRoot)) {
    Write-Error "❌ TrackEval not found at: $trackEvalRoot"
    exit 1
}

Write-Host "🔍 TrackEval structure:" -ForegroundColor Cyan
Get-ChildItem -Path $trackEvalRoot -Recurse |
    Where-Object { $_.Name -in @("run_kitti.py", "run.py", "__init__.py") } |
    ForEach-Object {
        $rel = $_.FullName.Replace((Resolve-Path $trackEvalRoot).Path, "").TrimStart("\")
        $status = if ($_.Name -eq "run.py") { "⚠️ MISSING" } else { "✅ OK" }
        Write-Host "$rel → $status"
    }

# Final check
$hasRunKitti = Test-Path "$trackEvalRoot\scripts\run_kitti.py"
$hasInit = Test-Path "$trackEvalRoot\trackeval\__init__.py"
if ($hasRunKitti -and $hasInit) {
    Write-Host "✅ Core files present. Ready for evaluation." -ForegroundColor Green
} else {
    Write-Host "❌ Critical files missing. Re-clone TrackEval." -ForegroundColor Red
}