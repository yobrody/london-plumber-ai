# What’s next (ICO last)

Ordered checklist. ICO registration is intentionally last.

## 1. Bland UI (manual)

- [x] Add `{{ai_name}}` to Node 1 opening (branded persona per plumber).
- [x] Apply revised opening (remove “got 30 seconds” preamble).
- [x] Merge Q1 + Q2 into one natural question.
- [ ] Run “loo overflow in Clapham flat” slang test (later — after E2E is up, then tweak words like loo).
- [x] Confirm pathway ID is the one used in Make.com (Module 4).

## 2. Security & config (get everything up and running)

- [ ] **Bland API key in `.env`** — In the folder where your call script lives (e.g. `2_bland_setup.py` on D:\ or in `london-plumber-ai/scripts/`), create a `.env` with `BLAND_API_KEY=your_key`. In the script, load it (e.g. `os.environ.get("BLAND_API_KEY")` or `python-dotenv`). Never commit `.env`.
- [ ] **Webhook auth in Make.com** — Open your scenario → Webhooks module (Module 1) → add a **custom header** or **token** (e.g. `X-Webhook-Token: your_secret`). In the system that POSTs to the webhook (form, script), send that header/param so only you can trigger the scenario.
- [ ] **Make.com Core** — If you’ll exceed ~100 ops/month, upgrade at make.com/pricing to Core ($9/mo).

## 3. Ops

- [ ] Confirm Google Sheets “Plumber Leads V1” exists and is shared with Make.com service account (`4_GOOGLE_SHEETS_SETUP.md`).
- [ ] Run all 10 test scenarios (`test_webhook.py` + `2_bland_setup.py`).
- [ ] Voice quality sign-off from 2 people.
- [ ] Full E2E: webhook → call → CRM → SMS (and optionally WhatsApp via `whatsapp-service/`).

## 4. Go-live

- [ ] Buy **londonplumberai.co.uk** (e.g. Namecheap).
- [ ] Deploy this folder to **Netlify** (or Vercel): connect repo, publish directory = `london-plumber-ai` or repo root.
- [ ] Set up **live demo Bland number** (clone pathway for demo).
- [ ] Record **“loo overflow in Clapham flat”** demo call for the site.
- [ ] **Stripe** payment link (£297/month).
- [ ] **LinkedIn** page + first post (“Called 20 plumbers, 14 went to voicemail”).
- [ ] List of **20 target London plumbers** + cold outreach (use `outreach.html`).

## 5. Optional: WhatsApp instead of SMS

- [ ] Deploy `whatsapp-service/` to Hetzner (Lucky). Set `TWILIO_WHATSAPP_FROM` (sandbox or production).
- [ ] In Make.com, add HTTP module to POST to `https://your-server/send` with `to_phone`, `urgency`, `address`, `issue`, `postcode` (and `X-Webhook-Token` if set).

## 6. ICO registration (last)

- [ ] Register with ICO (ico.org.uk, ~£40/year). Required before processing personal data commercially.
