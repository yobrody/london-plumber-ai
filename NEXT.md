# What’s next (ICO last)

Ordered checklist. ICO registration is intentionally last.

## 1. Bland UI (manual)

- [x] Add `{{ai_name}}` to Node 1 opening (branded persona per plumber).
- [x] Apply revised opening (remove “got 30 seconds” preamble).
- [x] Merge Q1 + Q2 into one natural question.
- [ ] Run “loo overflow in Clapham flat” slang test (Bland → Chat with Pathway).
- [ ] Confirm pathway ID is the one used in Make.com (Module 4).

## 2. Security & config

- [ ] Move Bland API key to `.env` (when `2_bland_setup.py` or similar is in this repo or on the same machine).
- [ ] Add webhook auth token to Make.com Module 1 (so only your scenario can trigger the webhook).
- [ ] Upgrade Make.com to Core ($9/mo) for more than ~100 leads/month.

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
