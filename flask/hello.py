import csv
import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import datetime

from scrape_main import search
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home page
@app.route('/')
def index():
    # Get all the files in the uploads folder
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    for file in files:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
    return render_template('index.html')

# Create a file
# TODO: Add error handling for empty inputs
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        search_term = request.form['search_term']
        filename = request.form['file_name']
        # TODO: Do the error handling in the front end as well
        if not search_term or not filename:
            return redirect(request.url)
        filename = secure_filename(filename)
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
        filename = "{}_{}".format(filename, formatted_datetime)
        filename = "{}.csv".format(filename)

    
        full_filename = "{}/{}".format(app.config["UPLOAD_FOLDER"], filename)
        column_names = ["URL", "Date", "Remark", "Title", "Author", "Type", "Price", "Summary", "Publication Year", "Language", "ISBN", "Category", "Copyright", "Contributors",
        "Pages", "Binding", "Interior Color", "Dimensions", "Format", "Keywords"]
        with open(full_filename, 'w', encoding="utf-8", newline='') as f:
            csv_obj = csv.DictWriter(f, fieldnames=column_names)
            csv_obj.writeheader()
        
        search(search_term, full_filename)

        return redirect(url_for('download_file', name=filename))
    
    return render_template('create.html')

# Update an existing file
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # Check if file exists and is valid
        if not file.filename or not allowed_file(file.filename):
            return redirect(request.url)
        filename = secure_filename(file.filename)
        filename = filename.split("_")
        filename = "_".join(filename[:-6])
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
        filename = "{}_{}".format(filename, formatted_datetime)
        filename = "{}.csv".format(filename)
        search_term = request.form['search_term']
        full_filename = "{}/{}".format(app.config["UPLOAD_FOLDER"], filename)
        file.save(full_filename)
        search(search_term, full_filename)
        return redirect(url_for('download_file', name=filename))
    
    return render_template('upload.html')

# File download redirect
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)