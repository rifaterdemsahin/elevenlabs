#!/bin/bash
set -e

echo "========================================================"
echo " ElevenLabs Studio — Local Launcher with Azure Key Vault"
echo "========================================================"

PORT=8080
VAULT_NAME="dp-kv-deliverypilot"
SECRET_NAME="FAL-AI-KEY"

echo "🔍 Attempting to load FAL API key from Azure Key Vault '$VAULT_NAME'..."

FAL_KEY=""
if command -v az >/dev/null 2>&1; then
  FAL_KEY=$(az keyvault secret show --vault-name "$VAULT_NAME" --name "$SECRET_NAME" --query value -o tsv 2>/dev/null || true)
fi

if [ -n "$FAL_KEY" ]; then
  echo "✓ Successfully loaded FAL_KEY from Azure Key Vault ($SECRET_NAME)!"
  TARGET_URL="http://localhost:$PORT/?key=$FAL_KEY"
else
  echo "⚠️  Could not automatically fetch key from Azure Key Vault. Starting server without preloaded key."
  TARGET_URL="http://localhost:$PORT/"
fi

# Check if port is already in use, kill old instance if any
PID=$(lsof -ti tcp:$PORT || true)
if [ -n "$PID" ]; then
  echo "Terminating existing server on port $PORT (PID: $PID)..."
  kill -9 $PID 2>/dev/null || true
  sleep 1
fi

echo "🚀 Starting local HTTP server on port $PORT..."
python3 -m http.server $PORT >/dev/null 2>&1 &
SERVER_PID=$!
echo "✓ Server running (PID: $SERVER_PID)"

# Wait for server to start
sleep 1

echo "🌐 Opening in Google Chrome: $TARGET_URL"
open -a "Google Chrome" "$TARGET_URL"

echo "========================================================"
echo "ElevenLabs Studio is now live at: http://localhost:$PORT"
echo "Press Ctrl+C to stop the local server."
echo "========================================================"

# Keep alive or wait
wait $SERVER_PID
