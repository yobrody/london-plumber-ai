# PlumberAI Pipecat Worker

Replaces Bland.ai as the voice runtime for inbound plumber calls. Twilio Media Streams → this worker → Deepgram STT → Gemini 2.0 Flash → Cartesia TTS, with smart turn detection and 5 function-calling tools that hit the existing dashboard API.

See full plan: `~/.claude/projects/D--/memory/plans/2026-04-27-pipecat-migration.md`

## Layout

| File | Purpose |
|---|---|
| `worker.py` | FastAPI app: `/twiml` (Twilio webhook), `/ws` (Media Streams WebSocket), `/health` |
| `prompts.py` | System prompt translating Bland v2e pathway (12 nodes) to a single Gemini instruction |
| `tools.py` | 5 function-calling tools: `check_postcode_coverage`, `set_call_metadata`, `book_callback`, `transfer_to_human`, `end_call` |
| `config.py` | Env loading; fails loud on missing required vars |
| `requirements.txt` | Pinned deps |

## Setup (local dev)

```bash
python -m venv venv
venv/Scripts/activate      # Windows
# source venv/bin/activate # macOS/Linux
pip install -r requirements.txt
cp .env.example .env
# Fill in: DEEPGRAM_API_KEY, CARTESIA_API_KEY, CARTESIA_VOICE_ID, GOOGLE_API_KEY, TWILIO_AUTH_TOKEN
python worker.py
```

Then expose locally with `ngrok http 8090` for Twilio testing.

## Accounts you need

| Service | Purpose | Sign up | Free tier? |
|---|---|---|---|
| **Deepgram** | STT (nova-2-phonecall, telephony-tuned) | https://console.deepgram.com | $200 free credit |
| **Cartesia** | TTS (Sonic, British voices, sub-100ms TTFB) | https://play.cartesia.ai | Free tier exists |
| **Google AI Studio** | Gemini 2.0 Flash LLM | https://aistudio.google.com/apikey | Free for Flash |

## Deploying

This worker can NOT run on the existing Hetzner VPS (98% disk full, 4GB RAM already busy). It needs a dedicated worker VPS:

- Recommended: Hetzner CPX21 (4GB RAM, ~£5/mo) — sized for ~15 concurrent calls.
- Tailscale on both VPSes — worker dials existing dashboard API over private mesh.
- nginx termination on existing box → forwards Twilio WS to worker over Tailscale.

See plan doc for full deploy sequence.

## Twilio configuration

Update Twilio number's Voice URL to:
```
https://worker.londonplumberai.co.uk/twiml
```
(or whatever public hostname routes to the worker). Twilio POSTs incoming-call metadata to `/twiml`, our handler returns TwiML pointing at `/ws`, Twilio opens the WebSocket. Done.

## Status

Scaffolded 2026-04-27. NOT YET TESTED — awaiting:
- Deepgram, Cartesia, Google AI Studio account signups
- Worker VPS provisioning
- DNS / nginx for `worker.londonplumberai.co.uk`
