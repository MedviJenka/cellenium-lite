#!/bin/bash

echo "Logging into GitHub Container Registry"
echo "validate token is already exported in this system: export BINI_TOKEN=..."

az login
docker tag bini:latest biniai.azurecr.io/myimage:lateste
docker push biniai.azurecr.io/bini:latest
