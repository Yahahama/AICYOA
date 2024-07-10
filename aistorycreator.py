from gpt4all import GPT4All
import json

currentChoiceToFillOut = 0

model = GPT4All("Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf", "C:/Users/rokso/AppData/Local/nomic.ai/GPT4All/")
print("Model loaded!")

storypath = r"C:\Users\rokso\OneDrive\Documents\Code\AICYOA\story.json"

with open(storypath, "r") as file:
    storydata = json.load(file)

print("Story loaded!")

system_template = "An uncompleted choose-your-own-adventure interactive story that needs to be filled in with story. Fill in only the first empty choice. For example, if Choice 0 and Choice 1 are empty, fill in only Choice 0."
prompt_template = "{0}\nChoice " + str(currentChoiceToFillOut) + ": "

print(prompt_template.format(storydata["storyNodes"][0]["text"]))

with model.chat_session(system_template, prompt_template):
    response = model.generate(storydata["storyNodes"][0]["text"])
    print(response)