import os
import base64
import json
import firebase_admin
from firebase_admin import credentials, auth, initialize_app
from dotenv import load_dotenv

load_dotenv()

# Decode the base64-encoded service account key
firebase_key_b64 = os.getenv("FIREBASE_ADMIN_KEY_B64")
if not firebase_key_b64:
    raise ValueError("FIREBASE_ADMIN_KEY_B64 not found in environment variables")

firebase_key_json = base64.b64decode(firebase_key_b64).decode("utf-8")
cred_data = json.loads(firebase_key_json)

# Initialize Firebase
cred = credentials.Certificate(cred_data)
if not firebase_admin._apps:
    initialize_app(cred)  

# Export auth module for convenience
firebase_auth = auth
