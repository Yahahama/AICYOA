from gpt4all import GPT4All
from random import randint
import json
from sys import platform
import os

def extractQuote(text, n=1):
    quotes = []
    for _ in range(n):
        start = -1
        for j in range(len(text)):
            if text[j] == "\"":
                if start == -1:
                    start = j
                else:
                    quotes.append(text[start+1:j])
                    # Remove quoted string, account for possible error when start's value is 0
                    text = (text[:start-1] + text[j:] if start != 0 else text[j:])
                    start = -2
                    break
        # If start is -2, quote found and popped.
        if start == -2: continue
        quotes.append("")
    return quotes

def delete_last_lines(n=1): 
    from sys import stdout
    CURSOR_UP_ONE = '\x1b[1A' 
    ERASE_LINE = '\x1b[2K' 
    for _ in range(n): 
        stdout.write(ERASE_LINE) 
        stdout.write(CURSOR_UP_ONE)

def printGreen(text, *args, **kwargs): print("\033[92m{}\033[00m".format(text), *args, **kwargs)
def printRed(text, *args, **kwargs): print("\033[91m{}\033[00m".format(text), *args, **kwargs)

printGreen("Please wait, loading...")

# Hardcoded paths for myself
if platform == "win32": modelPath = "C:/Users/rokso/AppData/Local/nomic.ai/GPT4All/"
elif platform == "darwin": modelPath = "/Users/abibolov27/Library/Application Support/nomic.ai/GPT4All/"
else: raise Exception("Unsupported OS: %s" % platform)

model = GPT4All("Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf", modelPath)
printGreen("Model loaded!")

storypath = os.path.join(os.path.dirname(__file__), "story.json")
printGreen("JSON found!")
storydata = []

printGreen("What would you like the title of your story to be? (Leave blank for the default title):")
title = input()
if title == "": title = "Untitled Story"
printGreen("What would you like the initial scenario of your story to be? (Leave blank for the default scenario):")
currentStory = input()
if currentStory == "": currentStory = "You are in a dark room. You can't see anything."
printGreen("How many choices deep do you want your game to be? (Note: each layer deeper will take 3x as long to generate.)")
try: finalDepth = int(input())
except ValueError: finalDepth = None
while isinstance(finalDepth, int) == False or finalDepth < 1:
    printRed("Please enter a valid integer greater than 0.")
    try: finalDepth = int(input())
    except ValueError: pass
printGreen("Generating story. This may take a while.")

system_template = "A helpful generative AI that specializes in writing stories is chatting with a curious user who wants it to write some content l his choose-your-own-adventure game."

def createStory(id='', prevGenStories=[]):
    global currentStory
    currentDepth = len(id)
    # Base case of recursive function
    if currentDepth > finalDepth: return
    if currentDepth > 0: currentStory = prevGenStories[-1][int(id[-1])]
    newNode = {}
    newNode.update({"id": id})
    # Each layer uses the story generated by the previous layer
    newNode.update({"text": currentStory})
    # Don't generate additional choices and stories at the final layer, just use a previous story
    if currentDepth != finalDepth:
        # If we're at second-to-last depth, prompt attempts to generate conclusions rather than continuations
        if currentDepth == finalDepth - 1:
            prompt_template = "USER: Hi, I've got a snippet of a CYOA game's story here: \"{0}\" I need you to write three choices to give the player at this point, each choice surrounded by quotation marks and separated by a whitespace. After all three are completed, write three corresponding story conclusions each surrounded by quotes and seperated by a whitespace. Use this form, making sure to fill in the quotation marks with real content: CHOICES: \"\" \"\" \"\" STORIES: \"\" \"\" \"\"\nAI: "
        else:
            prompt_template = "USER: Hi, I've got a snippet of a CYOA game's story here: \"{0}\" I need you to write three choices to give the player at this point, each choice surrounded by quotation marks and separated by a whitespace. After all three are completed, write three corresponding story continuations each surrounded by quotes and seperated by a whitespace. Use this form, making sure to fill in the quotation marks with real content: CHOICES: \"\" \"\" \"\" CONCLUSIONS: \"\" \"\" \"\"\nAI: "
        printGreen("Generating node with ID \"%s\"" % id)
        with model.chat_session(system_template, prompt_template):
            genChoices = []
            genStories = []
            # First six quotations from AI response consist of 3 generated stories and 3 generated choices
            response = model.generate(currentStory, max_tokens=800, temp=.75)
            print(response)
            for i in range(len(response)):
                try:
                    # Removes possible AI-generated double quotes before extractQuote can be affected
                    if response[i:i+2] == '\"\"': response[i+1] == ' '
                except IndexError: pass
            response = extractQuote(response, 6)
            print(response)
            if "" in response:
                printRed("Incomplete response generated! Retrying node \"%s\"" % id)
                # Response regenerated with random seed, hopefully getting a satisfactory response. If not, it's a lost cause anyway _/¯(ツ)_/¯
                response = extractQuote(model.generate("CHAT SEED: %i\n%s" % (randint(0, 9999), currentStory), max_tokens=400, temp=.75), 6)
            genChoices, genStories = response[:3], response[3:]
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
    storydata.append(newNode)
    if currentDepth < finalDepth:
        createStory(id + '0', prevGenStories)
        createStory(id + '1', prevGenStories)
        createStory(id + '2', prevGenStories)
        prevGenStories.pop()

createStory()

printGreen("Story successfully generated!")

storydata.append({
    "depth": finalDepth,
    "title": title
    })

with open(storypath, "w") as file:
    json.dump(storydata, file)

printGreen("Story saved!")