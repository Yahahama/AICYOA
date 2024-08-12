let currentID = '';
let storyData = [];
let currentNode = {};
const storyURL = "https://yahahama.github.io/AICYOA/story.json";

const text = document.getElementById('text');
const choice0 = document.getElementById('choice0');
const choice1 = document.getElementById('choice1');
const choice2 = document.getElementById('choice2');

fetch(storyURL)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        storyData = data;
        console.log('Story data:', storyData);
        currentNode = storyData[0];
        print(storyData[0], currentNode);
        updateScreen();
    })
    .catch(error => {
        console.error('Error loading story.json:', error);
    });

function updateScreen() {
    if (currentID != '') {
        const nodeCount = storyData[storyData.length-1].depth;
        let c = 0;
        for (let i = 0; i < currentID.length; i++) {
            c += currentID[i]*nodeCount/3**i;
        }
        currentNode = storyData[c];
    }

    console.log("updateScreen() currentNode: "+currentNode);

    text.innerHTML = currentNode.text;
    choice0.innerHTML = currentNode.choices[0].text;
    choice1.innerHTML = currentNode.choices[1].text;
    choice2.innerHTML = currentNode.choices[2].text;
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
    }
})