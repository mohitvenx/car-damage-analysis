from posixpath import basename
from flask import Flask, render_template,redirect, request
import joblib
import os
from os.path import join, dirname, realpath
from flask import Flask, request, redirect, url_for, send_from_directory, render_template, flash
from werkzeug.utils import secure_filename
import os
import threading
import product
from product import *
import damagearea_bbox
from damagearea_bbox import *
import ntpath
from flasgger import Swagger


#UPLOAD_FOLDER = join(dirname(realpath('save.jpg')), "C:/Users/Admin/OneDrive/Desktop/damaged_cars/file_input")
#BOUNDING_FOLDER = join(dirname(realpath('save.jpg')), "C:/Users/Admin/OneDrive/Desktop/damaged_cars/area-bbox-test")

UPLOAD_FOLDER = join(dirname(realpath('save.jpg')), "./file_input")
BOUNDING_FOLDER = join(dirname(realpath('save.jpg')), "./area-bbox-test")

ALLOWED_EXTENSIONS = {'png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG', 'gif', 'GIF'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['BOUNDING_FOLDER'] = BOUNDING_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.secret_key = 'key'

#bounding_location = "C:/Users/Admin/OneDrive/Desktop/damaged_cars/area-bbox-test"
bounding_location = "./area-bbox-test"


os.environ["FLASK_ENV"] = "development"

port = 5000

location = './templates'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def home():
   return render_template("./index.html")
  
    
@app.route('/<a>')
def available(a):
	flash('Please contact {} for concerns and queries'.format(a))
	return render_template("./index.html", result=None, scroll='third')


@app.route('/')
def assess():
   return render_template("./index.html", result=None, scroll='third')


@app.route('/assessment', methods=['GET', 'POST'])
def upload_and_classify():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('assess'))

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('assess'))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            box = damagearea_bbox.bounding_box(filepath)
            model_results = product.pipe(filepath)
            
    
            return render_template("./results.html", result=model_results, scroll='third', filename=filename)

    flash('Invalid file format. Please try again.')
    return redirect(url_for('assess'))




@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/results/<filename>')
def send_boxfile(filename):
    basename = ntpath.basename(filename)
    return send_from_directory(BOUNDING_FOLDER, basename)



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/results/<filename>')
def uploaded_boxfile(filename):
    return send_from_directory(app.config['BOUNDING_FOLDER'], basename)


#app.run(host = '0.0.0.0',port = '5000', use_reloader=False)
app.run(host = '0.0.0.0',port = '5000', use_reloader=os.environ.get('DEBUG')=='1')

