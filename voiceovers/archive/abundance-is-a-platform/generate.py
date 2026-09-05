#!/usr/bin/env python3
"""Generate Abundance is a Platform voiceover via fal.ai ElevenLabs (standard Adam voice)."""

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
        "Someone calls this an A.I. con. I walk in anyway. "
        "Abundance is a platform. The sale can still be dishonest."
    ),
    "scene-02.mp3": (
        "Trains were expensive. Coal plants were expensive. "
        "People still had to learn. What we do with the knowledge is the point."
    ),
    "scene-03.mp3": (
        "Every leap drinks power. Ask the only adult question: "
        "is this hall needed, or are the chairs just dancing?"
    ),
    "scene-04.mp3": (
        "Software used to tax the geeks. Now the model does the legwork. "
        "Keep the tool only if it meets a real lack."
    ),
    "scene-05.mp3": (
        "Most people never burn the horror-story bill. "
        "A thin slice does: builders, and founders who cannot hire."
    ),
    "scene-06.mp3": (
        "Three ledgers: useful for me. Profitable for them. Honestly sold. "
        "Coders do not go back. That does not bless the cap-ex."
    ),
    "scene-07.mp3": (
        "Trust the engineer at the wheel. Stay bound to the real world. "
        "Let the agent argue. You check the street."
    ),
    "scene-08.mp3": (
        "I do not send the same recruiter mail by hand. "
        "The agent sends. I still own the voice."
    ),
    "scene-09.mp3": (
        "Combinations explode. New work: Delivery Pilot. Forward-deployed engineer. "
        "A bigger archive makes the second brain normal."
    ),
    "scene-10.mp3": (
        "Taste is the scarce hour. The mundane gets trained locally. "
        "The model is glue, not a god."
    ),
    "scene-11.mp3": (
        "Secrets stay local. Heavy jobs go to the cloud. "
        "The meter is the product. Tokens as payments."
    ),
    "scene-12.mp3": (
        "Price your stack. Pay the honest bill or don't. "
        "Uplift is real. And it is conditional on learning."
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
