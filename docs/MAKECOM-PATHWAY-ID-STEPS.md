# Put the Bland pathway ID into Make.com (step-by-step)

**Your Bland pathway ID:** `e3caf18f-3bda-4927-b6dd-437a6d5e903b`

Copy that ID and use it in Make.com as below.

---

## Steps in Make.com

1. **Open Make.com** and log in. Go to **Scenarios** and open the scenario that has:
   - **Webhooks** (first module, trigger)
   - **HTTP – Make a request** (second module, blue globe icon)

2. **Click the second module** — the first blue **HTTP** box (the one right after the pink Webhooks box). That module is the one that starts the Bland call.

3. **Open the HTTP request settings.** You should see:
   - **URL** (Bland’s API endpoint, e.g. `https://api.bland.ai/v1/calls` or similar)
   - **Method** (usually **POST**)
   - **Body type** (e.g. **Raw** or **JSON**)

4. **Find where the pathway is set.** In the request **body** (or in a **Body** / **Request content** section), look for a field named one of:
   - `pathway_id`
   - `pathway`
   - **Pathway ID**

   If you’re editing **raw JSON**, the body might look like:
   ```json
   {
     "phone_number": "...",
     "pathway_id": "PASTE_ID_HERE",
     ...
   }
   ```
   If you’re using **form fields**, there will be a key like `pathway_id` and a value box.

5. **Set the value to your pathway ID:**
   - **Paste or type:** `e3caf18f-3bda-4927-b6dd-437a6d5e903b`
   - Replace any old ID that’s there. Don’t add extra quotes if the field is already a “value” field; if it’s raw JSON, keep the quotes: `"e3caf18f-3bda-4927-b6dd-437a6d5e903b"`.

6. **Save the module** (OK / Save / checkmark). Then **save the scenario** (Save button in the bottom bar).

---

## If you don’t see pathway_id

- If the HTTP module uses **Bland’s built-in Make.com app** (e.g. “Bland.ai – Create a call”), open that module and look for a **Pathway** or **Pathway ID** dropdown or text field. Paste `e3caf18f-3bda-4927-b6dd-437a6d5e903b` there.
- If the body is **form** (key/value), add or edit a key `pathway_id` with value `e3caf18f-3bda-4927-b6dd-437a6d5e903b`.

Once that’s saved, your scenario will use this Bland pathway (the 21-node plumber flow) when it starts a call.

---

## Optional improvements (noted for later)

- **Personalised opening:** Add `lead_name` and `ai_name` to `request_data` (if the webhook provides them) so the pathway’s opening uses `{{lead_name}}` and `{{ai_name}}`.
- **Call length:** Consider increasing `max_duration` from 3 to 5–10 minutes if full intake (address, issue, postcode, tenant/landlord, scheduling) often runs longer.
