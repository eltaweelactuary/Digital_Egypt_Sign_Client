# 🇪🇬 Digital Egypt (مصر الرقمية) - Sign Language Demo Client

This repository acts as a **B2B Client Showcase** demonstrating how external businesses or government portals can integrate the **Wasel Core AI Engine (SaaS)** into their own front-end applications.

## How it works (The complete cycle)

1. **Frontend (Browser):** Asks for camera permissions. Captures short 1-second motion chunks (3 frames).
2. **Translation Request:** Sends these 3 frames as `images_base64` to the Wasel SaaS API.
3. **Receipt:** Receives the translation (e.g., "بطاقة تموين") and prints it to the user chat screen.
4. **Customer Service Bot:** The client's frontend then hits its own local backend (`/chat`) which connects to its own AI model to reply: "أهلاً بك، هل تود تجديد أو إصدار بطاقة التموين؟"

## Setup & Running

**1. Install dependencies:**
```bash
pip install -r requirements.txt
```

**2. Setup Environment Variables:**
The client application only needs an API key for the conversational AI (e.g., Gemini) to act as the chatbot. It does *not* need the API key for the Wasel Vision engine (that is handled via the `X-API-Key` sent to the SaaS URL).

```powershell
$env:GEMINI_API_KEY="Your_Conversational_Google_Key"
```

**3. Run the Client:**
```bash
python app.py
```
*Open `http://localhost:3000` in your browser.*

## Integration Pointers for Developers
* Look at `templates/index.html` to see the `captureMotionChunk()` function implementing dynamic frame arrays.
* Look at the `fetch` block inside `engineLoop()` to see how the frontend handles the `X-API-Key` and deals with `204 No Content` for empty signals.
