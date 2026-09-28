<#
.SYNOPSIS
  Runs the video assembly step (Remotion enhance + intro prepend) for whichever video in
  Video Generator\Videos\ is marked ready, unattended. Meant to run on a Windows Task
  Scheduler trigger on this PC.

.NOTES
  Deterministic only — no AI reasoning needed here, this just runs the same commands a human
  would type into Claude Code per 04_Video_Editing/Remotion/README.md and
  04_Video_Editing/FFmpeg_Pipeline.md Step 7. The Cowork-scheduled pipeline run drops a
  READY_FOR_ASSEMBLY.txt marker (optionally containing a music track name on the first line)
  in a video's Editing\ folder once images + narration audio are both in place; this script
  picks up the oldest unprocessed marker each time it runs, and writes DONE_ASSEMBLY.txt (or
  FAILED_ASSEMBLY.txt with the error) next to it when finished, which the next scheduled
  Cowork run reads to report status back by email and continue to thumbnail/title/delivery.

  Register with Task Scheduler, e.g. (edit the path to match where you put this project):
    schtasks /Create /SC DAILY /TN "VideoGenerator_Assembly" /TR "powershell.exe -ExecutionPolicy Bypass -File \"<PROJECT_ROOT>\04_Video_Editing\Run_Assembly.ps1\"" /ST 07:00
  Run it a few hours after your scheduled Cowork pipeline run (if you set one up), so
  images/audio have had time to finish. Safe to run more often than needed — it's a no-op
  when nothing is marked ready.
#>

$ErrorActionPreference = 'Stop'
$Root = "<PROJECT_ROOT>"    # <-- edit this to the full path of your "Video Generator" folder
$VideosRoot = Join-Path $Root "Videos"
$RemotionDir = Join-Path $Root "04_Video_Editing\Remotion"
$AssetsIntro = Join-Path $Root "04_Video_Editing\Assets\Intro\intro.mp4"
$LogFile = Join-Path $Root "04_Video_Editing\Assembly_Log.txt"

function Write-Log($msg) {
    $line = "[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $msg
    Add-Content -Path $LogFile -Value $line
    Write-Host $line
}

# Find the oldest video folder with a ready marker and no done/failed marker yet.
$candidates = Get-ChildItem -Path $VideosRoot -Directory | Where-Object {
    $_.Name -notin @('Archived')
} | ForEach-Object {
    $editing = Join-Path $_.FullName "Editing"
    $ready = Join-Path $editing "READY_FOR_ASSEMBLY.txt"
    $done = Join-Path $editing "DONE_ASSEMBLY.txt"
    $failed = Join-Path $editing "FAILED_ASSEMBLY.txt"
    if ((Test-Path $ready) -and -not (Test-Path $done) -and -not (Test-Path $failed)) {
        [PSCustomObject]@{ Topic = $_.Name; Path = $_.FullName; Ready = $ready; Editing = $editing }
    }
} | Sort-Object { (Get-Item $_.Ready).LastWriteTime } | Select-Object -First 1

if (-not $candidates) {
    Write-Log "No video ready for assembly. Exiting."
    exit 0
}

$Topic = $candidates.Topic
$VideoPath = $candidates.Path
$Editing = $candidates.Editing
$Music = (Get-Content $candidates.Ready -ErrorAction SilentlyContinue | Select-Object -First 1)

Write-Log "Starting assembly for '$Topic'"
if ($Music) { Write-Log "Music track: $Music" }

try {
    Push-Location $RemotionDir

    if (-not (Test-Path (Join-Path $RemotionDir "node_modules"))) {
        Write-Log "Running npm install (first run)..."
        npm install
        npm approve-scripts esbuild
    }

    $enhanceArgs = @("scripts/enhance.py", "--video", "Videos/$Topic")
    if ($Music) { $enhanceArgs += @("--music", $Music) }

    Write-Log "Running enhance.py..."
    python @enhanceArgs
    if ($LASTEXITCODE -ne 0) { throw "enhance.py exited with code $LASTEXITCODE" }

    $bodyFile = Join-Path $Editing "${Topic}_enhanced_body.mp4"
    if (-not (Test-Path $bodyFile)) { throw "Expected enhanced body not found: $bodyFile" }

    if (-not (Test-Path $AssetsIntro)) {
        throw "Channel intro missing at $AssetsIntro — cannot prepend, stopping before Step 7."
    }

    # Step 7 — normalize intro then concat (per FFmpeg_Pipeline.md)
    $introNorm = Join-Path $Editing "intro_normalized.mp4"
    Write-Log "Normalizing intro..."
    ffmpeg -y -i $AssetsIntro -vf "scale=1920:1080" -r 25 -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k $introNorm
    if ($LASTEXITCODE -ne 0) { throw "intro normalize failed, code $LASTEXITCODE" }

    $publishDir = Join-Path $VideoPath "Publish"
    New-Item -ItemType Directory -Force -Path $publishDir | Out-Null
    $finalFile = Join-Path $publishDir "$Topic.mp4"

    Write-Log "Concatenating intro + body..."
    ffmpeg -y -i $introNorm -i $bodyFile -filter_complex `
      "[0:v]format=yuv420p,fps=25,setsar=1[v0];[1:v]format=yuv420p,fps=25,setsar=1[v1];[v0][0:a][v1][1:a]concat=n=2:v=1:a=1[outv][outa]" `
      -map "[outv]" -map "[outa]" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart $finalFile
    if ($LASTEXITCODE -ne 0) { throw "intro concat failed, code $LASTEXITCODE" }

    if (-not (Test-Path $finalFile)) { throw "Final file not found after concat: $finalFile" }

    Set-Content -Path (Join-Path $Editing "DONE_ASSEMBLY.txt") -Value "Assembled $(Get-Date -Format o) -> $finalFile"
    Write-Log "SUCCESS: '$Topic' assembled -> $finalFile"
}
catch {
    $err = $_.Exception.Message
    Set-Content -Path (Join-Path $Editing "FAILED_ASSEMBLY.txt") -Value "Failed $(Get-Date -Format o): $err"
    Write-Log "FAILED: '$Topic' — $err"
}
finally {
    Pop-Location
}
