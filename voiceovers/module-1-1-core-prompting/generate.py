#!/usr/bin/env python3
"""Generate Module 1.1 Core Prompting Principles voiceover via fal.ai ElevenLabs (Adam)."""

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

# Recommended settings from prompt:
# Voice Profile: Professional, confident, warm, clear, energetic corporate trainer.
# Stability: 0.45
# Clarity / Similarity: 0.80
# Style Exaggeration: 0.15
VOICE_SETTINGS = {
    "voice": "Adam",
    "stability": 0.45,
    "similarity_boost": 0.80,
    "style": 0.15,
    "use_speaker_boost": True,
}

SCENES = {
    "scene-01.mp3": (
        "Welcome to Module 1.1 of the A.O.U. Certified A.I. Associate course. [pause] "
        "Today, we’re unpacking the foundational shift that turns unpredictable A.I. outputs into production-ready results: "
        "Core Prompting Principles and Structured Input Formats."
    ),
    "scene-02.mp3": (
        "When working with Large Language Models, clarity isn't just about good grammar... [pause] "
        "it's about system architecture. Effective prompts contain four key components: "
        "a clear Role, rich Context, an explicit Task, and strict Constraints. "
        "When we wrap these components inside structured input formats like Markdown or JSON, "
        "we eliminate ambiguity and make outputs deterministic."
    ),
    "scene-03.mp3": (
        "Let's see this in action. Look at the left side of your screen: "
        "a standard, unstructured prompt asking for a competitive analysis. "
        "It’s vague, lacks boundaries, and yields a messy essay."
    ),
    "scene-04.mp3": (
        "Now, watch what happens on the right when we reframe the exact same request using Markdown delimiters and a target JSON schema. "
        "By defining our system context, providing input parameters inside explicit tags, and requesting a strict output format, "
        "[firm] the A.I. skips the fluff [firm] and generates precise, machine-readable data ready for immediate integration."
    ),
    "scene-05.mp3": (
        "Now, let’s build one together. "
        "Imagine you need an A.I. assistant to extract key deliverables and action items from raw meeting notes."
    ),
    "scene-06.mp3": (
        "First, declare the context using system tags. [pause] "
        "Second, place the raw meeting transcript inside clear X.M.L. or Markdown block quotes so the A.I. knows where the data starts and ends. [pause] "
        "Third, specify the exact schema for the response. "
        "Notice how setting constraints—like 'If a deadline is unknown, output null'—prevents the model from guessing or hallucinating dates."
    ),
    "scene-07.mp3": (
        "It's your turn to apply this framework. In your course workspace, launch Exercise 1.1: The Prompt Refactor. "
        "You'll find real-world enterprise prompts that are currently generating inconsistent results. "
        "Your task: restructure them using the Role, Context, Task, Constraint framework, "
        "and format the inputs using Markdown headers and X.M.L. boundaries."
    ),
    "scene-08.mp3": (
        "Test your prompt directly in the interactive sandbox to verify your output structure. "
        "Master this pattern, and you've unlocked the core engine of professional A.I. productivity. "
        "See you in Video 1.2!"
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
    print("All voiceover audio clips generated successfully.")


if __name__ == "__main__":
    main()
