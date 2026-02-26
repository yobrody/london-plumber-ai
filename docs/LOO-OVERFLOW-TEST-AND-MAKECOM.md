# Why the “loo overflow in Clapham flat” test — and Make.com pathway ID

## What the slang test means and why it’s useful

**What it is:** A real sentence a London customer might say: *“I’ve got a loo overflow in a Clapham flat.”*

- **Loo** = toilet (British).
- **Overflow** = the plumbing problem (water overflowing from the basin/pan).
- **Clapham flat** = flat in Clapham, London (postcode area SW4); “flat” strongly suggests **tenant** or at least a specific **property type**.

**What we check:** When you run this in Bland’s “Chat with Pathway”, the bot should **extract** something like:

- `issue_type` = overflow (or similar)
- `property_type` = tenant or flat
- `postcode` = SW4 (or full postcode if it asks)

**Why it’s useful:**

1. **Demo credibility** — Competitors sell “plumber lingo training”. Showing the bot correctly handling “loo overflow in Clapham flat” proves it understands real British plumbing language and geography.
2. **Downstream automation** — Make.com and your CRM rely on those variables. If the bot misclassifies (e.g. wrong postcode or issue type), routing and SMS/WhatsApp alerts will be wrong.
3. **One test, many checks** — One phrase checks issue detection, property type, and London postcode logic in a single go.

So the test isn’t just “does it sound good” — it’s “does it **set the right variables** so the rest of the system works.”

---

## Step 2: Confirm pathway ID in Make.com (you do this)

**Important:** The number in your Make.com URL (e.g. `4408343` in `.../scenarios/4408343/edit`) is the **Make.com scenario ID** — it just identifies this workflow. The **pathway ID** you need is from **Bland AI** (a UUID like `e3caf18f-3bda-4927-b6dd-437a6d5e903b`). You get it in Bland, then paste it into the Make.com module that triggers the call.

### 1. Get the pathway ID from Bland (not from Make.com)

- Log in at **app.bland.ai** (or your Bland dashboard).
- Go to **Conversational Pathways** (or **Pathways**).
- Open the **plumber pathway** (the one with 21 nodes you built with Norm).
- The pathway ID is shown in one of these places (Bland’s UI varies):
  - **Pathway settings / details** (gear or “…” menu on the pathway card or inside the editor).
  - **Browser URL** when the pathway is open, e.g. `.../pathways/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`.
  - **API or “Use pathway”** section: when you click “Use via API” or “Get pathway ID”, it shows the UUID.
- Copy the full **UUID** (e.g. `e3caf18f-3bda-4927-b6dd-437a6d5e903b`). That is your **Bland pathway ID**.

### 2. Put that ID in Make.com

- In **Make.com**, open the scenario you showed (Webhooks → HTTP → Google Sheets → Sleep → HTTP). This is the one that receives the webhook and starts the Bland call.
- Click the **first blue “HTTP – Make a request”** module (the one right after the pink Webhooks trigger). That module should be the one calling Bland’s API to **start the outbound call**.
- Inside that HTTP module, look for where the request body or URL parameters are set. There should be a field for **pathway_id** or **pathway** (Bland’s API expects `pathway_id` in the JSON body when creating a call).
- **Paste the Bland pathway ID** (the UUID from step 1) into that field. If the field currently has an old or different UUID, replace it with the 21‑node pathway ID.
- **Save** the module, then save the scenario.

### 3. Optional: check variable names

- Your new pathway returns variables like: `issue_type`, `urgency_level`, `postcode`, `property_type`, `landlord_name`, `landlord_phone`, `full_address`, `caller_name`, `callback_number`.
- In the **next** Make.com module (the one that reads the Bland call result and writes to Sheets/CRM), make sure the **field mapping** uses these names (or map them to your sheet columns). If your scenario still expects old names (e.g. `issue` instead of `issue_type`), update the mapping so the right data goes into the right columns.

Once the pathway ID in Make.com matches the 21‑node pathway and the variable mapping is correct, your E2E flow (webhook → Bland call → result → CRM/SMS) will use the new behaviour.

---

## Is your Make.com scenario set up correctly?

From your screenshot, the **flow** is in the right order for the usual plumber flow:

1. **Webhooks (Custom webhook)** — Trigger when your form or system sends the lead (e.g. phone number, lead_name, plumber_name). The webhook URL here is what you (or Make.com) give to the form/script so it can start this scenario.
2. **HTTP (Make a request)** — This should be the call to **Bland’s API** to start the outbound call. It must use the **Bland pathway ID** (from Bland, step 1 above) in the request (e.g. in the JSON body as `pathway_id`), plus the phone number and any variables (e.g. `lead_name`, `plumber_name`, `ai_name`) from the webhook.
3. **Google Sheets (Add a row)** — Typically logs that a call was started (e.g. call_id, timestamp) so you have a record.
4. **Tools (Sleep)** — Waits for the call to finish (e.g. 5 minutes / 300 seconds) before checking the result.
5. **Second HTTP (Make a request)** — Usually a request to **Bland’s API** to get the **call result** (e.g. GET `/v1/calls/{call_id}`) so you get the extracted variables (issue_type, postcode, urgency_level, etc.), then later modules can write them to Sheets and route (e.g. send SMS).

So **yes, the structure looks correct.** To be sure it’s set up right for your 21‑node pathway:

- **First HTTP module:** Method is POST, URL is Bland’s “create call” endpoint, and the body includes `pathway_id` = your Bland pathway UUID (and phone number, variables). That’s where you confirm the pathway ID.
- **Webhook:** Expects the payload your form or script sends (e.g. phone, lead_name, plumber_name).
- **Google Sheets:** Maps the webhook/HTTP output to the right columns (and later, the second HTTP result to CRM columns using the new variable names).
- **Second HTTP:** Uses the `call_id` from the first HTTP response to fetch the completed call result from Bland, so the rest of the scenario can use `issue_type`, `postcode`, etc.
