# What to tell Bland’s Norm AI assistant

Copy the **Main prompt** below into Norm. It tells Norm exactly what the pathway must do and how Bland’s bot receives and acts on information (nodes, conditions, variables). Use the **Follow-up checklist** if Norm doesn’t do everything in one go.

---

## Main prompt (paste this to Norm)

*ch step. Use **pathways** between nodes with **conditions** so the next node depends on what the user said or what was extracted (e.g. “if postcode not in London area → go to out-of-area node”; “if issue is burst pipe / no water / flooding / gas → URGENT”).  
- In each node, the bot **speaks** from the node’s prompt and **listens** for the user’s answer; then **extract variables** from that turn (or from the whole conversation so far) and route via **conditions** on the pathways.  
- Use **global** or first nodes for: (1) **Opt-out** — if the user says they want to stop, be removed, or not be called again, **end the call immediately** and set status to opt-out. (2) **Confusion** — if the user is confused or asks for a human, offer a callback from a real person and set status accordingly, then end or route. (3) **Objections** — if they say “are you a robot?”, question the price, or hesitate, *Role and product**  
This pathway is for an **outbound** AI receptionist for a **London plumber**. The call is triggered when someone submits a web form; we ring them back within 60 seconds. The bot must: (1) confirm who we’re speaking to and what they need, (2) triage urgency and check they’re in our London postcode area, (3) capture job details and property/tenant info, (4) either schedule or hand off (e.g. out-of-area). Everything must work with **variables** and **nodes**: the bot receives `{{lead_name}}`, `{{plumber_name}}`, and `{{ai_name}}` at the start (so each plumber can have a branded AI name). Every node that collects information must **extract variables** so our automation (Make.com) gets: `issue` (or issue_type), `postcode`, `urgency` (URGENT / PRIORITY / STANDARD), `property` (e.g. homeowner / tenant / commercial), `status` (e.g. scheduled / callback_requested / opt_out / out_of_area), and `full_address`. Tenant calls must also capture **landlord name** and **landlord phone** in a dedicated sub-flow.

**How the bot should work (Bland terms)**  
- Use **nodes** for eaacknowledge and **return to the previous node** (don’t end).  
- **Opening (first real node after any global checks):** Do **not** say “got 30 seconds” or similar. Start with a short, natural opener that uses `{{ai_name}}`, `{{plumber_name}}`, and `{{lead_name}}`, e.g. “Hi {{lead_name}}, this is {{ai_name}} from {{plumber_name}}. You asked for a call back about a plumbing issue — can you tell me what’s going on and your postcode?” Merge the “what’s going on” and “postcode” into **one natural question** (not two separate Q1 and Q2 nodes).  
- **Emergency detection:** From their first answer, classify **issue_type** and whether there’s **active damage** (flooding, burst pipe, no water, frozen pipes, gas smell). If emergency, set **urgency** to URGENT and route to an urgent-handling node that: (1) gives **safety guidance** (e.g. “If you have a burst pipe, turn off your stopcock if you can”), (2) confirms address and that we’ll get someone out.  
- **Triage:** Assign **urgency** as URGENT / PRIORITY / STANDARD. **Out-of-area:** London postcodes only: SW1–SW10, W1–W11, WC1, WC2, EC1–EC4. If postcode is outside these, go to an **out-of-area** node: politely say we don’t cover that area and offer to **send a text with an alternative plumber** if they want; then end and set status to out_of_area.  
- **Job details:** In the main flow, collect **full_address**, **issue_type** (e.g. leak, boiler, blocked drain, overflow), and **property_type**: homeowner, tenant, or commercial. If **tenant**, branch to a **tenant sub-flow** (separate nodes) to capture **landlord name** and **landlord phone**.  
- **British English only:** Voice and wording must be British: “postcode” not “zip”, “flat” not “apartment”, “loo”/“overflow” understood. Train the model on phrases like “loo overflow in a Clapham flat” → extract issue_type e.g. “overflow”, property_type “tenant” (or “flat”), postcode SW4/Clapham.  
- **“Not a good time”:** If they say they can’t talk now, offer to call back later, set status to **callback_requested**, and end gracefully.  
- **Scheduling:** If they’re in area and want to book, capture that and set status to **scheduled** (or equivalent); you can mention a booking link or “we’ll get you in the diary” — no need for live calendar in this pathway.  
- **Recording and voicemail:** Ensure the call is **recorded**. If the system detects **voicemail** (answered_by_enabled), **hang up** and do not leave a message.  
- **Tone:** Professional, warm, concise. No forbidden phrases (e.g. no “I’m just a bot” or “I don’t have that information” in a way that sounds evasive). If you have a **global tone prompt** or **forbidden phrases** list, apply it to all nodes.  
- **PECR:** In the **opening**, include a brief, clear disclosure that this is an **automated call** (e.g. “This is an automated call from {{plumber_name}}.”) so we comply with outbound automated-call rules.

**Variables to extract (for Make.com)**  
Ensure these are **extracted** and available at end of call (or when routing): **issue** (or issue_type), **postcode**, **urgency** (URGENT / PRIORITY / STANDARD), **property** (homeowner / tenant / commercial), **status** (scheduled / callback_requested / opt_out / out_of_area / no_answer, etc.), **full_address**. For tenant flow add **landlord_name**, **landlord_phone**. Use your **Extract Variables** (or equivalent) on the relevant nodes so the API/payload returns these.

**Summary for Norm**  
Build or update this pathway so it: (1) uses {{ai_name}}, {{plumber_name}}, {{lead_name}} in the opening and a single merged “what’s wrong + postcode” question with no “got 30 seconds” line; (2) has global opt-out, confusion, and objection handling; (3) detects emergencies and gives safety guidance; (4) enforces London postcodes and out-of-area exit with optional text for another plumber; (5) captures address, issue, property type, and tenant landlord details where needed; (6) uses British English and understands plumber slang like “loo overflow in Clapham flat”; (7) records calls and hangs up on voicemail; (8) includes a short “automated call” disclosure in the opening; (9) extracts all variables above for our automation.

---

## Follow-up checklist (if Norm misses something)

Tell Norm to add or fix:

- [ ] **Opening:** Uses `{{ai_name}}`, `{{plumber_name}}`, `{{lead_name}}`; one natural question for “what’s wrong and postcode”; no “got 30 seconds”; short “this is an automated call” line.
- [ ] **Global nodes:** (1) Opt-out → end call and set opt_out. (2) Confusion → offer human callback. (3) Objections → return to previous node.
- [ ] **Emergency:** Detect burst pipe, leak, flooding, no water, frozen pipes; set URGENT; node with safety guidance (e.g. stopcock).
- [ ] **London postcodes:** Only SW1–SW10, W1–W11, WC1, WC2, EC1–EC4; else out-of-area node and offer to text alternative plumber.
- [ ] **Tenant flow:** Separate nodes for landlord name and landlord phone; extract both.
- [ ] **Extract variables:** issue/issue_type, postcode, urgency, property, status, full_address, landlord_name, landlord_phone (for tenants).
- [ ] **British English** and **plumber slang** (e.g. “loo overflow in Clapham flat” → overflow, tenant/flat, SW4).
- [ ] **Voicemail:** Hang up when answered_by indicates voicemail.
- [ ] **Recording:** Enabled for the call.

---

## After Norm is done

**Done (pathway built):** Opening with {{ai_name}}, {{plumber_name}}, {{lead_name}}; merged question; PECR disclosure; no "got 30 seconds". Global nodes: Opt Out, Confusion, Not Good Time, Objections. Emergency detection + safety guidance (stopcock, gas 0800 111 999). London postcodes SW1–SW10, W1–W11, WC1, WC2, EC1–EC4; out-of-area offers text for alternative plumber. Tenant flow → landlord_name, landlord_phone. Variables: issue_type, urgency_level, postcode, property_type, landlord_name, landlord_phone, full_address, caller_name, callback_number. British English; webhook to Make.com; recording on. 21 nodes, 23 edges.

**Still to do:**
1. Confirm the **pathway ID** is the one used in Make.com (Module 4 / Bland trigger).  
2. Run the **“loo overflow in Clapham flat”** test via Chat with Pathway; confirm issue_type, property_type, postcode extracted.  
3. Test opt-out, confusion, objection, and out-of-area flows once each.
