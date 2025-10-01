#!/bin/bash
# Production startup script for Render
echo "Starting Ramble app in production mode..."
echo "Environment variables:"
echo "PORT: $PORT"
echo "SUPABASE_URL: ${SUPABASE_URL:0:20}..."
echo "LINKEDIN_CLIENT_ID: $LINKEDIN_CLIENT_ID"

# Start with Gunicorn for production
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
