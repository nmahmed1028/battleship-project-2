import pyttsx3
import re

WORDS_PER_MINUTE_RATE = 130

VOICE_ENGINE = None
ENGINE_VOICES = None
VOICE_IDS = None

async def init_voice_engine():
    global VOICE_ENGINE, ENGINE_VOICES, VOICE_IDS
    VOICE_ENGINE = pyttsx3.init()
    ENGINE_VOICES = VOICE_ENGINE.getProperty("voices")
    VOICE_IDS = []
    for voice in ENGINE_VOICES:
        if re.match(".*[.]en-.*", str(voice.id)) or re.match(".*synthesis[.]voice.*", str(voice.id)):
            VOICE_IDS.append(voice.id)
    print("Voice engine initialized")

def text_to_speech(text: str, voice_id: str = "com.apple.speech.synthesis.voice.Albert") -> None:
    VOICE_ENGINE.setProperty("rate", WORDS_PER_MINUTE_RATE)
    VOICE_ENGINE.setProperty("voice", voice_id)

    VOICE_ENGINE.say(text)
    VOICE_ENGINE.runAndWait()
