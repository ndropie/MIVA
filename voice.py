import wave
import winsound
import os

import sounddevice as sd
from faster_whisper import WhisperModel
from piper import PiperVoice
import ollama


# ==============================
# LOAD MODELS
# ==============================

# Load Whisper
whisper_model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

# Load Piper voice
piper_voice = PiperVoice.load(
    "en_US-lessac-medium.onnx"
)


# ==============================
# LISTEN
# ==============================

def listen():

    print("\nMIVA is listening...")

    # Record 5 seconds
    audio = sd.rec(
        int(5 * 16000),
        samplerate=16000,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    print("Processing...")

    # Convert audio into 1D array
    audio = audio.flatten()

    # Speech → text
    segments, info = whisper_model.transcribe(audio)

    text = ""

    for segment in segments:
        text += segment.text

    return text.strip()

# ==============================
# ASK QWEN
# ==============================

def ask_miva(user_input):

    try:

        response = ollama.chat(
            model="qwen3:4b-instruct",
            messages=[
                {
                    "role": "system",
                    "content": """
You are MIVA, a local AI personal assistant running on the user's computer.

Your name is MIVA.

Do not introduce yourself as Qwen unless the user specifically asks which underlying AI model you use.

Answer naturally and conversationally.
Keep responses reasonably short because your responses are spoken aloud using text-to-speech.
"""
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        return response["message"]["content"]

    except Exception as error:

        print("Ollama Error:", error)

        return "Sorry, I couldn't process that right now."
# ==============================
# SPEAK
# ==============================

def remove_emojis(text):

    # Keep normal English characters
    # Remove emojis and other unsupported characters
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

        # Remove emojis before sending text to Piper
        text = remove_emojis(text)

        # Temporary audio file
        filename = "miva_response.wav"

        # Text → WAV
        with wave.open(filename, "wb") as wav_file:

            piper_voice.synthesize_wav(
                text,
                wav_file
            )

        # Play WAV
        winsound.PlaySound(
            filename,
            winsound.SND_FILENAME
        )

        # Delete temporary file
        os.remove(filename)

    except Exception as error:

        print("Audio Error:", error)
# ==============================
# MIVA LOOP
# ==============================

while True:

    # Listen
    user_input = listen()

    # If nothing was heard, listen again
    if not user_input:

        print("MIVA: I didn't hear anything.")

        continue

    print("You:", user_input)

    # Stop MIVA
    if user_input.lower() == "bye":

        print("MIVA: Goodbye!")

        speak("Goodbye Ahmed!")

        break

    # Ask Qwen
    response = ask_miva(user_input)

    print("MIVA:", response)

    # Speak response
    speak(response)