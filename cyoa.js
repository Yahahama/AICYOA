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
        console.log(data);
    })
    .catch(error => {
        console.error('Error loading story.json:', error);
    });