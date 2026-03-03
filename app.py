import os, logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.genai as genai
from google.genai import types

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("dx-egypt-client")

app = Flask(__name__)
CORS(app)

# The client uses their own Gemini key or another AI service for the Chatbot part (Customer Service)
# This is separate from the Wasel SaaS engine which handles the vision translation.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

# Digital Egypt Customer Service Prompt
CUSTOMER_SERVICE_PROMPT = """
أنت ممثل خدمة عملاء ذكي وبشوش تعمل لدى بوابة "مصر الرقمية" للخدمات الحكومية.
تتحدث مع مواطن مصري من الصم وضعاف السمع، وتمت ترجمة لغة إشارته إلى نص عربي.
مهمتك:
1. الترحيب به بلطف وبلهجة مصرية محترمة وودودة.
2. فهم سؤاله والرد عليه بإجابة قصيرة ومفيدة جداً تخص خدمات مصر الرقمية (مثل: التموين، التوثيق، المرور، الأحوال المدنية).
3. اجعل الرد قصيراً (سطرين كحد أقصى) ومباشراً ليناسب المحادثة السريعة.
النص المترجم من لغة الإشارة الخاصة بالمواطن:
"""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Receives translated text and generates a customer service response."""
    if not client:
        return jsonify({"error": "Backend AI not configured."}), 500

    data = request.json
    user_text = data.get("text", "").strip()
    
    if not user_text:
        return jsonify({"error": "No text provided"}), 400

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[CUSTOMER_SERVICE_PROMPT + "\n[" + user_text + "]"],
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=150
            )
        )
        return jsonify({"reply": response.text.replace("*", "").strip()}), 200
    except Exception as e:
        logger.error(f"Chat API Error: {e}")
        return jsonify({"error": "Failed to generate reply"}), 500

if __name__ == "__main__":
    print("="*50)
    print(" 🇪🇬 Digital Egypt Sign Language Demo Client")
    print("="*50)
    app.run(host="0.0.0.0", port=3000, debug=False)
