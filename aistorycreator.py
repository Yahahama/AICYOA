from gpt4all import GPT4All
import json
from sys import platform
from time import sleep
import os

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

def delete_last_lines(n=1): 
    from sys import stdout
    CURSOR_UP_ONE = '\x1b[1A' 
    ERASE_LINE = '\x1b[2K' 
    for _ in range(n): 
        stdout.write(ERASE_LINE) 
        stdout.write(CURSOR_UP_ONE)

def printGreen(text, *args, **kwargs): print("\033[92m{}\033[00m".format(text), *args, **kwargs)

printGreen("Please wait, loading...")

if platform == "win32": modelPath = "C:/Users/rokso/AppData/Local/nomic.ai/GPT4All/"
elif platform == "darwin": modelPath = "/Users/abibolov27/Library/Application Support/nomic.ai/GPT4All/"
else: raise Exception("Unsupported OS: %s" % platform)

model = GPT4All("Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf", modelPath)

printGreen("Model loaded!")

storypath = os.path.join(os.path.dirname(__file__), "story.json")

storydata = {
    "storyNodes": []
}

printGreen("JSON loaded!")

printGreen("What would you like the initial scenario to be? (Leave blank for the default scenario):")
# initialStory = input()
initialStory = ""
if initialStory == "":
    initialStory = "You are in a dark room. You can't see anything."
    delete_last_lines(1)
    print(initialStory)

printGreen("How many choices deep do you want your game to be? (Note: each layer deeper will take 3x as long to generate.)")
# depth = int(input())
depth = 2

printGreen("Generating story. This may take a while.")

system_template = "A helpful generative AI that specializes in writing stories is chatting with a curious user who wants it to write some content l his choose-your-own-adventure game."

def createStory(id='', prevGenStories=[]):
    newNode = {}
    newNode.update({"id": id})
    currentDepth = len(id)
    if currentDepth >= depth: return
    if currentDepth == depth - 1:
        prompt_template = "USER: Hi, I've got a snippet of a CYOA game's story here: \"{0}\" I need you to write three choices to give the player at this point, each choice surrounded by quotation marks and separated by a whitespace. After all three are completed, write three corresponding story conclusions each surrounded by quotes and seperated by a whitespace.\nAI: "
    else:
        prompt_template = "USER: Hi, I've got a snippet of a CYOA game's story here: \"{0}\" I need you to write three choices to give the player at this point, each choice surrounded by quotation marks and separated by a whitespace. After all three are completed, write three corresponding story continuations each surrounded by quotes and seperated by a whitespace.\nAI: "
    with model.chat_session(system_template, prompt_template):
        if currentDepth == 0:
            newNode.update({"text": initialStory})
        else:
            newNode.update({"text": prevGenStories[-1][int(id[-1])]})
        if currentDepth < depth - 1:
            response = model.generate(initialStory, max_tokens=400, temp=.75)
            genChoices = extractQuote(response, 6)[:3]
            genStories = extractQuote(response, 6)[3:]
            prevGenStories.append(genStories)
            newNode.update({"choices": [
                {
                    "text": genChoices[0],
                    "nextNodeID": id + '0'
                },
                {
                    "text": genChoices[1],
                    "nextNodeID": id + '1'
                },
                {
                    "text": genChoices[2],
                    "nextNodeID": id + '2'
                }
            ]})
    storydata["storyNodes"].append(newNode)
    createStory(id + '0', genStories)
    createStory(id + '1', genStories)
    createStory(id + '2', genStories)

createStory()

printGreen("Story generated!")

with open(storypath, "w") as file:
    json.dump(storydata, file)

printGreen("Story saved!")