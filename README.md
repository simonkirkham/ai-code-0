# Countdown Web App

This is a Python Flask web application that generates a beautiful countdown image to a user-selected date, time, and occasion. The app features:

- A modern web interface for entering an occasion, date, and time.
- AI-generated background images for the countdown using Hugging Face's Stable Diffusion XL (SDXL) model.
- The ability to download or share the generated countdown image.

## Features
- **Web Form:** Enter an occasion, date, and time to generate a countdown.
- **AI Backgrounds:** Uses Hugging Face's SDXL model to create a unique background for each occasion (requires a free Hugging Face API key).
- **.env Support:** Secrets like API keys are loaded from a `.env` file for security and convenience.

## Setup
1. **Clone the repository:**
   ```
   git clone https://github.com/simonkirkham/ai-code-0.git
   cd ai-code-0
   ```
2. **Create and activate a virtual environment:**
   ```
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```
3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
4. **Set up your Hugging Face API key:**
   - Create a free account at [Hugging Face](https://huggingface.co/).
   - Get your API key from [your settings](https://huggingface.co/settings/tokens).
   - Copy `.env` if it doesn't exist and add your key:
     ```
     HUGGINGFACE_API_KEY=your_hf_key_here
     ```

## Running the App
1. Make sure your `.env` file is set up with your API key.
2. Start the app:
   ```
   python src/webapp.py
   ```
3. Open your browser and go to [http://localhost:5000](http://localhost:5000)

## Security
- **Never commit your `.env` file** with real secrets to version control. `.env` is in `.gitignore` by default.
- API keys are loaded at runtime using `python-dotenv`.

## Project Structure
```
├── src/
│   ├── webapp.py         # Main Flask app
│   ├── countdown.py      # Countdown logic
│   ├── templates/
│   │   └── index.html    # Web UI
│   └── static/
│       └── style.css     # CSS
├── tests/                # Unit tests
├── .env                  # Your secrets (not committed)
├── requirements.txt      # Python dependencies
├── README.md
```

## License
This project is for educational/demo purposes. For production use, review the licenses of all dependencies and AI models.
