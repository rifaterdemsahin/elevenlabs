#!/usr/bin/env python3
"""Generate Day One LLM tokenization voiceover via fal.ai ElevenLabs (standard Adam voice)."""

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
        "Day one: how an L.L.M. actually reads. Not with eyes. With tokens."
    ),
    "scene-02.mp3": (
        "Tokenization chops text into pieces the model can number. "
        "It does not understand English. It turns language into I.D.s."
    ),
    "scene-03.mp3": (
        "You guess a new subtitle word from neighbors. The model does not. "
        "It looks up pieces it already trained on."
    ),
    "scene-04.mp3": (
        "First, match against a vocabulary of words, subwords, and symbols. "
        "G.P.T. four's set is about a hundred thousand tokens."
    ),
    "scene-05.mp3": (
        "If a word is rare, split it into smaller known chunks. "
        "Spaces and punctuation often count as tokens too."
    ),
    "scene-06.mp3": (
        'Cartoon: "What a morning," question mark. Four tokens. '
        "You hear three words. The model may count four."
    ),
    "scene-07.mp3": (
        "Prompt plus reply share one budget. Toy numbers: thirty-five hundred in, "
        "six hundred out, limit four thousand. Overflow."
    ),
    "scene-08.mp3": (
        "Every space and symbol can spend the budget. Tokens are expensive. "
        "Day two next. Follow for the series."
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
