from gpt4all import GPT4All
import json
from sys import platform
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

with open(storypath, "r") as file:
    storydata = json.load(file)

printGreen("JSON loaded!")

printGreen("What would you like the initial scenario to be? (Leave blank for the default scenario):")
initialStory = input()
if initialStory == "":
    initialStory = "You are in a dark room. You can't see anything."
    delete_last_lines(1)
    print(initialStory)

printGreen("How many choices deep do you want your game to be? (Note: each layer deeper will take 3x as long to generate.)")
depth = int(input())

system_template = "A helpful generative AI that specializes in writing stories is chatting with a curious user who wants it to write some content l his choose-your-own-adventure game."
prompt_template = "USER: Hi, I've got a snippet of a CYOA game's story here: \"{0}\" I need you to write three choices to give the player at this point, each choice surrounded by quotation marks and separated by a whitespace. After all three are completed, write three corresponding story continuations each surrounded by quotes and seperated by a whitespace.\nAI: "

genChoices = []

def createStory(id=''):
    currentDepth = len(id)
    if currentDepth >= depth: return
    if currentDepth == depth - 1:
        prompt_template = "USER: Hi, I've got a snippet of a CYOA game's story here: \"{0}\" I need you to write three choices to give the player at this point, each choice surrounded by quotation marks and separated by a whitespace. After all three are completed, write three corresponding story conclusions each surrounded by quotes and seperated by a whitespace.\nAI: "
    with model.chat_session(system_template, prompt_template):
        response = model.generate(initialStory, max_tokens=400, temp=.75)
        prevGenChoices = genChoices
        genChoices = extractQuote(response, 6)[:3]
        genStories = extractQuote(response, 6)[3:]
    newNode = {}
    if currentDepth == 0:
        newNode.update({"text": initialStory})
    else:
        newNode.update({"text": prevGenChoices[id[-1]]})
    newNode.update({"choices": [
        {
            "text": genChoices[0],
            "nextNodeID": id + 0
        },
        {
            "text": genChoices[1],
            "nextNodeID": id + 1
        },
        {
            "text": genChoices[2],
            "nextNodeID": id + 2
        }
    ]})
    storydata.update(newNode)
    createStory(id + '0')
    createStory(id + '1')
    createStory(id + '2')

    with open(storypath, "w") as file:
        json.dump(storydata, file)