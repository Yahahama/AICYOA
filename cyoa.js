let currentID = '';
const storyURL = "https://yahahama.github.io/AICYOA/story.json";

fetch(storyURL)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        storyData = data;
        updateScreen();
    })
    .catch(error => {
        console.error('Error loading story.json:', error);
    });

currentNode = storyData[0];

const text = document.getElementById('text');
const choice0 = document.getElementById('choice0');
const choice1 = document.getElementById('choice1');
const choice2 = document.getElementById('choice2');

function updateScreen() {
    if (currentID != '') {
        nodeCount = storyData[-1].depth;
        for (let i = 0, c = 0; i < currentID.length; i++) {
            c += currentID[i]*nodeCount/3**i;
        }
        currentNode = storyData[c];
    }
    text.innerHTML = currentNode.text;
    choice0.innerHTML = currentNode.choices[0].text;
    choice1.innerHTML = currentNode.choices[1].text;
    choice2.innerHTML = currentNode.choices[2].text;
}

addEventListener('click', function (event) {
    if (event.target === choice0) {
        currentID = currentNode.choices[0].nextNodeID;
        updateScreen();
    } else if (event.target === choice1) {
        currentID = currentNode.choices[1].nextNodeID;
        updateScreen();
    } else if (event.target === choice2) {
        currentID = currentNode.choices[2].nextNodeID;
        updateScreen();
    }
})