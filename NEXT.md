# What's next

## Status snapshot (updated 2026-04-09)

### Done
- [x] Domain: **londonplumberai.co.uk** — purchased
- [x] Netlify deploy — live
- [x] Stripe payment links wired to pricing cards
- [x] Google Sheets "Plumber Leads V1" — set up and shared with Make.com
- [x] Make.com scenario — built and configured (webhook → Bland → Sheets → SMS)
- [x] Bland pathway — 21-node pathway built, pathway ID `e3caf18f-3bda-4927-b6dd-437a6d5e903b` in Make.com
- [x] Bland UI: branded persona `{{ai_name}}`, revised opening, merged Q1+Q2, pathway ID confirmed
- [x] ICO registration number **ZC102733** added to site (index.html, privacy-policy.html, terms.html)

### Blockers / Problems
- [x] **ICO Data Protection Fee — FAILED**: Payment of £52.00 returned unpaid. Must retry payment at ico.org.uk before processing personal data commercially.
- [x] **Facebook/Meta ads — PERMANENTLY DISABLED**: Account permanently disabled, no further review available. Facebook is a dead channel for this project. Need alternative acquisition strategy.

---

## 1. Bland UI (manual)

- [x] Add `{{ai_name}}` to Node 1 opening (branded persona per plumber).
- [x] Apply revised opening (remove "got 30 seconds" preamble).
- [x] Merge Q1 + Q2 into one natural question.
- [ ] Run "loo overflow in Clapham flat" slang test (after E2E is up, then tweak slang).
- [x] Confirm pathway ID is the one used in Make.com (Module 4).

## 2. Security & config

- [ ] **Bland API key in `.env`** — create `.env` with `BLAND_API_KEY=your_key`, load via python-dotenv. Never commit.
- [ ] **Webhook auth in Make.com** — add custom header/token to Webhooks module so only you can trigger.
- [ ] **Make.com Core** — upgrade if exceeding ~100 ops/month ($9/mo).

## 3. Ops / Testing

- [ ] Run all 10 test scenarios (`test_webhook.py` + `2_bland_setup.py`).
- [ ] Voice quality sign-off from 2 people.
- [ ] Full E2E: webhook → call → CRM → SMS.

## 4. Go-live

- [x] Buy **londonplumberai.co.uk** — done
- [x] Deploy to Netlify — done
- [ ] Set up **live demo Bland number** (clone pathway for demo).
- [ ] Record **"loo overflow in Clapham flat"** demo call for the site.
- [x] Stripe payment link (£297/month) — done
- [ ] **LinkedIn** page + first post ("Called 20 plumbers, 14 went to voicemail").
- [ ] List of **20 target London plumbers** + cold outreach (use `outreach.html`).

## 5. Acquisition (Facebook DEAD — find alternative)

- Facebook/Meta permanently banned — no ads possible on that channel.
- Alternatives to consider: Google Ads, LinkedIn ads/DMs, cold email, SEO, TikTok, direct outreach via outreach.html.

## 6. Optional: WhatsApp instead of SMS

- [ ] Deploy `whatsapp-service/` to Hetzner (Lucky). Set `TWILIO_WHATSAPP_FROM`.
- [ ] In Make.com, add HTTP module to POST to `https://your-server/send`.

## 7. ICO Data Protection Fee (RETRY REQUIRED)

- ICO number ZC102733 registered but **£52.00 payment returned unpaid**.
- Must retry payment at ico.org.uk before going live and processing personal data.
