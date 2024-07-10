from gpt4all import GPT4All
import json

currentChoiceToFillOut = 0

model = GPT4All("Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf", "C:/Users/rokso/AppData/Local/nomic.ai/GPT4All/")
print("Model loaded!")

storypath = r"C:\Users\rokso\OneDrive\Documents\Code\AICYOA\story.json"

with open(storypath, "r") as file:
    storydata = json.load(file)

print("Story loaded!")

system_template = "An uncompleted choose-your-own-adventure interactive story that needs to be filled in with story when a colon is followed by nothing. For example, 'Choice 1: {fill in story after colon'"
prompt_template = "{0}\Choice " + str(currentChoiceToFillOut) + ": "

with model.chat_session(system_template, prompt_template):
    print(storydata["storyNodes"][0]["text"])
    response = model.generate(storydata["storyNodes"][0]["text"])
    print(response)