#!/usr/bin/env bash
set -e

echo "========================================================"
echo " Apple Silicon M1 Max (64GB) Voice Cloning Setup"
echo " Engine: MLX-Audio + Qwen3-TTS 1.7B Base"
echo "========================================================"

# Step 1: Check architecture
ARCH=$(uname -m)
if [ "$ARCH" != "arm64" ]; then
  echo "⚠️ Warning: Expected arm64 architecture for Apple Silicon, found: $ARCH"
else
  echo "✓ Apple Silicon architecture confirmed ($ARCH)"
fi

# Step 2: Check Homebrew & FFmpeg
if ! command -v ffmpeg &> /dev/null; then
  echo "📦 Installing FFmpeg via Homebrew..."
  if command -v brew &> /dev/null; then
    brew install ffmpeg
  else
    echo "❌ Error: Homebrew not found. Please install Homebrew first from https://brew.sh"
    exit 1
  fi
else
  echo "✓ FFmpeg is installed ($(which ffmpeg))"
fi

# Step 3: Setup Virtual Environment with Python 3.12/3.11
INSTALL_DIR="$HOME/AI/voice-cloning"
mkdir -p "$INSTALL_DIR"/{voice_dataset,output,scripts}
cd "$INSTALL_DIR"

PYTHON_BIN=""
if command -v python3.12 &> /dev/null; then
  PYTHON_BIN=$(which python3.12)
elif command -v python3.11 &> /dev/null; then
  PYTHON_BIN=$(which python3.11)
elif command -v python3 &> /dev/null; then
  PYTHON_BIN=$(which python3)
fi

echo "🐍 Setting up virtual environment at $INSTALL_DIR/.venv using $PYTHON_BIN..."
"$PYTHON_BIN" -m venv .venv
source .venv/bin/activate

echo "📦 Upgrading pip and installing mlx-audio..."
pip install --upgrade pip
pip install -U mlx-audio

echo "========================================================"
echo "✓ Voice Cloning environment successfully configured!"
echo "Location: $INSTALL_DIR"
echo "To activate manually: source $INSTALL_DIR/.venv/bin/activate"
echo "========================================================"
