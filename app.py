from flask import Flask, request, jsonify
import fitz # PyMuPDF
import spacy
nlp = spacy.load("en_core_web_sm")
# from spacy.matcher import Matcher

app = Flask(__name__)

@app.route('/')
def home():
    return "AI Resume Analyzer is running!"

@app.route('/upload', methods = ['POST'])
def upload_file():
    # Check if a file is part of a request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']

    # Checks that the file is legit
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    # Process only PDFs
    if file and file.filename.endswith('.pdf'):
        try:
            doc = fitz.open(stream=file.read(), filetype='pdf')
            text = ""
            for page in doc:
                text += page.get_text()

            # Extract sections after parsing the text
            sections = extract_sections(text)
            return jsonify({'content': sections})
        
        except Exception as e:
            return jsonify({'error': str(e)})
    
    return jsonify({'error': 'Unsupported file format'})

def extract_sections(resume_text):
    doc = nlp(resume_text)
    sections = {'EXPERIENCE': '', 'PROJECTS': '', 'EDUCATION': '', 'SKILLS': ''}
    current_section = None
    
    # Extract text under section headers
    for token in doc:
        text = token.text.upper()
        if text in sections:
            current_section = text
        elif current_section:
            # Append the token text to the current section
            sections[current_section] += ' ' + token.text

    return sections

if __name__ == '__main__':
    app.run(debug=True)