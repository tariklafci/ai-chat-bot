from flask import Flask, request, jsonify
from chat_job import ChatJob

app = Flask(__name__)
app.debug = True

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    message = data.get('message', '').strip()

    if not message:
        return jsonify({'reply': 'Please provide a message.'}), 400

    try:
        job = ChatJob(user_message=message)
        job.run()
        return jsonify({'reply': job.reply})
    except Exception as e:
        return jsonify({'reply': 'Error occurred.', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

