let currentID = '';
let storyData = null;
let base10ID = 0;
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

const text = document.getElementById('text');
const choice0 = document.getElementById('choice0');
const choice1 = document.getElementById('choice1');
const choice2 = document.getElementById('choice2');

function updateScreen() {
    console.log("updateScreen called, base10ID: " + base10ID);
    if (currentID != '') {
        base10ID = parseInt(currentID, 3) + 1;
    }
    text.innerHTML = storyData[base10ID].text;
    choice0.innerHTML = storyData[base10ID].choices[0].text;
    choice1.innerHTML = storyData[base10ID].choices[1].text;
    choice2.innerHTML = storyData[base10ID].choices[2].text;
}

addEventListener('click', function (event) {
    console.log("addEventListener called, base10ID: " + base10ID);
    if (event.target === choice0) {
        currentID = storyData[base10ID].choices[0].nextNodeID;
        updateScreen();
    } else if (event.target === choice1) {
        currentID = storyData[base10ID].choices[1].nextNodeID;
        updateScreen();
    } else if (event.target === choice2) {
        currentID = storyData[base10ID].choices[2].nextNodeID;
        updateScreen();
    }
})