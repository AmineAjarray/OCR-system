from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

try:  
    from PIL import Image
except ImportError:  
    import Image


def ocr_core(filename):  
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

app = Flask(__name__, template_folder = 'template')
     
app.secret_key = "cairocoders-ednalan"
  
UPLOAD_FOLDER = 'static/uploads/'
  
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
  
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
  
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
      
  
@app.route('/')
def home():
  return render_template('index.html')
  
@app.route('/', methods=['POST'])
def upload_image():
  print("9wed")
  if 'file' not in request.files:
    flash('No file part')
    return redirect(request.url)
  file = request.files['file']
  if file.filename == '':
    print('No image selected for uploading')
    return redirect(request.url)
  if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    ocr = ocr_core(file)
    print('Image successfully uploaded and displayed below')
    print(ocr)
    return render_template('index.html', text=ocr)
  else:
    print('Allowed image types are - png, jpg, jpeg, gif')
    return redirect(request.url)
  
  
if __name__ == "__main__":
    app.run()

