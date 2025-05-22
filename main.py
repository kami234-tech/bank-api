from flask import Flask, request, jsonify
from auth import get_user_id_from_token
from parser import extract_transactions
import os

app = Flask(__name__)

@app.route('/')
def health():
    return 'Bank API is running 🚀', 200

@app.route('/parse', methods=['POST'])
def parse():
    user_id, error = get_user_id_from_token()
    if error:
        return jsonify({'error': error}), 401

    data = request.get_json()
    if 'pdf_path' not in data:
        return jsonify({'error': 'Missing pdf_path'}), 400

    if not os.path.exists(data['pdf_path']):
        return jsonify({'error': 'File not found'}), 404

    transactions = extract_transactions(data['pdf_path'])

    return jsonify({
        'user_id': user_id,
        'transactions': transactions
    })

if __name__ == '__main__':
    app.run(debug=True)
