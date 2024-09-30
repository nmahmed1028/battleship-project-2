import pyttsx3 # imports text to speech
import re # imports regular expression

WORDS_PER_MINUTE_RATE = 130 #sets rate of speech, 130 words per minute

VOICE_ENGINE = None # initializes voice engine
ENGINE_VOICES = None # initializes available voice varaibles 
VOICE_IDS = None # initialzes voice ID variables 

# asynchronous function to initialize the voice engine/set up available voices
async def init_voice_engine(): # defines async function 
    global VOICE_ENGINE, ENGINE_VOICES, VOICE_IDS # uses global variables to store engine and voice data
    VOICE_ENGINE = pyttsx3.init() # initialize the pyttsx3 voice engine
    ENGINE_VOICES = VOICE_ENGINE.getProperty("voices") # retrieve available voices from engine
    VOICE_IDS = [] # initialize empty list to store filtered voice ids
    for voice in ENGINE_VOICES: # loop through all available voices
        if re.match(".*[.]en-.*", str(voice.id)) or re.match(".*synthesis[.]voice.*", str(voice.id)): # use regex to match voice ids containing .en- or .synthesis.voice
            VOICE_IDS.append(voice.id) # add matching voice ids to list
    print("Voice engine initialized") # print confirmation message

# fucntion to convert text to speech using a specified voice
def text_to_speech(text: str, voice_id: str = "com.apple.speech.synthesis.voice.Albert", wpm: int = WORDS_PER_MINUTE_RATE) -> None: # defines text to speeach functions
    VOICE_ENGINE.setProperty("rate", wpm) # set speech rate to defined words per minute
    VOICE_ENGINE.setProperty("voice", voice_id) # set the voice engine to use the specified voice id

    VOICE_ENGINE.say(text) # queue text for speech output
    VOICE_ENGINE.runAndWait() # process speech output, wait until finished
