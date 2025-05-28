// List of alphabet images from A to Z
const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
let currentIndex = 0;
const alphabetImage = document.getElementById('alphabet-image');

// Next button click event
document.getElementById('next-btn').addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % letters.length;
    const nextLetter = letters[currentIndex];
    alphabetImage.src = `/static/images/alphabets/${nextLetter}.jpg`;

});

// Webcam and hand recognition setup
const videoElement = document.createElement('video');
const canvasElement = document.getElementById('camera-canvas');
const canvasCtx = canvasElement.getContext('2d');

// Set up MediaPipe hands (you would need to add hand landmark visualization here)
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
    // Call your hand recognition function here, e.g., MediaPipe

    requestAnimationFrame(drawVideoToCanvas);
} 