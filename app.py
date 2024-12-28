from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import cv2 as cv
from predictTumor import predictTumor
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image = Image.open(filepath)
            mriImage = cv.imread(filepath, 1)
            res = predictTumor(mriImage)
            result = "Tumor Detected" if res > 0.5 else "No Tumor Detected"
            return render_template('result.html', result=result, image=filename)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
