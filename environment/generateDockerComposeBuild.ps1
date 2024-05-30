$pythonScriptPath = "C:\Users\evgenyp\PycharmProjects\cellenium-lite\infrastructure\core\config_key.py"


# Check if the Python script exists at the constructed path
if (Test-Path $pythonScriptPath) {
    # Run the Python script
    python $pythonScriptPath

    # Check if the Python script set the environment variable
    if ($env:API_KEY) {
        Write-Output "API_KEY successfully set: $env:API_KEY"
    } else {
        Write-Error "API_KEY is not set by the Python script"
        exit 1
    }
    cd "C:\Users\evgenyp\PycharmProjects\cellenium-lite"
    # Start Docker Compose
    docker-compose up --build
} else {
    Write-Error "Python script not found at path: $pythonScriptPath"
}
