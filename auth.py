# auth.py
from firebase_admin import auth
from flask import request, jsonify # type: ignore

def get_user_id_from_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None, "Missing Authorization header"
    
    id_token = auth_header.split("Bearer ")[-1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token['uid'], None
    except Exception as e:
        return None, str(e)
