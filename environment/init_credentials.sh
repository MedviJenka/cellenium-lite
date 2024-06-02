#!/bin/sh

# Ensure the credentials file is available in the shared volume

cp /C/Users/evgenyp/Downloads/credentials_1.json /app/credentials.json


# Execute the original command
exec "$@"
chmod +x init_credentials.sh
