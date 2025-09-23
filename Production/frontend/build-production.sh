#!/bin/bash

# Production build script for frontend
# Sets environment variables at build time

export VITE_API_URL="https://security-monitor.dreamhrai.com/api"
export VITE_APP_TITLE="Network Security Monitor"
export VITE_APP_VERSION="1.0.0"
export NODE_ENV="production"

echo "Building frontend with production environment variables..."
echo "VITE_API_URL: $VITE_API_URL"
echo "VITE_APP_TITLE: $VITE_APP_TITLE"
echo "VITE_APP_VERSION: $VITE_APP_VERSION"

# Build the application
npm run build

echo "Build completed!"
