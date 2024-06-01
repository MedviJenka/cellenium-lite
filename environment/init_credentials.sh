#!/bin/sh

# Ensure the credentials file is available in the shared volume
if [ ! -f /app/credentials/credentials.json ]; then
  cp /c/Users/medvi/Downloads/credentials_1.json /app/credentials/credentials.json
fi

# Execute the original command
exec "$@"
chmod +x init_credentials.sh
