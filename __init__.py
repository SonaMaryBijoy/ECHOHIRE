from flask import Flask
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Upload folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import routes  # keep this LAST
