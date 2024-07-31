function loadImage(event) {
    var imageOutput = document.querySelector("#imageOutput");
    // Display the selected image on the webpage
    imageOutput.src = URL.createObjectURL(event.target.files[0]);
}

document.querySelector("#imageUploadForm").addEventListener("submit", e => {
    e.preventDefault();
    
    var formData = new FormData();
    var image = document.querySelector('#imageInput').files[0];
    // Create a new FormData object and append the selected image to it
    formData.append('image', image);
    
    // Send a POST request to the server with the image data
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    // Parse the JSON response from the server
    .then(response => response.json())
    .then(data => {
        console.log("Response:", data);
        document.querySelector('#response').innerText = data['resText'];
    
        // Update the percentage counter
        let prediction = parseFloat(data['resText'].split(':')[1].split('%')[0]);
        let countElement = document.getElementById('percentageCount');
        let currentCount = parseFloat(countElement.innerText);
        let increment = 1; // Change this value to adjust the increment speed
    
        // Animate the count increase
        function updateCount() {
            if (currentCount < prediction) {
                currentCount += increment;
                countElement.innerText = currentCount.toFixed(2);
                setTimeout(updateCount, 10); // Change the timeout value for smoother animation
            }
        }
    
        updateCount();
    });    
});
