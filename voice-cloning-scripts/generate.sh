#!/usr/bin/env bash
set -e

SCRIPT_FILE="${1:-lesson_script.txt}"
REF_AUDIO="${2:-./voice_dataset/001.wav}"
REF_TEXT="${3:-./voice_dataset/001.txt}"
OUTPUT_DIR="${4:-./output}"
MODEL="${5:-mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16}"

if [ ! -f "$SCRIPT_FILE" ]; then
  echo "❌ Error: Script text file '$SCRIPT_FILE' not found!"
  echo "Usage: ./generate.sh <script_to_speak.txt> [ref_audio.wav] [ref_transcript.txt] [output_dir] [model_id]"
  exit 1
fi

if [ ! -f "$REF_AUDIO" ]; then
  echo "❌ Error: Reference audio file '$REF_AUDIO' not found!"
  exit 1
fi

if [ ! -f "$REF_TEXT" ]; then
  echo "❌ Error: Reference text transcript '$REF_TEXT' not found!"
  exit 1
fi

VENV_PATH="$HOME/AI/voice-cloning/.venv"
if [ -d "$VENV_PATH" ]; then
  source "$VENV_PATH/bin/activate"
else
  echo "⚠️ Warning: $VENV_PATH not found. Running with current Python environment."
fi

mkdir -p "$OUTPUT_DIR"

TEXT_CONTENT=$(cat "$SCRIPT_FILE")
REF_TEXT_CONTENT=$(cat "$REF_TEXT")

echo "🎙️ Generating voiceover in your cloned voice..."
echo "Model: $MODEL"
echo "Input text: ${TEXT_CONTENT:0:80}..."

mlx_audio.tts.generate \
  --model "$MODEL" \
  --text "$TEXT_CONTENT" \
  --ref_audio "$REF_AUDIO" \
  --ref_text "$REF_TEXT_CONTENT" \
  --output_path "$OUTPUT_DIR"

echo "🎉 Generation complete! Audio saved to: $OUTPUT_DIR"
