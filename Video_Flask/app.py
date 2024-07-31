from flask import Flask, request, jsonify, render_template  # Import necessary modules for building a Flask web application
import numpy as np  # Import numpy library for numerical computations
import tensorflow as tf  # Import TensorFlow library for using pre-trained neural network models
import cv2  # Import OpenCV library for image and video processing
import os  # Import os module for interacting with the operating system
import tempfile  # Import tempfile module for creating temporary files and directories
from werkzeug.utils import secure_filename  # Import secure_filename function for safely handling file uploads

app = Flask(__name__)  # Create a Flask application instance

app.config['MODEL_PATH'] = "static/model.keras"  # Set the path to the pre-trained model file
app.config['UPLOAD_FOLDER'] = "static/uploads"  # Set the directory where uploaded files will be saved
app.config['MAX_CONTENT_LENGTH'] = 256 * 1024 * 1024  # Set the maximum allowed size for uploaded files (256 MB)
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}  # Define the set of allowed file extensions

model = tf.keras.models.load_model(app.config['MODEL_PATH'])  # Load the pre-trained neural network model

# Define a function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define a function to run the neural network on input frames and return predictions
def runNeuralNetwork(frames):
    predictions = []
    for frame in frames:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the frame to RGB color format
        frame = cv2.resize(frame, (256, 256))  # Resize the frame to match the input size expected by the model
        frame = frame.astype('float32') / 255.0  # Normalize the pixel values of the frame
        frame = np.expand_dims(frame, axis=0)  # Add a batch dimension to the frame
        pred = model.predict(frame)[0][0]  # 1st zero for predicted output and 2nd zero for 1st element of the array
        predictions.append(pred)  # Append the prediction to the list of predictions
    return predictions

# Define a route for the landing page and render the mainpage.html template
@app.route('/', methods=['GET'])
def displayLandingPage():
    return render_template("mainpage.html")

# Define a route for handling video uploads and classifying the videos
@app.route('/upload', methods=['POST'])
def classifyVideo():
    if request.method == 'POST':
        resText = ''
        if 'video' not in request.files:
            resText = "Error uploading video"  # Handle case where video file is not present in the request
        else:
            file = request.files['video']  # Get the uploaded video file from the request
            
            if file and allowed_file(file.filename):  # Check if the file has an allowed extension
                temp_video_fd, temp_video_path = tempfile.mkstemp(suffix='.mp4')  # Create a temporary file path for storing the uploaded video
                file.save(temp_video_path)  # Save the uploaded video to the temporary file path

                # Extract frames from the uploaded video
                cap = cv2.VideoCapture(temp_video_path)
                frames = []
                success, image = cap.read()
                count = 0
                while success:
                    cap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))
                    success, image = cap.read()
                    if success:
                        frames.append(image)  # Append each frame to the list of frames
                        cv2.imwrite(f"static/uploads/frame{count}.jpg", image)  # Save each frame as a JPEG file
                        count += 1
                cap.release()
                
                os.close(temp_video_fd)  # Close the temporary file descriptor
                os.remove(temp_video_path)  # Remove the temporary video file

                # Pass the frames through the neural network for prediction
                predictions = runNeuralNetwork(frames)

                # Determine the overall video prediction based on the average prediction value
                avg_pred = np.mean(predictions)
                if avg_pred >= 0.5:
                    resText="Tyre Life Remaining: {:.2f}%. Tyre is in good condition".format(avg_pred * 100)
                else:
                    resText="Tyre Life Remaining: {:.2f}%. Tyre is not in good condition".format(avg_pred * 100)
            else:
                resText = "Error uploading video"  # Handle case where file extension is not allowed
        
        response = jsonify({'resText' : resText})  # Create a JSON response containing the result text
        response.headers.add('Access-Control-Allow-Origin', '*')  # Allow cross-origin resource sharing
        return response  # Return the JSON response

if __name__ == "__main__":
    app.run(port=5000)  # Run the Flask application on port 5000
