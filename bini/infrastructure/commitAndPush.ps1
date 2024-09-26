# Set the execution policy for the script
Set-ExecutionPolicy Bypass -Scope Process

# Get the main drive character from the environment variable (C://, D:// etc)
$driver = $env:SystemDrive

# Define log file path
$logFilePath = "$driver\Projects\PyBREnv\pull_log.txt"

# Clear previous logs
Clear-Content -Path $logFilePath

# Format time for readibillity
$readableTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Add this time format to Start time value
Add-Content -Path $logFilePath -Value "Start time: $readableTime"

# Start logging
Start-Transcript -Path $logFilePath -Append

# List of repositories to pull and rebase
$repos = @(
    "$driver\Projects\PyBREnv\coreinfra",
    "$driver\Projects\PyBREnv\qasharedinfra",
    "$driver\Projects\PyBREnv\testing\smarttap"
)

# Loop each repo and pull rebase
foreach ($repo in $repos) {

    Write-Host "setting safe directory for $repo"

    # git config --global --add safe.directory $repo

    if (Test-Path $repo) {

        Set-Location $repo
        Write-Host "Pulling from $repo..."
        git add .
        git stash
        git pull --rebase

        if ($LASTEXITCODE -ne 0) {
            Write-Host "Failed to pull repository: $repo"
        } else {
            Write-Host "Successfully pulled and rebased: $repo"
        }
    } else {
        Write-Host "$repo does not exist"
    }
}

function Set-CommitMessage {
    param ([string]$autoMessage = "Auto commit message")
    $commitMessage = Read-Host -Prompt "Type commit message"
    if ([string]::IsNullOrWhiteSpace($commitMessage)) {
        $commitMessage = $autoMessage
    }
    return $commitMessage
}


function Confirm-Continue {
    param (
        [string]$message = "Do you want to continue? (Y/N)"
    )
    do {
        $response = Read-Host -Prompt $message
    } while ($response -ne "Y" -and $response -ne "N")

    return $response -eq "Y"
}

git add .
git status
Confirm-Continue
git commit -m Set-CommitMessage
git push origin head:refs/for/master

# Stop logging
Stop-Transcript
