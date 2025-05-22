from flask import Flask, request, jsonify
from auth import get_user_id_from_token
from parser import parse_statement  # assume this is your function

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse():
    user_id, error = get_user_id_from_token()
    if error:
        return jsonify({'error': error}), 401

    data = request.get_json()
    result = parse_statement(data)
    result['user_id'] = user_id  # optional: attach user ID to the result
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
