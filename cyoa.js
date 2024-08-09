let currentID = '';
let storyData;
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
    })
    .catch(error => {
        console.error('Error loading story.json:', error);
    });

text = document.getElementById('text');
choice0 = document.getElementById('choice0');
choice1 = document.getElementById('choice1');
choice2 = document.getElementById('choice2');

function updateScreen() {
    text.innerHTML = storyData[currentID].text;
    choice0.innerHTML = storyData[currentID].choices[0].text;
    choice1.innerHTML = storyData[currentID].choices[1].text;
    choice2.innerHTML = storyData[currentID].choices[2].text;
}

updateScreen();

addEventListener('click', function (event) {
    if (event.target === choice0) {
        currentID = storyData[currentID].choices[0].nextID;
        updateScreen();
    } else if (event.target === choice1) {
        currentID = storyData[currentID].choices[1].nextID;
        updateScreen();
    } else if (event.target === choice2) {
        currentID = storyData[currentID].choices[2].nextID;
        updateScreen();
    }
})