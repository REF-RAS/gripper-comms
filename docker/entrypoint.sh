#! /bin/bash

echo "> ENTRYPOINT RUNNING"
# Run CMD from Dockerfile or the overriding command from docker compose yaml file
echo "> Running $@"
exec "$@"
