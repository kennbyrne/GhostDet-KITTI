# extract_keyframes.ps1
# Extracts high-impact frames showcasing GhostDet's advantages over YOLOv8.
# Requires: ffmpeg in PATH

$videos = @{
    # Updated filename to match your rename
    "ghostdet_seq0006_250frame__v1.1.mp4" = @{
        45  = "occlusion_start_bus_enters";
        75  = "occlusion_peak_yolo_flickers";
        135 = "motion_blur_during_turn";
        190 = "recovery_ghostdet_stable";
        240 = "final_comparison_jitter_10pct";
    }
    "ghostdet_seq0006_500f_deep_dive_v1.1.mp4" = @{
        55  = "occlusion_start_full";
        120 = "multi_object_id_switch_yolo";
        270 = "motion_blur_severe";
        420 = "ghostdet_persistent_track";
    }
}

$baseDir = "logs/version1.1"
$outputDir = "figures/keyframes_v1.1_clean"
mkdir -Force $outputDir | Out-Null

foreach ($video in $videos.Keys) {
    $videoPath = Join-Path $baseDir $video
    if (!(Test-Path $videoPath)) {
        Write-Warning "Skip ${video}: not found"   # ✅ Fixed: ${video}
        continue
    }

    foreach ($frame in $videos[$video].Keys) {
        $desc = $videos[$video][$frame]
        $outName = "${video}_frame${frame}_${desc}.png"
        $outPath = Join-Path $outputDir $outName

        # Extract frame (10 FPS → time = frame/10)
        $timeSec = [Math]::Floor($frame / 10)
        ffmpeg -y -ss $timeSec -i $videoPath -vf "select=eq(n\,$frame)" -vframes 1 -q:v 2 $outPath

        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ $outName" -ForegroundColor Green
        } else {
            Write-Error "❌ Failed: $outName"
        }
    }
}

Write-Host "`n📌 Keyframes saved to: $outputDir" -ForegroundColor Cyan