# online.py - headless version (for Streamlit Cloud)
import os
import requests
import wikipedia
from email.message import EmailMessage
import smtplib
import xml.etree.ElementTree as ET
import webbrowser  # safe alternative to pywhatkit

NEWSAPI_KEY = os.getenv('NEWSAPI_KEY', '')
OPENWEATHER_KEY = os.getenv('OPENWEATHER_KEY', '')
EMAIL = os.getenv('PLUTO_EMAIL', '')
PASSWORD = os.getenv('PLUTO_EMAIL_PASSWORD', '')


def find_my_ip():
    try:
        ip_address = requests.get('https://api64.ipify.org?format=json', timeout=6).json()
        return ip_address.get('ip')
    except Exception:
        return "Unavailable"


def search_on_wikipedia(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except Exception as e:
        return f"Wikipedia fetch error: {e}"


def search_on_google(query):
    """Return top few text results instead of opening browser."""
    try:
        url = f"https://duckduckgo.com/html/?q={query}"
        r = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        results = []
        for link in soup.select(".result__a")[:5]:
            title = link.get_text()
            href = link.get("href")
            results.append(f"{title} — {href}")
        return results if results else ["No results found."]
    except Exception as e:
        print("search_on_google error:", e)
        return ["Search unavailable."]



def youtube(video):
    try:
        webbrowser.open(f"https://www.youtube.com/results?search_query={video}")
        return f"Opened YouTube search for {video}"
    except Exception as e:
        return f"Could not open YouTube: {e}"


def send_email(receiver_add, subject, message):
    if not EMAIL or not PASSWORD:
        return False
    try:
        email = EmailMessage()
        email['To'] = receiver_add
        email['Subject'] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print("send_email error:", e)
        return False


def get_news():
    try:
        if NEWSAPI_KEY:
            result = requests.get(
                f"https://newsapi.org/v2/top-headlines?country=in&category=general&apiKey={NEWSAPI_KEY}",
                timeout=8
            ).json()
            articles = result.get("articles", [])
            return [a.get("title", "").strip() for a in articles[:6] if a.get("title")]
        else:
            rss = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
            r = requests.get(rss, timeout=8)
            root = ET.fromstring(r.content)
            items = root.findall('.//item')[:6]
            return [i.find('title').text for i in items if i.find('title') is not None]
    except Exception as e:
        print("get_news error:", e)
        return ["News unavailable right now."]


def weather_forecast(city):
    try:
        if not OPENWEATHER_KEY:
            return ("No API key", "N/A", "N/A")
        res = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric",
            timeout=8
        ).json()
        if res.get("cod") != 200:
            return (res.get("message", "error"), "N/A", "N/A")
        weather = res["weather"][0]["main"]
        temp = res["main"]["temp"]
        feels_like = res["main"]["feels_like"]
        return weather, f"{temp}°C", f"{feels_like}°C"
    except Exception as e:
        print("weather_forecast error:", e)
        return ("error", "N/A", "N/A")

