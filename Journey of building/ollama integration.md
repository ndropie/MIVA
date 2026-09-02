by finding and searching a offline AI got to know about ollama Qwen AIs there have a huge number of parameters but right now i need a ai which don't think so much and smart enough to understand the input and give appropriate outputs so i think qwen3 4b will be a good choice. but i think a latency gonna be a big concern 

UPDATE !! 
 got to know a version of **Qwen3:4b-instruct** it does follow user instruction 
 so I think I gonna use it . for now if something bad happened i can switch the models


I have installed qwen3:4b but it taking too much time to think as expected.

that's too much for me . 
```
   def generate(self, user_input):
        response = ollama.chat(
            model= "qwen3:4b", # specifying the model
            messages = [
                    {
                    "role": "user",
                    "content" : user_input
                    }],
            think = False
        )
        print(response)
        return  response["message"]["content"]
```

Qwen was thinking to much to search and found out that i can do think = False but it did not worked
butb then o printed the response 
the output was :- 

```
model='qwen3:4b' created_at='2026-09-02T09:09:29.8860488Z' done=True done_reason='stop' total_duration=12275654600 load_duration=1093100 prompt_eval_count=11 prompt_eval_duration=5279665000 eval_count=331 eval_duration=6950487000 message=Message(role='assistant', content='Okay, the user said "hi". I need to respond appropriately. Let me think.\n\nFirst, I should greet them back. Since they used "hi", maybe I can say something friendly and open. Let me check the previous messages to see if there\'s any context, but in this case, it\'s the first message. So I should just respond with a simple greeting.\n\nWait, the user might be testing if I\'m working. So I should be friendly and helpful. Let me make sure the response is not too long. Maybe say "Hello! How can I assist you today?" That\'s a standard greeting. But the user said "hi", so maybe "Hi there! 👋 How can I help you today?" That\'s a bit more friendly with an emoji.\n\nWait, the user might be in a different language, but they used "hi", which is English. So I can stick to English. Let me avoid any markdown. Just plain text.\n\nAlso, make sure it\'s not too formal. Since it\'s a greeting, keep it casual. Maybe add a smiley to be friendly. Let me go with "Hi there! 👋 How can I help you today?" That\'s good.\n\nWait, the user might want a more concise response. Let me check examples. Sometimes people just say "Hi" and expect a short reply. But in this case, the assistant should be helpful. So the response should be friendly and open for the user to ask anything.\n\nYes, I think that\'s a good response. Let me write it out.\n</think>\n\nHi there! 👋 How can I help you today?', thinking=None, images=None, tool_name=None, tool_calls=None) logprobs=None
```

that's too much to handle 

i think i gonna use chatgpt for this one

chat gpt is stupid hahah i told him to use qwen3:4b-instruct but he still used 4b resulting in latency 


# next step 
now as a latency problem is fixed with instruct version i can focus on building the proper chat history .

for which i just have to create a list and store responses into that so MIVA can remember what we are talking about 