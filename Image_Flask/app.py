from flask import Flask, request, jsonify, render_template  # Import necessary modules for building a Flask web application
import numpy as np  # Import numpy library for numerical computations
import tensorflow as tf  # Import TensorFlow library for using pre-trained neural network models
import cv2  # Import OpenCV library for image processing
import os  # Import os module for interacting with the operating system
from werkzeug.utils import secure_filename  # Import secure_filename function for safely handling file uploads

app = Flask(__name__)  # Create a Flask application instance
app.static_folder = 'static'  # Set the directory for serving static files

app.config['MODEL_PATH'] = "static/model.keras"  # Set the path to the pre-trained model file
app.config['UPLOAD_FOLDER'] = "static/uploads"  # Set the directory where uploaded files will be saved
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Set the maximum allowed size for uploaded files (16 MB)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])  # Define the set of allowed file extensions

model = tf.keras.models.load_model(app.config['MODEL_PATH'])  # Load the pre-trained neural network model

# Define a function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define a function to run the neural network on an input image file and return the classification result
def runNeuralNetwork(filename):
    img = cv2.imread(filename)  # Read the image file using OpenCV
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert the color format from BGR to RGB
    img = cv2.resize(img, (256, 256))  # Resize the image to match the input size expected by the model

    x_test = np.array([img])  # Convert the image to a numpy array and add a batch dimension
    x_test = x_test.astype('float32')  # Convert the pixel values to floating point format
    x_test = x_test / 255.0  # Normalize the pixel values
    
    pred = model.predict(x_test)[0][0]  #  1st zero for predicted output and 2nd zero for 1st element of the array
    if pred >= 0.5:
        return "Tyre Life Remaining: {:.2f}%. Tyre is in good condition".format(pred * 100)
    else:
        return "Tyre Life Remaining: {:.2f}%. Tyre is not in good condition".format(pred * 100)

# Define a route for the landing page and render the mainpage.html template
@app.route('/', methods=['GET'])
def displayLandingPage():
    return render_template("mainpage.html")

# Define a route for handling image uploads and classifying the images
@app.route('/upload', methods=['POST'])
def classifyImage():
    if request.method == 'POST':
        resText = ''
        if 'image' not in request.files:
            resText = "Error uploading image"  # Handle case where image file is not present in the request
        else:
            file = request.files['image']  # Get the uploaded image file from the request
            
            if file and allowed_file(file.filename) and file.filename != '':
                filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))  # Generate a secure filename and save path
                file.save(filename)  # Save the uploaded image to the specified file path
                resText = runNeuralNetwork(filename)  # Run the neural network on the uploaded image and get the classification result
            else:
                resText = "Error uploading image"  # Handle case where file extension is not allowed
        
        response = jsonify({'resText' : resText})  # Create a JSON response containing the result text
        response.headers.add('Access-Control-Allow-Origin', '*')  # Allow cross-origin resource sharing
        return response  # Return the JSON response

if __name__ == "__main__":
    app.run(port=5000)  # Run the Flask application on port 5000
