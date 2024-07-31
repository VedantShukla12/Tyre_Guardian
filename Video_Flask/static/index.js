function loadVideo(event) {
    var videoOutput = document.querySelector("#videoOutput");
    // Display the selected video on the webpage
    videoOutput.src = URL.createObjectURL(event.target.files[0]);
}

document.querySelector("#videoUploadForm").addEventListener("submit", e => {
    e.preventDefault();
    
    var formData = new FormData();
    var video = document.querySelector('#videoInput').files[0];
    // Create a new FormData object and append the selected video to it
    formData.append('video', video);
    
    // Send a POST request to the server with the video data
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    // Parse the JSON response from the server
    .then(response => response.json())
    .then(data => {
        // Log the response data to the console
        console.log("Response:", data);
        // Display the response text on the webpage
        document.querySelector('#response').innerText = data['resText'];
    });
});
