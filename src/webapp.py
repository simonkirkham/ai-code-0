from flask import Flask, request, render_template_string, send_file
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Countdown Generator</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Roboto:400,700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: #fff;
            border-radius: 16px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.12);
            padding: 40px 32px 32px 32px;
            max-width: 400px;
            width: 100%;
            text-align: center;
        }
        h1 {
            color: #4f3ca7;
            margin-bottom: 24px;
            font-weight: 700;
        }
        label {
            display: block;
            margin: 16px 0 8px 0;
            color: #333;
            font-weight: 500;
        }
        input[type="text"], input[type="date"], input[type="time"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            margin-bottom: 12px;
            font-size: 16px;
        }
        input[type="submit"] {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 12px 0;
            width: 100%;
            font-size: 18px;
            font-weight: 700;
            cursor: pointer;
            transition: background 0.2s;
        }
        input[type="submit"]:hover {
            background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
        }
        .countdown-section {
            margin-top: 32px;
        }
        .countdown-section h2 {
            color: #4f3ca7;
            margin-bottom: 16px;
        }
        .countdown-section img {
            border-radius: 12px;
            box-shadow: 0 2px 12px rgba(76, 61, 139, 0.15);
            max-width: 100%;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Countdown Image Generator</h1>
        <form method="post">
            <label for="occasion">Occasion:</label>
            <input type="text" id="occasion" name="occasion" required>
            <label for="date">Date:</label>
            <input type="date" id="date" name="date" required>
            <label for="time">Time:</label>
            <input type="time" id="time" name="time" required>
            <input type="submit" value="Create Countdown Image">
        </form>
        {% if image_url %}
        <div class="countdown-section">
            <h2>Countdown to {{ occasion }}</h2>
            <img src="{{ image_url }}" alt="Countdown Image">
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

def get_countdown_string(target_dt):
    now = datetime.now()
    diff = target_dt - now
    if diff.total_seconds() < 0:
        return "The date/time has already passed!"
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s left"

@app.route('/', methods=['GET', 'POST'])
def index():
    image_url = None
    occasion = None
    if request.method == 'POST':
        occasion = request.form['occasion']
        date_str = request.form['date']
        time_str = request.form['time']
        target_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        # Pass params in query string for image
        image_url = f"/countdown_image?date={date_str}&time={time_str}&occasion={occasion}"
    return render_template_string(HTML_FORM, image_url=image_url, occasion=occasion)

@app.route('/countdown_image')
def countdown_image():
    date_str = request.args.get('date')
    time_str = request.args.get('time')
    occasion = request.args.get('occasion', '')
    target_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    countdown = get_countdown_string(target_dt)
    # Create image
    img = Image.new('RGB', (500, 200), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    d.text((10, 40), f"Countdown to {occasion}", fill=(255,255,255), font=font)
    d.text((10, 100), countdown, fill=(255,255,0), font=font)
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
