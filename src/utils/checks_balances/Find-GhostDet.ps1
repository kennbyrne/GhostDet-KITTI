# Save as: C:\Users\Suzan\Documents\GhostDet-KITTI\Find-GhostDet.ps1
$ProjectRoot = "C:\Users\Suzan\Documents\GhostDet-KITTI"

$Patterns = @(
    "GhostDet", "ghostdet",            # Class/function name (case-insensitive)
    "temporal.?infuser",               # May be hyphen/spaced
    "seq.?0006", "sequence.?0006",
    "occlusion.?handling", "trajectory.?smoothing"
)

$Include = @("*.py", "*.m", "*.ipynb", "*.yaml", "*.yml", "*.json", "*.md", "*.txt")

Write-Host "🔍 Searching for GhostDet signatures in code/configs..." -ForegroundColor Cyan

Get-ChildItem -Path $ProjectRoot -Recurse -Include $Include -ErrorAction SilentlyContinue |
    Where-Object {
        $_.Length -lt 10MB -and
        $_.FullName -notmatch "\\(data|dataset|KITTI|logs|cache|__pycache__|\.git)\\"
    } |
    ForEach-Object {
        $file = $_.FullName
        try {
            $content = Get-Content $file -Raw -ErrorAction Stop
            foreach ($pat in $Patterns) {
                if ($content -match "(?i)$pat") {
                    Write-Host "✅ MATCH ($pat): $file" -ForegroundColor Green
                    break
                }
            }
        } catch {
            Write-Warning "⚠️  Skipped (read error): $file"
        }
    }

Write-Host "🔍 Search complete." -ForegroundColor Cyan