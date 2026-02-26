#!/usr/bin/env python3
"""
LondonPlumberAI — WhatsApp dispatch alert microservice.

Receives webhook calls from Make.com (or similar) and sends lead/alert
messages to plumbers via Twilio WhatsApp. Replace or supplement SMS dispatch.

Endpoints:
  POST /send   — Send one WhatsApp message (Make.com HTTP module).
  GET  /health — Health check for Hetzner/Lucky monitoring.

Env (required for sending):
  TWILIO_ACCOUNT_SID
  TWILIO_AUTH_TOKEN
  TWILIO_WHATSAPP_FROM  e.g. whatsapp:+14155238886 (sandbox) or your Twilio WhatsApp number
  WEBHOOK_AUTH_TOKEN    optional; if set, request must have X-Webhook-Token: <value>

Make.com payload (POST /send, JSON or form):
  to_phone   — E.164 plumber number (e.g. 447401097118)
  body       — Message text (or use urgency + lead fields for built-in template)
  urgency    — optional: URGENT | SCHEDULED (formats message with emoji)
  address    — optional: lead address
  issue      — optional: issue_type from Bland
  postcode   — optional
"""

import os
import re
from typing import Tuple

from flask import Flask, request, jsonify

app = Flask(__name__)

# E.164: digits only, allow leading +
E164_RE = re.compile(r"^\+?[1-9]\d{6,14}$")


def normalize_phone(raw: str) -> str:
    """Ensure phone is whatsapp:+44... form for Twilio."""
    if not raw:
        return ""
    digits = re.sub(r"\D", "", raw)
    if digits.startswith("0"):
        digits = "44" + digits[1:]  # UK national to E.164
    elif not digits.startswith("44") and len(digits) == 10:
        digits = "44" + digits
    if not digits.startswith("44"):
        return ""  # only UK for now
    return f"whatsapp:+{digits}"


def format_dispatch_message(urgency, address, issue, postcode, body):
    """Build alert text similar to existing SMS (emoji-formatted)."""
    if body and body.strip():
        return body.strip()
    parts = []
    if urgency and urgency.upper() == "URGENT":
        parts.append("🚨 URGENT LEAD")
    elif urgency and urgency.upper() == "SCHEDULED":
        parts.append("📅 Scheduled lead")
    else:
        parts.append("📋 New lead")
    if address:
        parts.append(f"Address: {address}")
    if issue:
        parts.append(f"Issue: {issue}")
    if postcode:
        parts.append(f"Postcode: {postcode}")
    return "\n".join(parts) if parts else "New lead — check CRM."


def get_client():
    sid = os.environ.get("TWILIO_ACCOUNT_SID")
    token = os.environ.get("TWILIO_AUTH_TOKEN")
    if not sid or not token:
        return None
    from twilio.rest import Client
    return Client(sid, token)


def check_auth() -> Tuple[bool, str]:
    token = os.environ.get("WEBHOOK_AUTH_TOKEN")
    if not token:
        return True, ""
    provided = request.headers.get("X-Webhook-Token") or request.args.get("token")
    if provided != token:
        return False, "Invalid or missing webhook token"
    return True, ""


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "whatsapp-alerts"}), 200


@app.route("/send", methods=["POST"])
def send():
    if request.content_type and "application/json" in request.content_type:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form or {}

    ok, err = check_auth()
    if not ok:
        return jsonify({"error": err}), 401

    to_raw = data.get("to_phone") or data.get("to") or ""
    to = normalize_phone(to_raw)
    if not to:
        return jsonify({"error": "Missing or invalid to_phone (UK E.164)"}), 400

    body = data.get("body") or ""
    urgency = data.get("urgency")
    address = data.get("address")
    issue = data.get("issue")
    postcode = data.get("postcode")
    message_body = format_dispatch_message(urgency, address, issue, postcode, body)

    from_number = os.environ.get("TWILIO_WHATSAPP_FROM")
    if not from_number or not from_number.startswith("whatsapp:"):
        return jsonify({"error": "TWILIO_WHATSAPP_FROM not set (e.g. whatsapp:+14155238886)"}), 500

    client = get_client()
    if not client:
        return jsonify({"error": "Twilio credentials not configured"}), 500

    try:
        msg = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to,
        )
        return jsonify({"sid": msg.sid, "status": msg.status}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
