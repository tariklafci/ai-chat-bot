from flask import Flask, request, jsonify
from flask_cors import CORS
from job import call_llm, parse_response
import os

# Serve React/HTML from ../web folder
env_web = os.path.join(os.path.dirname(__file__), '..', 'web')
app = Flask(__name__, static_folder=env_web, static_url_path='')
CORS(app)  # allow cross-origin requests for local testing
app.debug = True

# Serve index.html at the root
@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')

# Proxy static assets
@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return app.send_static_file(path)

# LLM generate endpoint
@app.route('/api/llama/generate', methods=['POST'])
def generate():
    data = request.get_json() or {}
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    llm_output = call_llm(prompt)
    print(f"\n[DEBUG] LLM Output:\n{llm_output}\n")  # Add this

    title, code = parse_response(llm_output)

    return jsonify({
        'title': title,
        'code': code.splitlines(),
        'raw': llm_output
    }), 200


if __name__ == '__main__':
    # default host and port
    app.run(host='0.0.0.0', port=5000)
