#!/bin/bash

# Debug output
echo "Current environment:"
echo "PORT: $PORT"
echo "RENDER: $RENDER"

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
