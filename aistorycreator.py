from gpt4all import GPT4All
import json

def extractQuote(text, n=1):
    quotes = []
    start = -1
    for i in range(n):
        for j in range(len(text)):
            if text[j] == "\"":
                if start == -1:
                    start = j
                else:
                    quotes.append(text[start:j+1])
                    text = text[:start] + text[j+1:]
                    start = -1
                    break
    return quotes

model = GPT4All("Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf", "C:/Users/rokso/AppData/Local/nomic.ai/GPT4All/")
print("Model loaded!")

storypath = r"C:\Users\rokso\OneDrive\Documents\Code\AICYOA\story.json"

with open(storypath, "r") as file:
    storydata = json.load(file)

print("Story loaded!")

system_template = "A helpful generative AI that specializes in writing stories is chatting with a curious user who wants it to write some content for his choose-your-own-adventure game."
prompt_template = "{0}\n"

print(prompt_template.format(storydata["storyNodes"][0]["text"]))

with model.chat_session(system_template, prompt_template):
    response = model.generate(storydata["storyNodes"][0]["text"])
    print(response)