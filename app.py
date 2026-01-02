from flask import Flask, render_template, request

from PIL import Image
import os
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def register():
    return render_template('register.html')

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["document"]

    if file.filename == "":
        return "No file selected"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # Fake verification logic (demo)
    result = "REAL" if file.filename.lower().endswith((".jpg", ".png")) else "FAKE"

    return render_template("result.html", result=result, image=file.filename)


@app.route('/process', methods=['POST'])
def process():
    file = request.files['document']
    path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(path)

    # OCR
    img = Image.open(path)
    text = pytesseract.image_to_string(img)

    # Advanced document validation logic
    keywords = ['government', 'india', 'name', 'date', 'id']
    score = sum(1 for k in keywords if k.lower() in text.lower())

    if score >= 3:
        status = "REAL DOCUMENT"
        confidence = 90
        remark = "Document structure & content look valid."
    else:
        status = "FAKE DOCUMENT"
        confidence = 55
        remark = "Missing official patterns or text."

    return render_template(
        'result.html',
        status=status,
        confidence=confidence,
        remark=remark
    )

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000, debug=True)


