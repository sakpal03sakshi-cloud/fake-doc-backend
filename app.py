from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


app = Flask(__name__)

# Upload settings
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def register():
    return render_template('register.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/process', methods=['POST'])
def process():
    # ✅ SAFETY CHECK
    if 'document' not in request.files:
        return "ERROR: No file part named 'document'"

    file = request.files['document']

    if file.filename == '':
        return "ERROR: No file selected"

    if not allowed_file(file.filename):
        return "ERROR: File type not allowed"

    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    extracted_text = ""

    # OCR only for images
    if filename.lower().endswith(('png', 'jpg', 'jpeg')):
        img = Image.open(path)
        extracted_text = pytesseract.image_to_string(img)

    # Simple document validation logic
    keywords = ['government', 'india', 'name', 'date', 'id']
    score = sum(1 for k in keywords if k in extracted_text.lower())

    if score >= 3:
        status = "REAL DOCUMENT"
        confidence = "90%"
        remark = "Document structure and content look valid."
    else:
        status = "FAKE DOCUMENT"
        confidence = "55%"
        remark = "Missing official patterns or text."

    return render_template(
        'result.html',
        status=status,
        confidence=confidence,
        remark=remark
    )

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000, debug=True)



