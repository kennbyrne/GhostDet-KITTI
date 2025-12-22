# audit_project.ps1
Write-Host "Auditing GhostDet-KITTI project files..." -ForegroundColor Cyan

Write-Host ""
Write-Host "src/ files:"
Get-ChildItem src\ -File -ErrorAction SilentlyContinue | ForEach-Object { Write-Host "  " $_.Name }

Write-Host ""
Write-Host "data/kitti_yolo/ files:"
Get-ChildItem data\kitti_yolo\ -File -ErrorAction SilentlyContinue | ForEach-Object { Write-Host "  " $_.Name }

Write-Host ""
Write-Host "logs/ files (non-video):"
Get-ChildItem logs\ -File -ErrorAction SilentlyContinue | Where-Object { $_.Extension -ne ".mp4" } | ForEach-Object { Write-Host "  " $_.Name }

Write-Host ""
Write-Host "runs/detect/ghostdet_local2/weights/ files:"
Get-ChildItem runs\detect\ghostdet_local2\weights\ -File -ErrorAction SilentlyContinue | ForEach-Object { Write-Host "  " $_.Name }

Write-Host ""
Write-Host "Root files:"
Get-ChildItem -File -Name README.md, requirements.txt, setup_kitti.ps1

Write-Host ""
Write-Host "=== Audit complete. Ready for consolidation. ===" -ForegroundColor Green