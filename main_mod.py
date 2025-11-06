# main_mod.py - web-side logic adapter (safe/resilient)
import os
import random
from datetime import datetime
from decouple import config
from conv import random_text
from online import find_my_ip, search_on_wikipedia, search_on_google, youtube, send_email, get_news, weather_forecast
from gtts import gTTS
import io

USER = os.getenv('USER', config('USER', default='User'))
HOSTNAME = os.getenv('BOT', config('BOT', default='Pluto'))


def greet_me_text():
    hour = datetime.now().hour
    if 6 <= hour < 12:
        greeting = f"Good morning {USER}"
    elif 12 <= hour <= 16:
        greeting = f"Good afternoon {USER}"
    else:
        greeting = f"Good evening {USER}"
    return f"{greeting}. I am {HOSTNAME}. How may I assist you?"


def speak_audio_bytes(text: str) -> bytes:
    """Return mp3 bytes for given text using gTTS."""
    try:
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception as e:
        print("TTS error:", e)
        return b""


def handle_query(query: str) -> str:
    q = query.lower().strip()

    # IP
    if 'ip' in q or 'ip address' in q:
        ip = find_my_ip()
        return f'Your public IP address is {ip}.'

    # YouTube
    if q.startswith('youtube:'):
        video = q.split(':', 1)[1].strip()
        youtube(video)
        return f'Requested YouTube: {video}. (Server-side open may not start playback)'

    # Google / search
    if q.startswith('google:') or q.startswith('search:'):
        term = q.split(':', 1)[1].strip()
        search_on_google(term)
        return f'Search initiated for: {term}.'

    # Wikipedia
    if q.startswith('wikipedia:') or q.startswith('wiki:'):
        term = q.split(':', 1)[1].strip()
        res = search_on_wikipedia(term)
        return f'According to Wikipedia: {res}'

    # News
    if 'news' in q:
        headlines = get_news()
        return '\n'.join(headlines)

    # Weather
    if q.startswith('weather:'):
        city = q.split(':', 1)[1].strip()
        weather, temp, feels_like = weather_forecast(city)
        if weather in ("No API key", "error"):
            return f"Weather unavailable: {weather}"
        return f'Weather in {city}: {weather}. Temp: {temp}. Feels like: {feels_like}.'

    # Small talk
    if 'how are you' in q:
        return "I'm absolutely fine. How can I help?"

    # fallback
    return random.choice(random_text)
