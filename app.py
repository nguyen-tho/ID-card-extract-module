from flask import Flask, request, jsonify, render_template, redirect, url_for
from process import processing  # Import the processing function from your module
import sys
import postprocessing as post
import os

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
        return redirect(f'/process/<{username}>/<{image.filename}>'), 200
    else:
        return render_template('index.html')
    
@app.route('/process/<username>/<image>', methods=['GET'])
def run_processing(username, image):
    file_path = os.path.join('uploads', image)
    try:
        # Assuming the input is a JSON payload with file_path and output_name

        # Extract parameters from the JSON payload
        # file_path = request.args.get('param1', default=sys.argv[1] if len(sys.argv) > 1 else None)
        # output_name = request.args.get('param2', default=sys.argv[2] if len(sys.argv) > 2 else None)

        # Check if the required parameters are present
        if not file_path or not image:
            return jsonify({'error': 'Missing required parameters'}), 400

        # Call the processing function with the provided parameters
        processing(file_path, username)
        result = post.read_json_file(f'output/{username}/result.json')

        # Return the result as JSON
        return jsonify(result)
    except Exception as e:
        # Handle any errors that may occur during the processing
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
