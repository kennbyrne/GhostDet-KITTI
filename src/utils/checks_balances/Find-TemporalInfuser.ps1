# Save as: Find-TemporalInfuser.ps1
$ProjectRoot = "C:\Users\Suzan\Documents\GhostDet-KITTI"
$Patterns = @(
    "temporal.?infuser", "frame.?stack", "occlusion.?mask",
    "feature.?propagate", "trajectory.?smooth", "jitter.?reduce",
    "temporal.?fusion", "sliding.?window", "memory.?bank",
    "ghostnet", "ghost.?module"
)

$Include = @("*.py", "*.m", "*.ipynb", "*.md", "*.txt")

Get-ChildItem -Path $ProjectRoot -Recurse -Include $Include -ErrorAction SilentlyContinue |
    Where-Object { $_.Length -lt 5MB } |
    ForEach-Object {
        $file = $_.FullName
        try {
            $content = Get-Content $file -Raw
            foreach ($pat in $Patterns) {
                if ($content -match "(?i)$pat") {
                    Write-Host "🎯 TEMPORAL INFUSER CANDIDATE ($pat): $file" -ForegroundColor Magenta
                    break
                }
            }
        } catch { }
    }