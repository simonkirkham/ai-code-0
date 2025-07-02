import os
import requests
from flask import Flask, request, render_template, send_file
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from countdown import get_countdown_string
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_KEY = os.environ["HUGGINGFACE_API_KEY"]
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

def generate_hf_background(prompt):
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {"inputs": prompt}
    response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=data)
    response.raise_for_status()
    return Image.open(BytesIO(response.content)).convert("RGBA")

app = Flask(__name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "static"))

@app.route('/', methods=['GET', 'POST'])
def index():
    image_url = None
    occasion = None
    if request.method == 'POST':
        occasion = request.form['occasion']
        date_str = request.form['date']
        time_str = request.form['time']
        target_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        image_url = f"/countdown_image?date={date_str}&time={time_str}&occasion={occasion}"
    return render_template('index.html', image_url=image_url, occasion=occasion)

@app.route('/countdown_image')
def countdown_image():
    date_str = request.args.get('date')
    time_str = request.args.get('time')
    occasion = request.args.get('occasion', '')
    target_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    countdown = get_countdown_string(target_dt)
    # Generate Hugging Face background
    try:
        bg_img = generate_hf_background(f"background for {occasion}").resize((500, 200))
    except Exception as e:
        print(f"Hugging Face background generation failed: {e}")
        bg_img = Image.new('RGBA', (500, 200), color=(73, 109, 137, 255))
    img = Image.new('RGBA', (500, 200))
    img.paste(bg_img, (0, 0))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except Exception:
        font = ImageFont.load_default()
    draw.text((10, 40), f"Countdown to {occasion}", fill=(255,255,255,255), font=font)
    draw.text((10, 100), countdown, fill=(255,255,0,255), font=font)
    buf = BytesIO()
    img.convert('RGB').save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
