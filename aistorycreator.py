from gpt4all import GPT4All
import json

model = GPT4All("Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf", "C:/Users/rokso/AppData/Local/nomic.ai/GPT4All/")
print("Model loaded!")

storypath = r"C:\Users\rokso\OneDrive\Documents\Code\AICYOA\story.json"

with open(storypath, "r") as file:
    storydata = json.load(file)

print("Story loaded!")

system_template = "An uncompleted choose-your-own-adventure interactive story that needs to be filled in with story. For each story node, create three choices for players to take, surrounded by apostrophes and seperated by commas, like so: 'CHOICE1','CHOICE2','CHOICE3'. Then, on a new line, create three new story nodes that correspond to the choices, surrounded by apostrophes and seperated by commas, like so: 'STORYNODE1','STORYNODE2','STORYNODE3'. Once you're finished writing these, stop generation immediately and do not write anything else. Keep all choices restricted to 100 characters and all story nodes restricted to 150 characters."
prompt_template = "{0}\n"

print(prompt_template.format(storydata["storyNodes"][0]["text"]))

with model.chat_session(system_template, prompt_template):
    response = model.generate(storydata["storyNodes"][0]["text"])
    print(response)