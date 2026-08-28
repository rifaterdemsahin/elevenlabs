#!/usr/bin/env python3
"""Generate Abundance is a Platform v2 (Human Leverage) via fal.ai ElevenLabs (Adam)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent
VAULT_NAME = "dp-kv-deliverypilot"
SECRET_NAME = "FAL-AI-KEY"
ENDPOINT = "https://fal.run/fal-ai/elevenlabs/tts/eleven-v3"

VOICE_SETTINGS = {
    "voice": "Adam",
    "stability": 0.50,
    "similarity_boost": 0.80,
    "style": 0.05,
    "use_speaker_boost": True,
}

SCENES = {
    "scene-01.mp3": (
        "Someone called this an A.I. con. I walked in anyway. "
        "Abundance is a platform. And yes, the hype can be dishonest."
    ),
    "scene-02.mp3": (
        "But look at history. Trains were expensive. Power grids were expensive. "
        "We didn't stop. We adapted."
    ),
    "scene-03.mp3": (
        "What we do with the knowledge is the whole point. "
        "Software used to tax our time. Now, the model does the heavy lifting."
    ),
    "scene-04.mp3": (
        "Automation isn't replacing us; it's clearing the noise. "
        "Don't waste your human effort sending repetitive emails. Let the agent handle it."
    ),
    "scene-05.mp3": (
        "I still own the voice. I still direct the machine."
    ),
    "scene-06.mp3": (
        "As these tools combine, human opportunity explodes. "
        "We're creating roles that didn't exist five years ago."
    ),
    "scene-07.mp3": (
        "Delivery pilots. Forward-deployed engineers. System architects."
    ),
    "scene-08.mp3": (
        "A bigger digital archive doesn't replace your mind. "
        "It finally gives your human brain room to create."
    ),
    "scene-09.mp3": (
        "The future isn't about automated noise. It's about human leverage."
    ),
}

FULL_TEXT = "\n\n[pause]\n\n".join(SCENES.values())


def load_fal_key() -> str:
    key = os.environ.get("FAL_KEY") or os.environ.get("FAL_AI_KEY") or ""
    if key.strip():
        return key.strip()
    try:
        result = subprocess.run(
            [
                "az",
                "keyvault",
                "secret",
                "show",
                "--vault-name",
                VAULT_NAME,
                "--name",
                SECRET_NAME,
                "--query",
                "value",
                "-o",
                "tsv",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    sys.exit("FAL_KEY not found in env or Azure Key Vault.")


def synthesize(api_key: str, text: str, dest: Path) -> None:
    payload = json.dumps({"text": text, **VOICE_SETTINGS}).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    print(f"Generating {dest.name} ...")
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    audio = data.get("audio") or {}
    url = audio.get("url")
    if not url:
        raise RuntimeError(f"No audio URL in response for {dest.name}: {data}")
    with urllib.request.urlopen(url, timeout=180) as audio_resp:
        dest.write_bytes(audio_resp.read())
    print(f"  saved {dest.name} ({dest.stat().st_size} bytes)")


def main() -> None:
    api_key = load_fal_key()
    jobs = [("full.mp3", FULL_TEXT), *SCENES.items()]
    for filename, text in jobs:
        synthesize(api_key, text, OUT_DIR / filename)
    print("Done.")


if __name__ == "__main__":
    main()
