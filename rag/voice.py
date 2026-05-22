from gtts import gTTS
import os

def speak(text: str):
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save("/tmp/response.mp3")
        os.system("mpg123 -q /tmp/response.mp3")
    except Exception as e:
        print(f"Voice unavailable: {e}")