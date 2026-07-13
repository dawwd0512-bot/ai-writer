from flask import Flask, request, render_template_string
import requests
import json

app = Flask(__name__)

# ============================================
# مفتاح Google Gemini API (ضع المفتاح الصحيح هنا)
# ============================================
GEMINI_API_KEY = "AQ.Ab8RN6LS8QCs0Eg4cg8zueyJSrQorzHP7tKlkS_lP187RG63Og"  # استبدل هذا بالمفتاح الحقيقي

# ============================================
# دالة الاتصال بـ Gemini API (نسخة معدلة)
# ============================================
def ask_gemini(prompt):
    # استخدام الإصدار v1beta مع نموذج gemini-1.5-flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if "candidates" in data:
                return data["candidates"][0]["content"]["parts"][0]["text"]
        return f"⚠️ خطأ: {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ فشل الاتصال: {str(e)}"

# ============================================
# واجهة الموقع (نفس التصميم)
# ============================================
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Writer Pro - Gemini</title>
    <style>
        body{font-family:sans-serif;background:#0f0c29;color:white;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}
        .container{background:rgba(255,255,255,0.1);padding:40px;border-radius:20px;max-width:600px;width:100%}
        textarea{width:100%;padding:10px;border-radius:10px;border:none;min-height:100px}
        button{width:100%;padding:10px;background:#ffd200;color:#1a1a2e;border:none;border-radius:10px;font-size:18px;cursor:pointer;margin-top:10px}
        .result{background:#333;padding:15px;border-radius:10px;margin-top:20px;white-space:pre-wrap}
    </style>
</head>
<body>
<div class="container">
    <h2>🤖 AI Writer Pro (Gemini 1.5 Flash)</h2>
    <form method="POST">
        <textarea name="text" placeholder="اكتب أي سؤال..."></textarea>
        <button type="submit">🚀 اسأل</button>
    </form>
    {% if result %}
    <div class="result">{{ result }}</div>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        text = request.form.get("text")
        if text:
            result = ask_gemini(text)
    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
