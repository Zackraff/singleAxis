from flask import Flask
from firebase_admin import credentials
import firebase_admin
import logging, os
from app.config import LoadConfig

app = Flask(__name__)

config = LoadConfig.config
for section in config:
    for param in config[section]:
        logging.debug(
            ">> %s.%s\t:%s"
            % (section, param, config[section][param])
        )

current_directory = os.path.dirname(os.path.abspath(__file__))
sdk_path = os.path.join(current_directory, 'assets', 'firebase-sdk.json')
if not firebase_admin._apps:
    cred = credentials.Certificate(sdk_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': config['firebase']['url']
    })

from app import routes