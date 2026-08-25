# ElevenLabs Voice Studio — Powered by fal.ai

A client-side studio for generating speech using **ElevenLabs models** (Eleven v3, Turbo v2.5, Multilingual v2) running on **fal.ai** serverless GPU infrastructure.

Deployed directly to GitHub Pages: [https://rifaterdemsahin.github.io/elevenlabs/](https://rifaterdemsahin.github.io/elevenlabs/)

---

## ✨ Features

- **Model Architectures**:
  - `fal-ai/elevenlabs/tts/eleven-v3`: High expressiveness with inline audio tags (`[excited]`, `[whispers]`, `[slowly]`, `[firm]`, `[pause]`).
  - `fal-ai/elevenlabs/tts/turbo-v2.5`: Low-latency, crisp delivery for technical guides.
  - `fal-ai/elevenlabs/tts/multilingual-v2`: Standard multilingual voiceover narration.
- **Voice Selection**: Pre-configured voices (Adam, Antoni, Brian, Rachel, Daniel, Charlie, Callum, etc.) or custom voice identifiers.
- **Precision Audio Controls**:
  - **Stability** slider (0.45 – 0.55 default for natural tone variation).
  - **Clarity / Similarity Boost** slider (0.75 – 0.85 for crisp acronyms).
  - **Style Exaggeration** slider (0.00 – 0.10 for professional tone).
  - **Speaker Boost** toggle.
- **Script Formatting Tools**:
  - One-click `[pause]` tag insertion.
  - One-click **Dot Acronyms** converter (`IDE` → `I.D.E.`, `LLM` → `L.L.M.`, `API` → `A.P.I.`, `UI` → `U.I.`, `CSS` → `C.S.S.`, `HTML` → `H.T.M.L.`, `ELO` → `E.L.O.`).
- **Cookie & LocalStorage Key Security**:
  - Enter your Fal.ai API key once; it persists safely in your browser cookie and `localStorage`.
  - Easy key modal with direct verification test ping.
- **Azure Key Vault Integration**:
  - Automatically loads `FAL-AI-KEY` from Azure Key Vault (`dp-kv-deliverypilot`) when launching locally.
- **Built-in Audio Player & History Drawer**:
  - Direct playback, speed controls, MP3 download, audio link sharing, and session history.

---

## 🚀 Quick Start (Local Development)

To run locally with automatic Azure Key Vault key retrieval and Google Chrome launch:

```bash
./start-local.sh
```

Or start standard python server:
```bash
python3 -m http.server 8080
```
Open `http://localhost:8080` in **Google Chrome**.

---

## 🌐 GitHub Pages Deployment

The application is hosted on GitHub Pages:
- **Live URL**: [https://rifaterdemsahin.github.io/elevenlabs/](https://rifaterdemsahin.github.io/elevenlabs/)
- Automatically updates on push to `main` branch.

---

## ⚙️ Sample Voiceover & Configuration

```text
Welcome! In this guide, we're diving into token optimization and cost-control strategies to scale your AI developer tooling... without breaking the bank.

[pause]

Here's a look at my custom I.D.E., built specifically to manage token allocation and model routing in real time. By routing tasks dynamically, running lightweight tools in parallel, and executing agentic file inspections, you maintain complete mastery over your L.L.M. expenditure.
...
```

**Recommended Settings:**
- **Voice**: `Adam` or `Brian`
- **Stability**: `0.50`
- **Clarity / Similarity**: `0.80`
- **Style Exaggeration**: `0.05`
- **Model**: `Eleven Multilingual v3` or `Turbo v2.5`
