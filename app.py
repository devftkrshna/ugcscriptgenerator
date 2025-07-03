from flask import Flask, request, render_template_string, redirect, url_for, session
from openai import OpenAI
from collections import defaultdict
import markdown2
import json
import os
from dotenv import load_dotenv
import os

load_dotenv() 

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# User credentials
user_credentials = {
    'maitriiiwadhwaa': '8652093953',
'life.as.prerna': '8955495635',
'nehasharma.3_': '7982747086',
'_her.aesthetics': '9817904361',
'sneha_mishra2903': '8824975828',
'ft.kshitija__': '9321866796',
'ugh_mehak': '9893666154',
'harikasdiary_': '9133428452',
'palakkveermaaa': '9667837199',
'kayvieeee': '7678622417',
'kratiijoshi': '6376349880',
'capturedbyanushka': '9650828004',
'gupta_bhumika19': '8920730907',
'hitanshi_stylez': '8962925434',
'Withprernaa': '9599234586',
'thatprettyme_': '8708295424',
'_her.digitaldiary_': '8743004423',
'sassy_siddhi': '8983470666',
'sunflowerscamera': '7303446266',
'livewithru': '7710977482',
'shruu.tii___': '9579854154',
'heyy.aryann': '7878086369',
'sezzhjll_': '9301907676',
'skinCraftedUGC': '7985716865',
'graceinsonn': '7668936337',
'jyotismita_._': '8472803083',
'life.of.surbs': '9210575240',
'deepiiikaa._': '7494952443',
'vanshikaadadhich': '8890427614',
'aesthe.tic_latte': '7997812614',
'khushiiiiaggarwal': '9810123138',
'khushbu_thadani': '7597599189',
'riii.yaaa_____': '9625334622',
'wolfgang_97_': '9990386104',
'_aditijain_24': '7982679856',
'blync.now':'6280221837',
}

# Persistent usage file
USAGE_FILE = 'usage_data.json'

def load_usage():
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_usage(data):
    with open(USAGE_FILE, 'w') as f:
        json.dump(data, f)

user_usage = load_usage()

demo_scripts = [
    {
        "inputs": {
            "product_name": "GlowBerry Serum",
            "product_type": "Skincare",
            "platform": "Instagram",
            "tone": "Relatable",
            "creator_role": "Consumer",
            "problem": "Dull and uneven skin tone",
            "target_audience": "College girls aged 18-25"
        },
        "output": """UGC Video Script for GlowBerry Serum (Instagram Reels, 30-45 sec)

1. Hook (0-3 sec)
Script:
“Ugh, does anyone else feel like their skin is just... blah lately?”

Visual:
Close-up selfie shot, natural lighting, slightly frustrated facial expression. Casual background (bedroom or dorm room).

On-screen text:
“Dull skin? Same here 😩”

2. Relatable Problem (3-10 sec)
Script:
“I’ve been dealing with this dull, uneven skin tone ever since classes got crazy. Makeup just doesn’t fix it.”

Visual:
Mid-shot showing your face, gently touching cheeks, looking tired but real. Maybe a quick swipe of makeup failing to cover dullness.

On-screen text:
“Tired of dull, uneven skin?”

3. Introducing the Product Naturally (10-20 sec)
Script:
“Then I found GlowBerry Serum — it’s super lightweight and smells amazing. I just add a few drops before my moisturizer every morning.”

Visual:
Show the serum bottle close-up, drop a few drops on hand, then gently pat on face. Soft smile, relaxed vibe.

On-screen text:
“GlowBerry Serum ✨ Lightweight & fresh scent”

4. Highlight Features / Use Experience (20-35 sec)
Script:
“It’s helped brighten my skin so much, and it’s not sticky at all. Plus, my makeup goes on way smoother now!”

Visual:
Before-and-after quick flash (could be a subtle glow effect), then applying makeup easily. Natural smile, confident.

On-screen text:
“Brightens + smooths skin 👏”

5. Soft CTA (35-45 sec)
Script:
“If you want to glow up your skin too, definitely try GlowBerry Serum. Link’s in my bio!”

Visual:
Friendly close-up, pointing upwards (to bio), genuine smile.

On-screen text:
“Try it yourself! ☀️ Link in bio”
"""
    },
    {
        "inputs": {
            "product_name": "HairGuard Oil",
            "product_type": "Haircare",
            "platform": "YouTube Shorts",
            "tone": "Funny",
            "creator_role": "Sister",
            "problem": "Hair fall and dandruff",
            "target_audience": "Teenagers and young adults"
        },
        "output": """**Hook:** My hairline was running faster than me!  
**Problem:** I couldn’t even comb without losing a dozen strands.  
**Solution:** HairGuard Oil changed the game.  
**Experience:** 2 weeks in, less hair fall and zero flakes.  
**CTA:** Don’t wait — get it now!"""
    }
]

login_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login | UGC Generator</title>
    <style>
        body { margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; background: #f3f4f6; display: flex; align-items: center; justify-content: center; height: 100vh; }
        .login-box {
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 400px;
        }
        h2 { margin-bottom: 25px; text-align: center; color: #333; }
        input[type=text], input[type=password] {
            width: 100%; padding: 12px; margin-bottom: 15px;
            border: 1px solid #ccc; border-radius: 8px;
        }
        input[type=submit] {
            width: 100%; padding: 12px; background: #007bff;
            color: white; border: none; border-radius: 8px; cursor: pointer;
            font-weight: bold;
        }
        .error { color: red; text-align: center; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Login to UGC Script Generator</h2>
        <form method="POST" action="/login">
            <input type="text" name="username" placeholder="Agency Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <input type="submit" value="Login">
        </form>
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
'''
dashboard_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>UGC Script Generator</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f3f4f6; padding: 40px; }
        .container {
            max-width: 1000px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.05);
        }
        h1 { color: #111; margin-bottom: 20px; text-align: center; }
        form label { display: block; margin-top: 15px; font-weight: bold; }
        form input[type=text] {
            width: 100%; padding: 12px; margin-top: 5px;
            border: 1px solid #ccc; border-radius: 8px;
        }
        input[type=submit] {
            margin-top: 25px; background: #28a745; color: white;
            border: none; padding: 12px 20px; border-radius: 8px;
            font-size: 16px; font-weight: bold; cursor: pointer;
        }
        .section { margin-top: 40px; }
        .demo-box, .output-box {
            background: #f9fafb; padding: 20px; border-radius: 10px;
            margin-bottom: 20px;
        }
        pre { white-space: pre-wrap; font-family: 'Courier New'; background: #eef1f6; padding: 10px; border-radius: 6px; }
        .usage { margin-bottom: 20px; font-weight: bold; }
        .logout { float: right; }
        .label-title { margin-top: 40px; font-size: 18px; font-weight: bold; border-bottom: 1px solid #ddd; padding-bottom: 5px; }
    </style>
</head>
<body>
<div class="container">
    <div class="logout"><a href="/logout">Logout</a></div>
    <h1>UGC Script Generator</h1>
    <div class="usage">Hi <b>{{ user }}</b> — You’ve generated {{ usage_count }}/5 scripts</div>

    {% if usage_count < 5 %}
    <form method="POST" action="/generate">
        <label>Product Name</label>
        <input type="text" name="product_name" placeholder="e.g. GlowBerry Serum" required>
        <label>Product Type</label>
        <input type="text" name="product_type" placeholder="e.g. Skincare" required>
        <label>Platform</label>
        <input type="text" name="platform" placeholder="e.g. Instagram">
        <label>Tone</label>
        <input type="text" name="tone" placeholder="e.g. Relatable">
        <label>Creator Role</label>
        <input type="text" name="creator_role" value="Consumer">
        <label>Problem it Solves</label>
        <input type="text" name="problem" placeholder="e.g. Uneven tone" required>
        <label>Target Audience</label>
        <input type="text" name="target_audience" placeholder="e.g. 18–25 year girls" required>
        <input type="submit" value="Generate UGC Script">
    </form>
    {% else %}
    <p style="color: red;"><b>You have reached your generation limit.</b></p>
    {% endif %}

    {% if script %}
    <div class="section">
        <div class="label-title">🎬 Generated Script</div>
        <div class="output-box">
            {{ script|safe }}
        </div>
    </div>
    {% endif %}

    <div class="section">
        <div class="label-title">📌 Demo Scripts</div>
        {% for demo in demo_scripts %}
        <div class="demo-box">
            <strong>Input:</strong>
            <ul>
                <li><b>Product:</b> {{ demo.inputs.product_name }}</li>
                <li><b>Type:</b> {{ demo.inputs.product_type }}</li>
                <li><b>Platform:</b> {{ demo.inputs.platform }}</li>
                <li><b>Tone:</b> {{ demo.inputs.tone }}</li>
                <li><b>Role:</b> {{ demo.inputs.creator_role }}</li>
                <li><b>Problem:</b> {{ demo.inputs.problem }}</li>
                <li><b>Audience:</b> {{ demo.inputs.target_audience }}</li>
            </ul>
            <strong>Output:</strong>
            <pre>{{ demo.output }}</pre>
        </div>
        {% endfor %}
    </div>
</div>
</body>
</html>
'''
@app.route('/')
def home():
    if 'user' in session:
        return redirect('/dashboard')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        if u in user_credentials and user_credentials[u] == p:
            session['user'] = u
            return redirect('/dashboard')
        else:
            return render_template_string(login_template, error="Invalid credentials or You have used your free Credits!!")
    return render_template_string(login_template, error=None)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    user = session['user']
    return render_template_string(
        dashboard_template,
        user=user,
        usage_count=user_usage.get(user, 0),
        script=None,
        demo_scripts=demo_scripts
    )

@app.route('/generate', methods=['POST'])
def generate():
    if 'user' not in session:
        return redirect('/login')
    user = session['user']
    if user_usage.get(user, 0) >= 5:
        return redirect('/dashboard')

    data = request.form
    prompt = f"""
You are a UGC copywriter and influencer marketing expert.
Based on the inputs below, generate a step-by-step UGC video script that hooks the viewer, showcases the product authentically, and ends with a soft CTA.
Break the script into clear steps (Hook, Problem, Solution, CTA).
Keep it simple, human, and optimized for short-form videos.

Inputs:
- Product Name: {data['product_name']}
- Product Type: {data['product_type']}
- Platform: {data['platform']}
- Tone: {data['tone']}
- Creator Role: {data['creator_role']}
- Problem it Solves: {data['problem']}
- Target Audience: {data['target_audience']}

Generate a 30-45 second video script with:
1. Hook (first 3 seconds)
2. Relatable problem or experience
3. Introducing the product naturally
4. Highlight 1-2 features or use experience
5. Soft CTA (e.g. "try it yourself", "link in bio")

Also suggest:
- Visual ideas for each step (camera angle, props)
- Optional on-screen text (captions)

Make it short, real, and high-conversion.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "UGC Script Writer"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=600
    )

    script = markdown2.markdown(response.choices[0].message.content.strip())

    user_usage[user] = user_usage.get(user, 0) + 1
    save_usage(user_usage)

    return render_template_string(
        dashboard_template,
        user=user,
        usage_count=user_usage[user],
        script=script,
        demo_scripts=demo_scripts
    )

if __name__ == '__main__':
    app.run(debug=True)