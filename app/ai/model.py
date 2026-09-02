import ollama

class Model:

    def __init__(self):
        self.messages = []

    def generate(self, user_input):
        self.messages.append({
            "role": "user",
            "content" : user_input
        })

        response = ollama.chat(
            model= "qwen3:4b-instruct", # specifying the model 
            messages=self.messages,
            think=False
        )

        asssitant_response = response["message"]["content"]

        self.messages.append({
            "role": "assistant",
            "content" : asssitant_response
        })

        return asssitant_response