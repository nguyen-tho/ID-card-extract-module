from flask import Flask, request, jsonify, render_template
from process import processing  # Import the processing function from your module
import sys
import postprocessing as post
import os
from werkzeug.utils import secure_filename
from concurrent.futures import ThreadPoolExecutor
import threading # We'll use a dictionary to track processing status/results

app = Flask(__name__, template_folder='template')
app.json.ensure_ascii = False

# Dictionary to store results for polling
# In a real-world app, this would be a database or a more robust cache (e.g., Redis)
# Key: username, Value: {'status': 'processing'} or actual result data
processing_results = {}

@app.route('/')
def home():
    return render_template('index.html')

# Thread pool with 5 concurrent workers
executor = ThreadPoolExecutor(max_workers=5)

@app.route('/', methods=['POST']) # Changed route to /upload for clarity, though / could work
def upload_file(): # Renamed function to avoid conflict with the home route
    if request.method == 'POST':
        username = request.form.get('username')
        image = request.files.get('image')

        if not username:
            return jsonify({'error': 'Username is required.'}), 400
        if not image:
            return jsonify({'error': 'No image uploaded.'}), 400

        filename = secure_filename(image.filename)
        # Ensure a unique path for each user's upload or handle overwrites carefully
        user_upload_dir = os.path.join('uploads', username)
        if not os.path.exists(user_upload_dir):
            os.makedirs(user_upload_dir)
        filepath = os.path.join(user_upload_dir, filename) # Store in user-specific folder

        try:
            image.save(filepath)
        except Exception as e:
            print(f"Error saving image: {e}", file=sys.stderr)
            return jsonify({'error': f'Failed to save image: {str(e)}'}), 500

        # Set initial status for this user
        processing_results[username] = {'status': 'processing', 'message': 'Upload successful! Processing started.'}

        # Start processing in a background thread
        # Pass the username to the processing function or update `processing_results` directly inside
        executor.submit(process_and_save_result, filepath, username)

        # Return a simple acknowledgment that processing has started
        return jsonify(processing_results[username]), 202 # 202 Accepted

# This function runs in the background thread
def process_and_save_result(filepath, username):
    try:
        # Assuming your `processing` function saves the result to `output/{username}/result.json`
        processing(filepath, username)
        # Once processing is done, update the status in our shared dictionary
        result_path = os.path.join('output', username, 'result.json')
        if os.path.exists(result_path):
            result = post.read_json_file(result_path)
            processing_results[username] = result # Store the actual result
            print(f"Processing for {username} completed and result stored.")
        else:
            processing_results[username] = {'status': 'error', 'message': 'Processing finished but result file not found.'}
            print(f"Processing for {username} completed, but result.json not found.", file=sys.stderr)
    except Exception as e:
        processing_results[username] = {'status': 'error', 'message': f'Error during processing: {str(e)}'}
        print(f"Error processing for {username}: {str(e)}", file=sys.stderr)
    finally:
        # Clean up the uploaded file if desired
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Cleaned up uploaded file: {filepath}")


# A route to retrieve results based on username (for polling)
@app.route('/result/<username>', methods=['GET'])
def get_result(username):
    # Check if the result is in our in-memory dictionary
    if username in processing_results:
        result_data = processing_results[username]
        # If it's the actual result (not just 'processing' status), you might want to clean up
        # the entry after sending it, depending on your caching strategy.
        # For simple demo, we'll keep it.
        return jsonify(result_data), 200
    else:
        # If username not found at all, it hasn't been uploaded or started yet
        return jsonify({'status': 'Processing not initiated or user not found.'}), 404

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    if not os.path.exists('output'): # Ensure output directory exists
        os.makedirs('output')
    app.run(debug=True, threaded=True)