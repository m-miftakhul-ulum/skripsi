import os
from flask import Flask, request, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES, AUDIO
from uuid import uuid4

app = Flask(__name__)

# Folder untuk menyimpan file
app.config['UPLOADED_AUDIOS_DEST'] = 'uploads/audios'
app.config['UPLOADED_IMAGES_DEST'] = 'uploads/images'

# Membuat set uploads untuk audio dan images
audios = UploadSet('audios', AUDIO)
images = UploadSet('images', IMAGES)

# Konfigurasi uploads
configure_uploads(app, (audios, images))

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and (file.filename.endswith('.wav') or file.filename.endswith('.jpg')):
        # Membuat nama file unik
        ext = os.path.splitext(file.filename)[1]
        unique_filename = str(uuid4()) + ext
        
        if file.filename.endswith('.wav'):
            filename = audios.save(file, name=unique_filename)
        else:
            filename = images.save(file, name=unique_filename)
        
        return jsonify({"message": "File successfully uploaded", "filename": filename}), 200
    else:
        return jsonify({"error": "Invalid file type, only .wav and .jpg are allowed"}), 400

if __name__ == '__main__':
    app.run(debug=True)
