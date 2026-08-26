# Day One: How an LLM Actually Reads

**Voice:** Adam (standard ElevenLabs, not cloned)  
**Style:** Calm, articulate explainer  
**Pacing:** ~140 words per minute (aim for ~18–22 words per 8-second clip)  
**Tone:** Clear and informative, without artificial hype  
**Model:** fal-ai/elevenlabs/tts/eleven-v3  
**Settings:** stability 0.50 · similarity 0.80 · style 0.05 · speaker boost on

---

## Scene 01 (0:00–0:08)

Day one: how an LLM actually reads. Not with eyes. With tokens.

## Scene 02 (0:08–0:16)

Tokenization chops text into pieces the model can number. It does not understand English. It turns language into IDs.

## Scene 03 (0:16–0:24)

You guess a new subtitle word from neighbors. The model does not. It looks up pieces it already trained on.

## Scene 04 (0:24–0:32)

First, match against a vocabulary of words, subwords, and symbols. GPT-4's set is about a hundred thousand tokens.

## Scene 05 (0:32–0:40)

If a word is rare, split it into smaller known chunks. Spaces and punctuation often count as tokens too.

## Scene 06 (0:40–0:48)

Cartoon: "What a morning," question mark. Four tokens. You hear three words. The model may count four.

## Scene 07 (0:48–0:56)

Prompt plus reply share one budget. Toy numbers: thirty-five hundred in, six hundred out, limit four thousand. Overflow.

## Scene 08 (0:56–1:04)

Every space and symbol can spend the budget. Tokens are expensive. Day two next. Follow for the series.
