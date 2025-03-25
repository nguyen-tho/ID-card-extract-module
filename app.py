from flask import Flask, request, jsonify, render_template, redirect, url_for
from process import processing  # Import the processing function from your module
import sys
import postprocessing as post
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='template')
app.json.ensure_ascii = False
@app.route('/')
def home():
    return render_template('index.html')



@app.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        username = request.form.get('username')
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            filepath = os.path.join('uploads', filename)
            image.save(filepath)

            # Process the image directly here
            try:
                processing(filepath, username)
                result = post.read_json_file(f'output/{username}/result.json')
                return jsonify(result) # Or return some other success message
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        else:
            return "No image uploaded", 400
    else:
        return render_template('index.html')



if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)