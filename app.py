from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

API_TOKEN = "hf_put_your_token_here"  # غير هذا بالمفتاح

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

def ask_ai(prompt):
    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    try:
        r = requests.post(url, headers=headers, json={"inputs": prompt}, timeout=30)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and len(data) > 0:
                return data[0].get("generated_text", "ما في رد")
        return f"خطأ: {r.status_code}"
    except Exception as e:
        return f"فشل: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        text = request.form.get("text")
        if text:
            result = ask_ai(text)
    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
