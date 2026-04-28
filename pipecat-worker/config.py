"""Environment-backed config — fail loud if anything is missing."""
import os
from dotenv import load_dotenv

load_dotenv()


def _required(key: str) -> str:
    val = os.environ.get(key)
    if not val:
        raise RuntimeError(f"Missing required env var: {key}")
    return val


# Twilio
TWILIO_ACCOUNT_SID = _required("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = _required("TWILIO_AUTH_TOKEN")

# AI services
DEEPGRAM_API_KEY = _required("DEEPGRAM_API_KEY")
CARTESIA_API_KEY = _required("CARTESIA_API_KEY")
CARTESIA_VOICE_ID = _required("CARTESIA_VOICE_ID")

# LLM via OpenRouter (OpenAI-compatible). Routes to whatever model is set.
# Default: gemini-2.0-flash through OpenRouter (Brody's existing credits).
OPENROUTER_API_KEY = _required("OPENROUTER_API_KEY")
LLM_MODEL = os.environ.get("LLM_MODEL", "google/gemini-2.0-flash-001")

# Direct Google AI Studio — kept around in case we cut over later when project
# billing is enabled (cheaper than OpenRouter markup).
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")

# Dashboard API (existing PlumberAI backend)
DASHBOARD_API_BASE = _required("DASHBOARD_API_BASE")
DASHBOARD_API_ADMIN_KEY = _required("DASHBOARD_API_ADMIN_KEY")

# Worker
WORKER_PORT = int(os.environ.get("WORKER_PORT", "8090"))

# Deepgram model — telephony-tuned
DEEPGRAM_MODEL = os.environ.get("DEEPGRAM_MODEL", "nova-2-phonecall")
