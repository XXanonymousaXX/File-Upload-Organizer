import os
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configurations
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# File organization function
def organize_uploaded_files():
    file_categories = {
        'Images': ['jpg', 'jpeg', 'png', 'gif', 'bmp'],
        'Documents': ['pdf', 'docx', 'txt', 'xlsx', 'pptx'],
        'Videos': ['mp4', 'mkv', 'avi', 'mov'],
        'Music': ['mp3', 'wav', 'aac', 'flac'],
        'Archives': ['zip', 'rar', '7z', 'tar'],
    }

    for filename in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isdir(filepath):
            continue

        file_ext = filename.split('.')[-1].lower()
        organized = False

        for category, extensions in file_categories.items():
            if file_ext in extensions:
                target_folder = os.path.join(UPLOAD_FOLDER, category)
                os.makedirs(target_folder, exist_ok=True)
                os.rename(filepath, os.path.join(target_folder, filename))
                organized = True
                break
        
        if not organized:
            misc_folder = os.path.join(UPLOAD_FOLDER, "Misc")
            os.makedirs(misc_folder, exist_ok=True)
            os.rename(filepath, os.path.join(misc_folder, filename))

# Routes
@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files part in the request'}), 400

    files = request.files.getlist('files[]')
    if not files:
        return jsonify({'error': 'No files selected'}), 400

    # Save files to the upload folder
    for file in files:
        if file.filename == '':
            continue
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Organize the files
    organize_uploaded_files()
    return jsonify({'message': 'Files uploaded and organized successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
