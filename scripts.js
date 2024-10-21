document.getElementById('convert-btn').addEventListener('click', () => {
    const inputText = document.getElementById('text-input').value;
    const words = inputText.split(' ');
    const imageContainer = document.getElementById('image-container');
    imageContainer.innerHTML = ''; // Clear previous images

    words.forEach(word => {
        const wordImage = `${word}.jpg`; // Correct usage of template literal
        const imgPath = `/static/images/words/${wordImage}`; // Correct path construction

        // Create an image element for the word
        const imgElement = document.createElement('img');
        imgElement.src = imgPath;

        imgElement.onload = () => {
            console.log(`Loaded word image: ${imgPath}`); // Log successful load
            imageContainer.appendChild(imgElement); // Add image to container if it loads
        };

        imgElement.onerror = () => {
            console.log(`Word image not found: ${word}`); // Log if word image not found

            // Load character images if word image fails
            for (let char of word) {
                const charImage = `${char.toLowerCase()}.jpg`; // Adjust for alphabet images
                const charImgPath = `/static/images/alphabets/${charImage}`; // Correct path for character images

                const charImgElement = document.createElement('img');
                charImgElement.src = charImgPath;

                charImgElement.onload = () => {
                    console.log(`Loaded character image: ${charImgPath}`); // Log successful load
                    imageContainer.appendChild(charImgElement); // Add character image to container
                };

                charImgElement.onerror = () => {
                    console.log(`Character image not found: ${char}`); // Log if image not found
                };
            }
        };
    });
});
