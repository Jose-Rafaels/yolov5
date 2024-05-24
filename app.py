from flask import Flask, request, jsonify
from detect import run as yolo_app
import os
import uuid

# Initialize the Flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'test-image/'
app.secret_key = 'supersecretkey'
unique_filename = ''
model_path = 'best.pt'  # Path to your custom YOLOv5 model


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

def generate_unique_filename(file):
    ext = file.filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return unique_filename

# @app.route('/')
# def index():
#     return '''
#     <!doctype html>
#     <title>Upload File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success":"false"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"success":"false"})

    if file and allowed_file(file.filename):
        unique_filename = generate_unique_filename(file)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        res = yolo_app(weights =model_path, source = filepath,nosave=True)
        if os.path.exists("test-image/"+unique_filename):
            os.remove("test-image/"+unique_filename)
        if res != '' : 
            return jsonify({"success":"true", "res" : res})
        else :
            return jsonify({"success":"false", "res" : "Not Found"})

        
    else:
        return jsonify({"success":"false"})


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
