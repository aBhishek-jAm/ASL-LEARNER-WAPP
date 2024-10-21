// List of word images to display
const words = ['aunt', 'hi', 'thankyou', 'please', 'eat', 'enri_media', 'father', 'help', 'i_love_you', 'learn', 'mother', 'name', 'want', 'water']; // Add your words here corresponding to the images
let currentWordIndex = 0;
const wordImageElement = document.getElementById('alphabet-image');

// Set the initial image on page load
wordImageElement.src = `/static/images/words/${words[currentWordIndex]}.jpg`;

// Next button click event to change word image
document.getElementById('next-btn').addEventListener('click', () => {
    currentWordIndex = (currentWordIndex + 1) % words.length;
    const nextWord = words[currentWordIndex];
    
    // Log the current image being loaded for debugging
    console.log(`Loading image: /static/images/words/${nextWord}.jpg`);
    
    // Set the new image source
    wordImageElement.src = `/static/images/words/${nextWord}.jpg`;
});

// Webcam and word recognition setup for the intermediate model
const videoElement = document.createElement('video');
const canvasElement = document.getElementById('camera-canvas');
const canvasCtx = canvasElement.getContext('2d');

// Set up MediaPipe hands (similar to the beginner page)
navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
    videoElement.srcObject = stream;
    videoElement.play();

    // Draw the video stream on the canvas
    videoElement.addEventListener('loadeddata', () => {
        canvasElement.width = videoElement.videoWidth;
        canvasElement.height = videoElement.videoHeight;
        drawVideoToCanvas();
    });
});

function drawVideoToCanvas() {
    canvasCtx.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
    // Add your hand recognition or MediaPipe processing here if needed

    requestAnimationFrame(drawVideoToCanvas);
}

// Load the video feed for the intermediate page
document.getElementById('camera-video').src = "/video_feed_intermediate";

// Function to display predicted word (based on model output)
function displayPredictedWord(predictedWord) {
    const recognitionTextElement = document.getElementById('recognizing-text');
    recognitionTextElement.textContent = `Recognized Word: ${predictedWord}`;
}
