# WhatsApp dispatch alerts — LondonPlumberAI

Flask microservice that sends lead/alert messages to plumbers via **Twilio WhatsApp**. Make.com can call it instead of (or in addition to) Twilio SMS when a lead is URGENT or SCHEDULED.

## Local run

```bash
cd whatsapp-service
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Twilio SID, token, and TWILIO_WHATSAPP_FROM (WhatsApp sandbox or number)
flask --app whatsapp_alerts run
# Or: python whatsapp_alerts.py
```

## Endpoints

| Method | Path    | Description |
|--------|---------|-------------|
| GET    | /health | Health check (for Lucky/Hetzner). |
| POST   | /send   | Send one WhatsApp message. |

### POST /send

**Auth (optional):** If `WEBHOOK_AUTH_TOKEN` is set, send either header `X-Webhook-Token: <token>` or query `?token=<token>`.

**Body (JSON or form):**

| Field     | Required | Description |
|-----------|----------|-------------|
| to_phone  | Yes      | Plumber number, UK E.164 (e.g. `447401097118` or `+44 7401 097118`). |
| body      | No*      | Full message text. If omitted, message is built from urgency/address/issue/postcode. |
| urgency   | No       | `URGENT` or `SCHEDULED` — adds emoji and label. |
| address   | No       | Lead address. |
| issue     | No       | Issue type from Bland. |
| postcode  | No       | Postcode. |

\* If `body` is provided, it is sent as-is; otherwise a formatted alert is built.

**Example (Make.com HTTP module):**

- URL: `https://your-hetzner-server/send`
- Method: POST
- Body type: JSON
- JSON:
  ```json
  {
    "to_phone": "447401097118",
    "urgency": "URGENT",
    "address": "12 High Street, SW4",
    "issue": "Burst pipe",
    "postcode": "SW4"
  }
  ```
- Header: `X-Webhook-Token: <WEBHOOK_AUTH_TOKEN>` (if set).

## Deploy to Hetzner (via Lucky)

1. **Server:** Ensure the Hetzner VPS (e.g. OpenClaw/Lucky host) has Python 3.10+ and a way to run the app (systemd, Docker, or Lucky-managed process).
2. **Secrets:** Put `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_WHATSAPP_FROM` (and optionally `WEBHOOK_AUTH_TOKEN`) in env or a secret store Lucky uses.
3. **Run:** e.g. `gunicorn -w 1 -b 0.0.0.0:5000 whatsapp_alerts:app`.
4. **Reverse proxy:** Expose `/send` and `/health` via nginx or your gateway; use HTTPS and keep `WEBHOOK_AUTH_TOKEN` so only Make.com can call `/send`.

## Twilio WhatsApp setup

- **Sandbox:** Twilio Console → Messaging → Try it out → Send a WhatsApp message. Use the sandbox “from” number (e.g. `whatsapp:+14155238886`). Recipients must join the sandbox (send the join code to the number).
- **Production:** Request a Twilio WhatsApp sender; set `TWILIO_WHATSAPP_FROM` to that number in `whatsapp:+...` form.

## Make.com: switch from SMS to WhatsApp

In the scenario where you currently send SMS (Paths 1 and 4), add an HTTP module that POSTs to this service with `to_phone`, `urgency`, `address`, `issue`, `postcode`. You can keep SMS as fallback or replace it once WhatsApp is verified.
