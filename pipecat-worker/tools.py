"""Function-calling tools — Gemini calls these, they hit the existing dashboard API."""
from __future__ import annotations
import time
import httpx
from typing import Any
from loguru import logger

import config


# Per-call state, keyed by call_sid. Pipecat function handlers receive this via closures.
_call_state: dict[str, dict[str, Any]] = {}


def init_call_state(call_sid: str, twilio_to_number: str) -> dict:
    state = {
        "call_sid": call_sid,
        "to_number": twilio_to_number,
        "started_at": time.time(),
        "metadata": {},
        "outcome": None,
        "summary": None,
        "transferred": False,
        "transfer_to": None,
    }
    _call_state[call_sid] = state
    return state


def get_call_state(call_sid: str) -> dict:
    return _call_state.get(call_sid, {})


def _api(method: str, path: str, **kwargs) -> httpx.Response:
    url = f"{config.DASHBOARD_API_BASE}{path}"
    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {config.DASHBOARD_API_ADMIN_KEY}"
    return httpx.request(method, url, headers=headers, timeout=8, **kwargs)


# ── Tool implementations (called by Pipecat function-call dispatch) ────────────

async def check_postcode_coverage(call_sid: str, postcode: str) -> dict:
    """Returns {covered: bool, area_name: str | None}."""
    to_number = _call_state.get(call_sid, {}).get("to_number", "")
    try:
        r = _api("GET", "/postcode-check", params={"postcode": postcode, "number": to_number})
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        logger.warning(f"postcode_check failed: {e}")
    return {"covered": False, "area_name": None}


async def set_call_metadata(call_sid: str, **kwargs) -> dict:
    """Stash arbitrary key/value pairs for the eventual /webhook/call-complete payload."""
    state = _call_state.setdefault(call_sid, {"metadata": {}})
    state.setdefault("metadata", {}).update(kwargs)
    return {"ok": True}


async def book_callback(call_sid: str, when: str, name: str, number: str,
                        address: str | None = None, postcode: str | None = None,
                        issue: str | None = None) -> dict:
    """Schedule outbound callback by writing metadata; main API picks up via background loop."""
    return await set_call_metadata(
        call_sid,
        callback_requested=True,
        callback_time=when,
        lead_name=name,
        lead_number=number,
        full_address=address,
        postcode=postcode,
        issue_type=issue,
    )


async def transfer_to_human(call_sid: str, reason: str) -> dict:
    """Mark call for transfer — Twilio dial executed by call_complete handler."""
    state = _call_state.setdefault(call_sid, {"metadata": {}})
    state["transferred"] = True
    state["transfer_reason"] = reason
    # Plumber mobile comes from /inbound-lookup at session start, stashed in state
    state["transfer_to"] = state.get("plumber_mobile")
    return {"ok": True, "transfer_to": state.get("plumber_mobile")}


async def end_call(call_sid: str, outcome: str, summary: str) -> dict:
    """Final tool — flushes everything to /webhook/call-complete and signals pipeline shutdown."""
    state = _call_state.setdefault(call_sid, {"metadata": {}})
    state["outcome"] = outcome
    state["summary"] = summary
    state["ended_at"] = time.time()

    payload = {
        "call_id": call_sid,
        "to": state.get("to_number"),
        "from": state.get("metadata", {}).get("lead_number"),
        "duration_sec": int(state["ended_at"] - state.get("started_at", state["ended_at"])),
        "outcome": outcome,
        "summary": summary,
        "transcript": state.get("transcript", ""),
        "recording_url": state.get("recording_url"),
        **state.get("metadata", {}),
    }

    try:
        r = _api("POST", "/webhook/call-complete", json=payload)
        logger.info(f"call-complete posted: {r.status_code}")
    except Exception as e:
        logger.error(f"call-complete post failed: {e}")

    return {"ok": True, "outcome": outcome}


# ── OpenAI-format tool schemas (passed to LLMContext tools=) ───────────────────
# OpenRouter/OpenAI-compatible format: flat list of {"type":"function","function":{...}}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "check_postcode_coverage",
            "description": "Check if a UK postcode is in the plumber's coverage area. Call this whenever the caller mentions a postcode you haven't already verified.",
            "parameters": {
                "type": "object",
                "properties": {
                    "postcode": {"type": "string", "description": "UK postcode like SW1A 1AA"}
                },
                "required": ["postcode"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_call_metadata",
            "description": "Stash any captured detail (lead name, address, issue, urgency, gas_safe_required, recording_consent_given, landlord info, etc.) for the post-call record.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lead_name": {"type": "string"},
                    "lead_number": {"type": "string"},
                    "full_address": {"type": "string"},
                    "postcode": {"type": "string"},
                    "issue_type": {"type": "string"},
                    "urgency": {"type": "string", "enum": ["URGENT", "PRIORITY", "STANDARD"]},
                    "property_type": {"type": "string", "enum": ["homeowner", "tenant", "letting_agent", "commercial"]},
                    "landlord_name": {"type": "string"},
                    "landlord_phone": {"type": "string"},
                    "letting_company": {"type": "string"},
                    "agent_phone": {"type": "string"},
                    "gas_safe_required": {"type": "boolean"},
                    "recording_consent_given": {"type": "boolean"},
                    "out_of_area_text_consent": {"type": "boolean"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "book_callback",
            "description": "Schedule a callback at a specific time the caller requested.",
            "parameters": {
                "type": "object",
                "properties": {
                    "when": {"type": "string", "description": "Time the caller requested, free-form"},
                    "name": {"type": "string"},
                    "number": {"type": "string"},
                    "address": {"type": "string"},
                    "postcode": {"type": "string"},
                    "issue": {"type": "string"},
                },
                "required": ["when", "name", "number"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "transfer_to_human",
            "description": "Transfer the call to the plumber's mobile. Only call when caller insists on a human, or when in-hours + urgent + caller agrees.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reason": {"type": "string"}
                },
                "required": ["reason"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "end_call",
            "description": "End the call. Call this exactly once at the very end — after this, only the final farewell line is allowed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "outcome": {
                        "type": "string",
                        "enum": ["scheduled", "callback", "out_of_area", "transferred", "declined"],
                    },
                    "summary": {"type": "string", "description": "One-sentence summary of the call for the plumber"},
                },
                "required": ["outcome", "summary"],
            },
        },
    },
]
