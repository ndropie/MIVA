import wave
import winsound
import os
import time

import sounddevice as sd
from faster_whisper import WhisperModel
from piper import PiperVoice

from brain import process_command


# ==============================
# SETTINGS
# ==============================

SAMPLE_RATE = 16000

# Time MIVA waits for the first command
COMMAND_TIMEOUT = 10

# Length of each microphone recording
RECORD_SECONDS = 3


# ==============================
# LOAD MODELS
# ==============================

print("Loading Whisper...")

whisper_model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

print("Loading Piper...")

piper_voice = PiperVoice.load(
    "voices/en_US-lessac-medium.onnx"
)

print("MIVA is ready.")


# ==============================
# RECORD AUDIO
# ==============================

def record_audio(seconds):

    audio = sd.rec(
        int(seconds * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    return audio.flatten()


# ==============================
# SPEECH TO TEXT
# ==============================

def speech_to_text(audio):

    segments, info = whisper_model.transcribe(
        audio
    )

    text = ""

    for segment in segments:

        text += segment.text

    return text.strip()


# ==============================
# WAIT FOR WAKE WORD
# ==============================

def wait_for_wake_word():

    print("\n💤 MIVA is sleeping...")
    print("Say 'MIVA' to wake me.")

    while True:

        audio = record_audio(
            RECORD_SECONDS
        )

        text = speech_to_text(
            audio
        )

        print(
            "Heard:",
            text
        )

        text = text.lower()

        wakewords = [
    # MIVA

    'hey',
    'yo',
    'listen',
    'sunna ',
                    

    "miva",
    "miwa",
    "meva",
    "meewa",
    "mewa",
    "mivaah",
    "miva a",
    "mivae",

    # Hey MIVA
    "hey miva",
    "hey miwa",
    "hey meva",
    "hey meewa",
    "hey mewa",
    "hey mivaah",
    "hey miva a",

    # Hi MIVA
    "hi miva",
    "hi miwa",
    "hi meva",
    "hi meewa",
    "hi mewa",

    # Hello MIVA
    "hello miva",
    "hello miwa",
    "hello meva",
    "hello meewa",
    "hello mewa",

    # OK MIVA
    "ok miva",
    "okay miva",
    "ok miwa",
    "okay miwa",
    "ok meva",
    "okay meva",

    # Wake commands
    "wake up miva",
    "wake up miwa",
    "wake up meva",
    "wake up miva please",
    "wake up miwa please",

    # Listen commands
    "listen",
    "listen miva",
    "listen miwa",
    "listen meva",
    "listen to me",
    "miva listen",
    "miwa listen",

    # Other common Whisper variations
    "miva please",
    "miwa please",
    "meva please",
    "miva ji",
    "miwa ji",
    "hey miva please",
    "hello miva please"
]

        if any(wakeword in text for wakeword in wakewords):

            print("\nMIVA: I'm awake.")

            return True


# ==============================
# LISTEN FOR COMMAND
# ==============================

def listen_for_command():

    print("\nMIVA is listening...")

    start_time = time.time()

    while True:

        # ==============================
        # CHECK 10 SECOND TIMEOUT
        # ==============================

        if time.time() - start_time >= COMMAND_TIMEOUT:

            print(
                "\nMIVA: No response. Going to sleep."
            )

            return None


        # ==============================
        # RECORD SHORT AUDIO
        # ==============================

        audio = record_audio(
            RECORD_SECONDS
        )


        # ==============================
        # CONVERT TO TEXT
        # ==============================

        print("Processing...")

        text = speech_to_text(
            audio
        )


        # ==============================
        # IF NOTHING HEARD
        # ==============================

        if not text:

            print(
                "No speech detected."
            )

            continue


        # ==============================
        # SPEECH FOUND
        # ==============================

        print(
            "You:",
            text
        )

        return text


# ==============================
# REMOVE EMOJIS
# ==============================

def remove_emojis(text):

    text = text.encode(
        "ascii",
        "ignore"
    ).decode()

    return text


# ==============================
# SPEAK
# ==============================

def speak(text):

    try:

        text = remove_emojis(
            text
        )

        filename = "miva_response.wav"

        with wave.open(
            filename,
            "wb"
        ) as wav_file:

            piper_voice.synthesize_wav(
                text,
                wav_file
            )

        winsound.PlaySound(
            filename,
            winsound.SND_FILENAME
        )

        os.remove(
            filename
        )

    except Exception as error:

        print(
            "Audio Error:",
            error
        )


# ==============================
# MIVA MAIN LOOP
# ==============================

while True:

    # ==============================
    # SLEEP MODE
    # ==============================

    wait_for_wake_word()


    # ==============================
    # AWAKE MODE
    # ==============================

    while True:

        user_input = listen_for_command()


        # ==============================
        # 10 SECOND TIMEOUT
        # ==============================

        if user_input is None:

            break


        # ==============================
        # STOP MIVA
        # ==============================

        if user_input.lower() == "bye":

            print(
                "MIVA: Goodbye!"
            )

            speak(
                "Goodbye Ahmed!"
            )

            exit()


        # ==============================
        # SEND COMMAND TO BRAIN
        # ==============================

        response = process_command(
            user_input
        )


        # ==============================
        # SHOW RESPONSE
        # ==============================

        print(
            "MIVA:",
            response
        )


        # ==============================
        # SPEAK RESPONSE
        # ==============================

        speak(
            response
        )


        # ==============================
        # STAY AWAKE
        # ==============================

        print(
            "\nMIVA is still awake."
        )