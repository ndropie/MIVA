import ollama
import json

from pc_control.applications import open_application


# ==============================
# ASK QWEN
# ==============================

def ask_brain(user_input):

    response = ollama.chat(
        model="qwen3:4b-instruct",
        messages=[
            {
                "role": "system",
                "content": """
You are MIVA, a local AI personal assistant.

Your job is to understand what the user wants.

If the user wants to open an application,
return ONLY JSON:

{
    "action": "open_application",
    "application": "application name"
}

If the user is having normal conversation,
return ONLY JSON:

{
    "action": "chat",
    "response": "your answer"
}

Do not write anything outside the JSON.
"""
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    return response["message"]["content"]


# ==============================
# PROCESS USER REQUEST
# ==============================

def process_command(user_input):

    response = ask_brain(user_input)

    print("\nQwen:")
    print(response)

    # ==============================
    # CONVERT JSON TEXT TO PYTHON
    # ==============================

    try:

        command = json.loads(response)

    except json.JSONDecodeError:

        print("MIVA: Invalid response from Qwen.")

        return "I couldn't understand that command."

    # ==============================
    # OPEN APPLICATION
    # ==============================

    if command["action"] == "open_application":

        application = command["application"]

        result = open_application(
            application
        )

        return result

    # ==============================
    # NORMAL CHAT
    # ==============================

    elif command["action"] == "chat":

        return command["response"]

    # ==============================
    # UNKNOWN ACTION
    # ==============================

    return "I don't understand that action."