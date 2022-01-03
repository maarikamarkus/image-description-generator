from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
import image_description_generator
import base64

UPLOAD_FOLDER = './imgs'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_img_desc(request):
  if 'filename' not in request.files:
    return render_template('error.html', reason="No file added.")

  file = request.files['filename']

  if file.filename == '':
    return render_template('error.html', reason="No selected file.")

  if not file or not allowed_file(file.filename):
    return render_template('error.html', reason="This file type is not supported.")

  filename = secure_filename(file.filename)
  
  try:
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    desc = generate_description_from_file(path)

  finally:
    remove_file_from_server(path)
  
  return desc

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_description_from_file(path):
  with open(path, 'rb') as f:
    img_bytes = f.read()
    decoded = base64.b64encode(img_bytes).decode('ascii')

  desc = image_description_generator.get_img_desc(path)

  return render_template('result.html', decoded=decoded, desc=desc)

def remove_file_from_server(path):
  if os.path.exists(path):
      os.remove(path)
  return

@app.route("/", methods=['GET', 'POST'])
def index():
  if request.method == 'GET':
    return render_template('index.html')
  
  if request.method == 'POST':
    return get_img_desc(request)
