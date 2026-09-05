#!/usr/bin/env bash
set -e

if [ "$#" -lt 1 ]; then
  echo "Usage: ./prepare-audio.sh <input_audio_file> [output_reference.wav]"
  echo "Example: ./prepare-audio.sh my_recording.m4a reference.wav"
  exit 1
fi

INPUT="$1"
OUTPUT="${2:-reference.wav}"

if [ ! -f "$INPUT" ]; then
  echo "❌ Error: Input audio file '$INPUT' does not exist."
  exit 1
fi

echo "🎵 Converting '$INPUT' to 24kHz Mono 16-bit PCM WAV: '$OUTPUT'..."
ffmpeg -y -i "$INPUT" -ar 24000 -ac 1 -sample_fmt s16 "$OUTPUT"

echo "✓ Converted successfully to $OUTPUT"
