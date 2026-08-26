# ElevenLabs Voice Studio — Powered by fal.ai

A comprehensive client-side studio for generating speech using **ElevenLabs models** (Eleven v3, Turbo v2.5, Multilingual v2) running on **fal.ai** serverless GPU infrastructure and direct ElevenLabs API.

Deployed directly to GitHub Pages:
- **Standard Voice Studio**: [https://rifaterdemsahin.github.io/elevenlabs/](https://rifaterdemsahin.github.io/elevenlabs/)
- **Day One Player** (How an LLM Actually Reads): [https://rifaterdemsahin.github.io/elevenlabs/voiceovers/day-one-how-an-llm-reads/](https://rifaterdemsahin.github.io/elevenlabs/voiceovers/day-one-how-an-llm-reads/)
- **Rifat Erdem Sahin Cloned Voice Studio**: [https://rifaterdemsahin.github.io/elevenlabs/cloned-voice.html](https://rifaterdemsahin.github.io/elevenlabs/cloned-voice.html)

---

## 🎙️ Rifat Erdem Sahin — Cloned Voice Studio

A dedicated workspace built for Rifat Erdem Sahin's personal trained voice clone:
- **Cloned Voice Page**: [`cloned-voice.html`](cloned-voice.html)
- **Interactive 5-Step Guide**: Clear instructions on training the voice in ElevenLabs VoiceLab, obtaining the `voice_id`, and generating custom voiceovers.
- **Custom Voice ID Persistence**: Stores your personal `voice_id` directly in cookies/storage.
- **Dual Execution Backend**: Supports both `fal.ai` serverless GPU endpoint and direct ElevenLabs `v1/text-to-speech` API.
- **Optimized Tuning Defaults**: Fine-tuned similarity boost (`0.85`), stability (`0.50`), and style exaggeration (`0.03`) to match Erdem's voice cadence and accent.

### 📋 Checklist for Erdem to Activate His Cloned Voice:
1. **Record Clean Audio**: 1–3 clean voice clips (2–5 minutes) without background noise or echo.
2. **Train on ElevenLabs**: Go to [ElevenLabs VoiceLab](https://elevenlabs.io/app/voice-lab) &gt; **+ Add Generative or Cloned Voice** &gt; **Instant Voice Cloning**.
3. **Copy Voice ID**: Copy the generated `voice_id` from your voice card in VoiceLab.
4. **Paste into Cloned Voice Studio**: Enter the `voice_id` into the **Cloned Voice Profile** input and click **Save to Cookie**.
5. **Generate Voiceover**: Select your script or preset and click **Generate Erdem Voiceover**.

---

## ✨ Features (Standard Studio)

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
- **Main Studio**: [https://rifaterdemsahin.github.io/elevenlabs/](https://rifaterdemsahin.github.io/elevenlabs/)
- **Day One Player**: [https://rifaterdemsahin.github.io/elevenlabs/voiceovers/day-one-how-an-llm-reads/](https://rifaterdemsahin.github.io/elevenlabs/voiceovers/day-one-how-an-llm-reads/)
- **Erdem Cloned Voice Studio**: [https://rifaterdemsahin.github.io/elevenlabs/cloned-voice.html](https://rifaterdemsahin.github.io/elevenlabs/cloned-voice.html)
- Automatically updates on push to `main` branch.
