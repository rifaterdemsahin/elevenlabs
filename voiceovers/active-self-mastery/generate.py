#!/usr/bin/env python3
"""Generate Active Self-Mastery voiceover via fal.ai ElevenLabs (Adam)."""

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
        "[firm] When the I.T. market hit a downturn, I realized the old playbooks were useless. "
        "[pause] The rules had changed, and I needed to build entirely new connections."
    ),
    "scene-02.mp3": (
        "As A.I. accelerates, skill expectations aren't just rising— "
        "[firm] they're skyrocketing."
    ),
    "scene-03.mp3": (
        "Instead of backing down or blaming my university degree, I looked inward. "
        "[pause] Active self-mastery was the only way forward."
    ),
    "scene-04.mp3": (
        "Real growth isn't a solo journey—it's collective. "
        "[pause] It's like launching a shared knowledge hub for everyone you care about."
    ),
    "scene-05.mp3": (
        "When you level up, you lift your entire community. "
        "[pause] Educating your outer circle isn't just an option— "
        "[firm] it's your duty."
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
