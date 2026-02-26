# Scripts (Bland / Make.com)

When you add call-dispatch or webhook scripts (e.g. `2_bland_setup.py` from D:\Development\PlumberAI):

1. **Secrets in `.env`** — Do not hardcode Bland API key or webhook URLs. In the script:
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   api_key = os.environ.get("BLAND_API_KEY")
   ```
2. **`.env`** — Create in this directory or repo root with `BLAND_API_KEY=...`, and add `.env` to `.gitignore` (already ignored in `whatsapp-service/`).
3. **Make.com webhook** — Use the auth token in Make.com Module 1 so the webhook URL is not public.
