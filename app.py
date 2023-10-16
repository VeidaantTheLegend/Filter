# Program to Upload Color Image and convert into Black & White image
import os
from flask import  Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2 
import numpy as np

app = Flask(__name__)

# Write load_form function below to Open and redirect to default upload webpage
@app.route('/')
def load_form():
    return render_template('upload.html')
# Write upload_image Function to upload image and redirect to new webpage
@app.route('/', methods = ['POST'])
def upload_image():
    optionselection = request.form['imagetypeselection']
    file = request.files['file']
    filename = secure_filename(file.filename)
    readfile = file.read()
    image_array = np.fromstring(readfile, dtype = 'uint8')
    decodeimage = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)
    if optionselection == 'gray':
        file_data = make_greyscale(decodeimage)

    elif optionselection == 'sketch':
        file_data = image_sketch(decodeimage)

    elif optionselection == 'oil':
        file_data = oil_effect(decodeimage)

    elif optionselection == 'rgb':
        file_data = rgb_effect(decodeimage)
    
    elif optionselection == 'hdr':
        file_data = hdr_effect(decodeimage)

    elif optionselection == 'oil':
        file_data = water_effect(decodeimage)

    elif optionselection == 'inv':
        file_data = invert_effect(decodeimage)

    else:
        print('No image selected')


    with open(os.path.join('static/', filename), 'wb') as f:
        f.write(file_data)
    display_message = filename + ' successfully uploaded and displayed below.'
    return render_template('upload.html', filename = filename, message = display_message)

def image_sketch(inputimage):
    convertedgrayimage = cv2.cvtColor(inputimage, cv2.COLOR_BGR2GRAY)
    sharpimage = cv2.bitwise_not(convertedgrayimage)
    blurimage = cv2.GaussianBlur(sharpimage, (111,111),0)
    sharpblur = cv2.bitwise_not(blurimage)
    sketchimage = cv2.divide(convertedgrayimage, sharpimage, 256.0)
    status, output_image = cv2.imencode('.PNG', sketchimage)
    return output_image
    print(status)

def make_greyscale(inputimage):
    convertedimage = cv2.cvtColor(inputimage, cv2.COLOR_RGB2GRAY)
    status, output_image = cv2.imencode('.PNG', convertedimage)
    return output_image
    print(status)

def oil_effect(inputimage):
    oil_effect_image = cv2.xphoto.oilPainting(inputimage, 7, 1)
    status, output_image = cv2.imencode('.PNG', oil_effect_image)
    return output_image
    print(status)

def rgb_effect(inputimage):
    rgb_effect_image = cv2.cvtColor(inputimage, cv2.COLOR_BGR2RGB)
    status, output_image = cv2.imencode('.PNG', rgb_effect_image)
    return output_image
    print(status)

def hdr_effect(inputimage):
    hdr_image = cv2.detailEnhance(inputimage, sigma_s = 12, sigma_r = 0.15)
    status, output_image = cv2.imencode('.PNG', hdr_image)
    return output_image
    print(status)

def water_effect(inputimage):
    water_image = cv2.stylization(inputimage, sigma_s = 60, sigma_r = 0.6)
    status, output_image = cv2.imencode('.PNG', water_image)
    return output_image
    print(status)

def invert_effect(inputimage):
    invert_image = cv2.bitwise_not(inputimage)
    status, output_image = cv2.imencode('.PNG', invert_image)
    return output_image
    print(status)

# Write display_image Function to display the uploaded image
@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename = filename))

if __name__ == "__main__":
    app.run()