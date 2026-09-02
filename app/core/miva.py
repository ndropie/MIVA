from app.ai.model import Model

class MIVA:

    def start(self):
        print("MIVA is online!!")
        self.conversation()

# handels complete converstion logic
    def conversation(self): 
        exit_commands = {
            "bye miva",
            "bye bye",
            "tata",
            "bye",
            "see you",
        }

        model = Model()
        while True:
            user_input = input('User: ').strip().lower()

            if user_input in exit_commands:
                print("MIVA: Good Bye Sir")
                break
            else:
                response = model.generate(user_input)
                print(f"MIVA: {response}")                
            