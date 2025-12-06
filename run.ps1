# Run geoclip_pipeline with the correct virtual environment
$venvPath = "C:\Users\benja\OneDrive\Documents\GitHub\Hacksmith-Hackathon-2025\geoclip-env"
$pythonExe = Join-Path $venvPath "Scripts\python.exe"

Write-Host "Running GeoCLIP pipeline with venv Python..."
Write-Host "Python: $pythonExe"

& $pythonExe geoclip_pipeline.py

Read-Host "Press Enter to exit"
