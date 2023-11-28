from flask import Flask, request, jsonify
from process import processing  # Import the processing function from your module
import sys
import postprocessing as post

app = Flask(__name__)
app.json.ensure_ascii = False

@app.route('/', methods=['GET'])
def run_processing():
    try:
        # Assuming the input is a JSON payload with file_path and output_name
        
        
        # Extract parameters from the JSON payload
        file_path = request.args.get('param1', default=sys.argv[1] if len(sys.argv) > 1 else None)
        output_name = request.args.get('param2', default=sys.argv[2] if len(sys.argv) > 2 else None)


        # Check if the required parameters are present
        if not file_path or not output_name:
            return jsonify({'error': 'Missing required parameters'}), 400

        # Call the processing function with the provided parameters
        processing(file_path, output_name)
        result = post.read_json_file(f'output/{output_name}/result.json')

        # Return the result as JSON
        return jsonify(result)
    except Exception as e:
        # Handle any errors that may occur during the processing
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
