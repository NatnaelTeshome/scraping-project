import csv
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

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
    return render_template('index.html')

# Create a file
# TODO: Add error handling for empty inputs
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        search_term = request.form['search_term']
        file_name = request.form['file_name']
        # TODO: Do the error handling in the front end as well
        if not search_term or not file_name:
            return redirect(request.url)
        file_name = secure_filename(file_name)
        file_name = "{}.csv".format(file_name)
        full_file_name = "./uploads/{}".format(file_name)
        column_names = ["URL", "Date", "Title", "Author", "Type", "Price", "Summary", "Publication Year", "Language", "ISBN", "Category", "Copyright", "Contributors",
        "Pages", "Binding", "Interior Color", "Dimensions", "Format", "Keywords"]
        with open(full_file_name, 'w', encoding="utf-8", newline='') as f:
            csv_obj = csv.DictWriter(f, fieldnames=column_names)
            csv_obj.writeheader()
        search(search_term, full_file_name)
        return redirect(url_for('download_file', name=file_name))
    
    return render_template('create.html')

# Update an existing file
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        print("reached if statement")
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # Check if file exists and is valid
        if not file.filename or not allowed_file(file.filename):
            return redirect(request.url)
        filename = secure_filename(file.filename)
        search_term = request.form['search_term']
        full_file_name = "./uploads/" + filename
        file.save(full_file_name)
        search(search_term, full_file_name)
        return redirect(url_for('download_file', name=filename))
    
    return render_template('upload.html')

# File download redirect
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)
