from flask import Flask, request
from werkzeug.utils import secure_filename
import os
import image_description_generator
import base64

UPLOAD_FOLDER = './imgs'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
  if request.method == 'GET':
    with open('index.html') as f:
      return f.read()
  
  if request.method == 'POST':
    if 'filename' not in request.files:
      return 'No file part'
      
    file = request.files['filename']
    if file.filename == '':
      return 'No selected file'

    if not file or not allowed_file(file.filename):
      return 'bad boy'

    filename = secure_filename(file.filename)
    
    try:
      path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      file.save(path)

      with open(path, 'rb') as f:
        img_bytes = f.read()
        decoded = base64.b64encode(img_bytes).decode('ascii')

      desc = image_description_generator.get_img_desc(path)
      #desc = "jou"

      return f'''
          <img src="data:image/jpeg;base64, {decoded}" width=500 style="display: block">
          <p style="width: 500px">{desc}</p>
        
        '''

    finally:
      if os.path.exists(path):
        os.remove(path)
