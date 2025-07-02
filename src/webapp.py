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
</head>
<body>
    <h1>Countdown Image Generator</h1>
    <form method="post">
        <label for="occasion">Occasion:</label>
        <input type="text" id="occasion" name="occasion" required><br><br>
        <label for="date">Date:</label>
        <input type="date" id="date" name="date" required><br><br>
        <label for="time">Time:</label>
        <input type="time" id="time" name="time" required><br><br>
        <input type="submit" value="Create Countdown Image">
    </form>
    {% if image_url %}
        <h2>Countdown to {{ occasion }}</h2>
        <img src="{{ image_url }}" alt="Countdown Image">
    {% endif %}
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
