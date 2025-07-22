
import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
import os

st.set_page_config(layout="wide")
st.image('image.jpg')

col1, col2 = st.columns([3, 2])
with col1:
    user_input = st.text_input('Enter your text here:')
    run = st.checkbox('Run', value=True)
    voice = st.button('Voice')

with col2:
    st.title("Output")
    output_text_area = st.empty()

# Configure the API key for Google Generative AI
genai.configure(api_key="AIzaSyACd3jcYie92qktM_Gbc78O6ykgwJvPjNU")
model = genai.GenerativeModel('gemini-1.5-flash')

if run and user_input:
    # response = model.generate_content(["You are a compassionate and understanding guide, dedicated to helping individuals struggling with medical conditions and mental instability regain their motivation and step into a healthier, happier life. Your words should be gentle yet inspiring, offering hope, encouragement, and practical steps to help them find strength within themselves.Your response should be polite, suggestive, and highly motivational, focusing on positivity and empowerment. Remind them that every small step toward health is a victory, that they are stronger than they think, and that healing is a journey worth taking. Provide uplifting advice on self-care, mindset shifts, and small daily actions that can lead to improvement. Help them visualize a better future and encourage them to embrace the process of healing with confidence and hope.", user_input])
    #
    response = model.generate_content(["Provide response :", user_input])
    output_text = response.text
    output_text_area.subheader(output_text)

    if voice:
        try:
            st.info("Generating audio...")
            tts = gTTS(text=output_text, lang='en')
            audio_file = "output.mp3"
            tts.save(audio_file)

            # Display audio in Streamlit
            with open(audio_file, "rb") as f:
                audio_bytes = f.read()
            st.audio(audio_bytes, format='audio/mp3')

            # Provide download link
            b64 = base64.b64encode(audio_bytes).decode()
            href = f'<a href="data:audio/mp3;base64,{b64}" download="{audio_file}">Download Audio</a>'
            st.markdown(href, unsafe_allow_html=True)

            # Clean up the audio file
            os.remove(audio_file)

        except Exception as e:
            st.error(f"An error occurred while generating audio: {e}")

