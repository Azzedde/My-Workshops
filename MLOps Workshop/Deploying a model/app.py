from flask import Flask, render_template, request, redirect, url_for
from keras.preprocessing.image import load_img
from model import process_image, predict_class
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = './static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/home', methods=['GET', 'POST'])
def home():
    welcome = "Hello, World !"
    return welcome

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'photo' not in request.files:
            return redirect(request.url)
        file = request.files['photo']
        
        # If user does not select a file, the browser submits an empty file
        if file.filename == '':
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Load, process, and predict
            image = load_img(filepath, target_size=(224, 224))
            image = process_image(image)
            prediction, percentage = predict_class(image)

            answer = "For {} : <br>The prediction is : {} <br>With probability = {}".format(filename, prediction, percentage)
            return answer

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)