from flask import Flask, request, jsonify
from extractor import ContactExtractor
import tempfile
from pathlib import Path
import os

app = Flask(__name__)
extractor = ContactExtractor()

@app.route('/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    files = request.files.getlist('file')
    if not files or all(f.filename == '' for f in files):
        return jsonify({'error': 'No selected file'}), 400
    results = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for file in files:
            if file.filename == '':
                continue
            file_path = os.path.join(tmpdir, file.filename)
            file.save(file_path)
            names, phone_numbers = extractor.process_file(file_path)
            results.append({
                'filename': file.filename,
                'names': names,
                'phone_numbers': phone_numbers
            })
    return jsonify({'results': results})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
