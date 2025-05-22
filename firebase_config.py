import firebase_admin
from firebase_admin import credentials
import os
import json

# Read JSON from environment variable
firebase_creds = os.environ.get("FIREBASE_ADMIN_CREDS")
if firebase_creds:
    cred_dict = json.loads(firebase_creds)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
else:
    raise RuntimeError("FIREBASE_ADMIN_CREDS environment variable not set.")
