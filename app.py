from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

# بنك ردود ذكية
responses = {
    "مرحبا": ["أهلاً بك! 🌟", "مرحباً! يسعدني وجودك."],
    "كيف": ["أنا بخير، شكراً!", "كل شيء تمام!"],
    "الذكاء الاصطناعي": ["🧠 هو محاكاة العقل البشري.", "🤖 هو مستقبل التكنولوجيا."],
    "بايثون": ["🐍 لغة برمجة سهلة وقوية.", "بايثون تستخدم في الذكاء الاصطناعي."],
    "فلسطين": ["🇵🇸 فلسطين أرض عربية، القدس عاصمتها.", "🕊️ نتمنى السلام لفلسطين."],
    "غزة": ["🇵🇸 غزة صامدة، نتمنى السلام لأهلها.", "💔 غزة تحتاج لدعم العالم."],
    "عدد سكان": ["🌍 عدد سكان الأرض 8.1 مليار.", "📊 آخر إحصائية 8.1 مليار نسمة."],
    "الوقت": ["🕐 الوقت الآن يعتمد على منطقتك.", "⏰ تحقق من الساعة في هاتفك."],
    "طقس": ["☀️ الطقس يختلف حسب المنطقة.", "🌧️ تحقق من تطبيق الطقس المحلي."],
}

def get_response(text):
    text_lower = text.lower()
    for key in responses:
        if key in text_lower:
            return random.choice(responses[key])
    return random.choice([
        "🤔 سؤال جميل! لكني لا أملك إجابة محددة.",
        "😅 اسألني عن: فلسطين، غزة، بايثون، ذكاء اصطناعي، أو مرحبا.",
        "🤖 جرب تسأل بطريقة أوضح."
    ])

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Writer Pro</title>
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
    <h2>🤖 AI Writer Pro</h2>
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
            result = get_response(text)
    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
