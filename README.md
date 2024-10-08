# AICYOA
###### (Artificial Intelligence Choose-Your-Own-Adventure)

A project that attempts to create choose-your-own-adventure interactive game stories using an AI, as well as displaying those stories in the browser.

Go [here](https://yahahama.github.io/AICYOA/) for a web demo of a story generated using this.

![A screenshot of the site displaying an AI-generated story](https://raw.githubusercontent.com/Yahahama/AICYOA/main/References/AICYOA%20Screenshot%202024-08-31%20204719.png)

## Table of Contents

- [Usage](#usage)
- [Limitations](#limitations)
- [Notes](#notes)

## Usage

The Python script aistorycreator.py is tricky to use.

I used Python 3.11 when running it with the modules random, json, sys, os, and GPT4ALL. The latter is not in Python's standard modules, so you need to install it with `pip install gpt4all`.

The LLM that is prompted to write the stories runs locally and is installed from GPT4ALL's app. You need to set modelPath to your file path where the model is installed, and replace the placeholder "PUT_YOUR_MODEL_NAME_HERE" with the actual model name. The model I used is called "Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf", and the script is untested on others. I suspect it works far worse on models smaller than it and possibly better on larger models.

The script, when run, will prompt you for an optional title (defaulting to "Untitled Story"), an optional starting scenario to begin branching from, and a positive integer "depth" of at least 1, indicating how many choices the final story will have. Note that the LLM will be prompted $\frac{3d^2 - d}{2}$ times, so it'll take a lot of resources to put a higher number in.

You then just need to wait for it to tell you it's finished. No further input is required, and at the end it overwrites story.json with the new story.

The Javascript script, cyoa.js, loads the JSON file from an online URL. Upload the JSON to something like GitHub sites where it's hosted online, and replace storyURL with the correct URL. Finally, open index.html in a browser to display your interactive story.

## Limitations

The story generation is slow if you don't have the proper hardware. Using an API like the one OpenAI provides should provide better models at better speeds compared to a local LLM.

The AI's story generation is blind. It only references a single part of the story to generate the proceeding nodes, so there is no consistency across branches. This also means the endings, when understood to be endings by the AI, are abrupt.

The AI generates repetitive stories, sometimes repeating endings and events.

There are occasionally holes left during story generation where certain nodes are wholly or partially left blank, ruining all nodes that stem from the empty parts.

The AI could maybe be made more creative and reliable during generation by finetuning; giving it many examples of ideal responses to prompting.

## Notes
*Github Copilot used for some coding questions and asking why things might not be working, but vast majority of code and most debugging is done with sustainably-farmed handmade artisanal bytes.*