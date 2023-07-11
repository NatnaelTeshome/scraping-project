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
    # Get all the files in the uploads folder to automatically delete them to free the space
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    for file in files:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
    return render_template('index.html', filename = None)

# Downloads the created/modified file
@app.route('/download_page/<items_count>/<time_diff>')
def download_page(items_count, time_diff):
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    if len(files) != 0:
        return render_template('download.html', filename = files[0], items_count = items_count, time_diff = time_diff)
    return render_template('download.html', filename = None)

# Create a file
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        search_term = request.form['search_term']
        filename = request.form['file_name']
        # Error handling for empty inputs
        if not search_term or not filename:
            return redirect(request.url)
        # Modify the filename
        filename = secure_filename(filename)
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
        filename = "{}_{}".format(filename, formatted_datetime)
        filename = "{}.csv".format(filename)
        full_filename = "{}/{}".format(app.config["UPLOAD_FOLDER"], filename)

        # Create a file with header
        column_names = ["URL", "Date", "Remark", "Title", "Author", "Type", "Price", "Summary", "Publication Year", "Language", "ISBN", "Category", "Copyright", "Contributors",
        "Pages", "Binding", "Interior Color", "Dimensions", "Format", "Keywords"]
        with open(full_filename, 'w', encoding="utf-8", newline='') as f:
            csv_obj = csv.DictWriter(f, fieldnames=column_names)
            csv_obj.writeheader()
        
        # Track the time it took to scrape
        start = datetime.datetime.now()

        items_count = search(search_term, full_filename)

        end = datetime.datetime.now()
        diff_seconds = end - start
        total_seconds = diff_seconds.total_seconds()
        hours = total_seconds // 3600
        remaining = total_seconds % 3600
        minutes = remaining // 60
        seconds = remaining % 60
        time_parts = [hours, minutes, seconds]
        for i in range(3):
            if time_parts[i] < 10:
                time_parts[i] = "0" + str(int(time_parts[i]))
            else:
                time_parts[i] = str(int(time_parts[i]))

        formatted_diff = ":".join(time_parts)

        return redirect(url_for('download_page', time_diff = formatted_diff, items_count = items_count))
    
    return render_template('create.html')

# Update an existing file
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        search_term = request.form['search_term']
        # Error handling for valid inputs
        if not file.filename or not allowed_file(file.filename) or not search_term:
            return redirect(request.url)
        filename = secure_filename(file.filename)
        # Isolate only the non-date section
        filename = filename.split("_")
        filename = "_".join(filename[:-6])
        # Modify the filename with a new date
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
        filename = "{}_{}".format(filename, formatted_datetime)
        filename = "{}.csv".format(filename)
        search_term = request.form['search_term']
        full_filename = "{}/{}".format(app.config["UPLOAD_FOLDER"], filename)
        file.save(full_filename)

        # Track the time it took to scrape
        start = datetime.datetime.now()

        items_count = search(search_term, full_filename)

        end = datetime.datetime.now()
        diff_seconds = end - start
        total_seconds = diff_seconds.total_seconds()
        hours = total_seconds // 3600
        remaining = total_seconds % 3600
        minutes = remaining // 60
        seconds = remaining % 60
        time_parts = [hours, minutes, seconds]
        for i in range(3):
            if time_parts[i] < 10:
                time_parts[i] = "0" + str(int(time_parts[i]))
            else:
                time_parts[i] = str(int(time_parts[i]))

        formatted_diff = ":".join(time_parts)

        return redirect(url_for('download_page', time_diff = formatted_diff, items_count = items_count))
    
    return render_template('upload.html')

# File download redirect
@app.route('/downloads/<name>', methods=['GET', 'POST'])
def download_file(name):
    if request.method == "POST" or request.method == "GET":
        return send_from_directory(app.config["UPLOAD_FOLDER"], name)