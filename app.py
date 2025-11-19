import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from utils.pdf_reader import extract_text_from_pdf
from utils.preprocess import preprocess_text
from utils.similarity import compute_similarities, highlight_matches

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
DOCUMENTS_FOLDER = os.path.join(BASE_DIR, 'documents')
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOCUMENTS_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_text = request.form.get('input_text', '').strip()
        uploaded_file = request.files.get('file')

        if uploaded_file and uploaded_file.filename != '' and allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(filepath)

            if filename.lower().endswith('.pdf'):
                input_text = extract_text_from_pdf(filepath)
            else:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    input_text = f.read()

        if not input_text:
            return render_template('index.html', error="Please enter text or upload a TXT/PDF file.")

        clean_input = preprocess_text(input_text)

        doc_texts = []
        doc_names = []
        for fname in os.listdir(DOCUMENTS_FOLDER):
            path = os.path.join(DOCUMENTS_FOLDER, fname)
            if os.path.isfile(path) and fname.endswith('.txt'):
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    raw = f.read()
                doc_texts.append(preprocess_text(raw))
                doc_names.append(fname)

        similarities, top_matches = compute_similarities(clean_input, doc_texts, doc_names)

        highlights = []
        for match in top_matches:
            idx = match['index']
            raw_path = os.path.join(DOCUMENTS_FOLDER, doc_names[idx])
            with open(raw_path, 'r', encoding='utf-8', errors='ignore') as f:
                raw_doc = f.read()

            highlighted = highlight_matches(input_text, raw_doc)
            highlights.append({
                'doc': doc_names[idx],
                'score': match['score'],
                'highlighted': highlighted
            })

        return render_template('result.html',
                               input_text=input_text,
                               similarities=similarities,
                               highlights=highlights)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
