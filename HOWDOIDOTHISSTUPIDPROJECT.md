# HOWDOIDOTHISSTUPIDPROJECT
is a question I should have asked before trying to start it.

My first approach:

- AI is told that its only purpose in life is to fill in missing story
- AI recieves story node
- I tell AI to generate three comma seperated strings that represent choices based on that story node
- AI decides to keep generating story nodes and choices past that, even though I explicitly told it not to do that

This is clearly not working.

New approach idea:
- AI is told that it's a strong independent chatbot that has some sort of a personality
- AI recieves story node, in the template of a chatbot user messaging the chatbot
- AI hopefully creates three quoted choices seperated by commas
- The AI, with that chat history, is given a larger cap on tokens and is told to generate three followups in the same format
- AI does what it's supposed to and doesn't screw up