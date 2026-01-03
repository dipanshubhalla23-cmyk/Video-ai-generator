import streamlit as st
import os
import requests
from openai import OpenAI

# Page Setup
st.set_page_config(page_title="AI Video Maker", page_icon="🎬")

st.title("🎬 Faceless Video Assistant")
st.write("Generate viral scripts and realistic AI voiceovers instantly.")

# Sidebar for Keys
st.sidebar.header("🔑 Settings")
openai_key = st.sidebar.text_input("OpenAI API Key", type="password")
elevenlabs_key = st.sidebar.text_input("ElevenLabs API Key", type="password")
voice_id = st.sidebar.text_input("Voice ID", value="21m00Tcm4TlvDq8ikWAM")

# Main Inputs
topic = st.text_input("Video Topic", "Facts about deep ocean mysteries")

# Functions
def generate_script(topic, key):
    client = OpenAI(api_key=key)
    prompt = f"Write a 30-second viral TikTok script about {topic}. No visual cues, just spoken words. Tone: Intense, engaging."
    try:
        response = client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"OpenAI Error: {e}")
        return None

def generate_audio(text, key, vid):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{vid}"
    headers = {"xi-api-key": key, "Content-Type": "application/json"}
    data = {"text": text, "model_id": "eleven_monolingual_v1"}
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.content
        else:
            st.error(f"ElevenLabs Error: {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

# The Button
if st.button("🚀 Generate Assets"):
    if not openai_key or not elevenlabs_key:
        st.warning("⚠️ Please enter your API keys in the sidebar first!")
    else:
        # 1. Make Script
        with st.spinner("Writing script..."):
            script = generate_script(topic, openai_key)
        
        if script:
            st.success("Script Generated!")
            st.text_area("Copy this script:", script, height=150)
            
            # 2. Make Audio
            with st.spinner("Generating voiceover..."):
                audio_data = generate_audio(script, elevenlabs_key, voice_id)
            
            if audio_data:
                st.audio(audio_data, format="audio/mp3")
                st.download_button(label="Download Voiceover MP3", data=audio_data, file_name="voiceover.mp3", mime="audio/mpeg")
                st.success("✅ Done! Download your audio above.")
