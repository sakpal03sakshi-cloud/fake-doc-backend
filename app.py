from flask import Flask, render_template, request
import os
from PIL import Image
import pytesseract

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- HOME / REGISTER ----------------
@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return render_template('upload.html')
    return render_template('register.html')


# ---------------- UPLOAD PAGE ----------------
@app.route('/upload')
def upload():
    return render_template('upload.html')


# ---------------- PROCESS DOCUMENT ----------------
@app.route('/process', methods=['POST'])
def process():
    if 'document' not in request.files:
        return "No file uploaded", 400

    file = request.files['document']
    if file.filename == '':
        return "No selected file", 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # OCR
    try:
        img = Image.open(filepath)
        text = pytesseract.image_to_string(img)
    except:
        text = ""

    keywords = ['government', 'india', 'name', 'date', 'id']
    score = sum(1 for k in keywords if k in text.lower())

    if score >= 3:
        status = "REAL DOCUMENT"
        confidence = "90%"
        remark = "Looks valid"
    else:
        status = "FAKE DOCUMENT"
        confidence = "55%"
        remark = "Missing official patterns"

    return render_template(
        'result.html',
        status=status,
        confidence=confidence,
        remark=remark
    )


if __name__ == '__main__':
    app.run(debug=True)





