#!/bin/bash

# Ensure PORT is set
export PORT="${PORT:-10000}"

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
