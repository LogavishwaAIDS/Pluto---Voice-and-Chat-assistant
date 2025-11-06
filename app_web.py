# app_web.py (updated) - run with `streamlit run app_web.py`
import streamlit as st
from main_mod import greet_me_text, handle_query, speak_audio_bytes
from online import get_news, weather_forecast

st.set_page_config(page_title="Pluto - Voice Assistant", page_icon="🎙️")
st.title("🎙️ Pluto — Virtual Voice Assistant (Web)")

if st.button("Greet me"):
    greeting = greet_me_text()
    st.info(greeting)
    audio_bytes = speak_audio_bytes(greeting)
    if audio_bytes:
        st.audio(audio_bytes, format='audio/mp3')

col1, col2 = st.columns(2)
with col1:
    if st.button("News"):
        try:
            headlines = get_news()
            for h in headlines:
                st.write("- ", h)
        except Exception as e:
            st.error(f"News fetch error: {e}")

with col2:
    city = st.text_input("City (for weather):")
    if st.button("Get Weather"):
        try:
            weather, temp, feels_like = weather_forecast(city)
            if weather in ("No API key", "error"):
                st.warning(f"Weather not available: {weather}")
            else:
                s = f"Weather in {city}: {weather}. Temp: {temp}. Feels like: {feels_like}."
                st.write(s)
                audio = speak_audio_bytes(s)
                if audio:
                    st.audio(audio, format='audio/mp3')
        except Exception as e:
            st.error(f"Weather fetch error: {e}")

query = st.text_input("Ask Pluto (prefix with 'wikipedia:', 'youtube:', 'weather:', 'google:', or type 'news'):")
if st.button("Ask") and query:
    try:
        response = handle_query(query)
        st.write(response)
        audio = speak_audio_bytes(response)
        if audio:
            st.audio(audio, format='audio/mp3')
    except Exception as e:
        st.error(f"Assistant error: {e}")
