
in the phase 0.1 MIVA 0.1 
I will just create chatbot with oops structure so i can gradually make it scalable eventually she gonna have a lot of features 

first i have created a class called start which contains a function to of conversation where i will put all the steps of replaying 

as 
`  
``` 
def conversation(self): # handels complete converstion logic

        exit_commands = {

            "bye miva",

            "bye bye",

            "tata",

            "see you",

        }

        while True:

            user_input = input('User: ').strip().lower()

  

            if user_input in exit_commands:

                print("MIVA: Good Bye Sir")

                break

  
            print(f'MIVA: you said {user_input}')
```
            
right now the logic is 
```
start()
 ├── print
 └── conversation()
       ├── input
       ├── exit handling
       └── response
```
, as MIVA becomes a real personal assistant, I’d expect the architecture to evolve toward something like:

```
main.py
   │
   ▼
MIVA.start()
   │
   ▼
MIVA.run()
   │
   ├── Listen
   │     └── Speech → Text
   │
   ├── Understand
   │     └── Qwen / AI Model
   │
   ├── Decide
   │     ├── Conversation?
   │     └── Action?
   │
   ├── Execute
   │     └── Tools / PC Control
   │
   ├── Respond
   │     └── Text
   │
   └── Speak
         └── Text → Speech
```

With the project eventually becoming something closer to:

```
MIVA/
│
├── main.py
│
├── app/
│   │
│   ├── core/
│   │   └── miva.py
│   │
│   ├── ai/
│   │   └── model.py
│   │
│   ├── voice/
│   │   ├── listener.py
│   │   └── speaker.py
│   │
│   ├── tools/
│   │   ├── system.py
│   │   ├── files.py
│   │   ├── browser.py
│   │   └── applications.py
│   │
│   └── memory/
│       └── memory.py
│
└── tests/
```
created a model.py in ai/
which will handle I/O

next step is [[ollama integration ]] 