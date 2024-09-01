let currentID = '';
let storyData = [];
let currentNode = {};
// Replace the below URL with a URL that links to your raw story JSON
const storyURL = "https://yahahama.github.io/AICYOA/story.json";

const title = document.getElementById('title');
const text = document.getElementById('text');
const extra = document.getElementById('extra');
const choice0 = document.getElementById('choice0');
const choice1 = document.getElementById('choice1');
const choice2 = document.getElementById('choice2');
const reset = document.getElementById('reset');

fetch(storyURL)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        storyData = data;
        currentNode = storyData[0];
        updateScreen();
    })
    .catch(error => {
        console.error('Error loading story.json:', error);
    });

function updateScreen() {
    for (let i = 0; i < storyData.length; i++) {
        if (storyData[i].id === currentID) {
            currentNode = storyData[i];
            break;
        }
    }

    title.innerHTML = storyData[storyData.length - 1].title;
    text.innerHTML = currentNode.text;

    if (currentID.length >= storyData[storyData.length - 1].depth) {
        extra.innerHTML = "The end! Your ending ID is " + currentID;
        choice0.disabled = true;
        choice1.disabled = true;
        choice2.disabled = true;
    } else {
        choice0.innerHTML = currentNode.choices[0].text;
        choice1.innerHTML = currentNode.choices[1].text;
        choice2.innerHTML = currentNode.choices[2].text;
    }
}

addEventListener('click', function (event) {
    if (event.target === choice0) {
        currentID += '0';
        updateScreen();
    } else if (event.target === choice1) {
        currentID += '1';
        updateScreen();
    } else if (event.target === choice2) {
        currentID += '2';
        updateScreen();
    } else if (event.target === reset) {
        currentID = '';
        updateScreen();
        extra.innerHTML = "What do you do?";
        choice0.disabled = false;
        choice1.disabled = false;
        choice2.disabled = false;
    }
})