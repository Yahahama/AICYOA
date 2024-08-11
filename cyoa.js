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
        console.log("Story loaded successfully", storyData);
        updateScreen();
    })
    .catch(error => {
        console.error('Error loading story.json:', error);
    });

text = document.getElementById('text');
choice0 = document.getElementById('choice0');
choice1 = document.getElementById('choice1');
choice2 = document.getElementById('choice2');

function updateScreen() {
    if (currentID === '') {
        base10ID = 0;
    } else {
        base10ID = parseInt(currentID, 3) + 1;
    }
    console.log("Beginning crazy logs!")
    console.log(base10ID);
    console.log(storyData);
    console.log(storyData[base10ID]);
    console.log(storyData[base10ID].text);
    text.innerHTML = storyData[base10ID].text;
    choice0.innerHTML = storyData[base10ID].choices[0].text;
    choice1.innerHTML = storyData[base10ID].choices[1].text;
    choice2.innerHTML = storyData[base10ID].choices[2].text;
    console.log("updateScreen ran successfully")
}

console.log("Got to event listener!")
addEventListener('click', function (event) {
    if (event.target === choice0) {
        currentID = storyData[base10ID].choices[0].nextNode;
        updateScreen();
    } else if (event.target === choice1) {
        currentID = storyData[base10ID].choices[1].nextNode;
        updateScreen();
    } else if (event.target === choice2) {
        currentID = storyData[base10ID].choices[2].nextNode;
        updateScreen();
    }
})