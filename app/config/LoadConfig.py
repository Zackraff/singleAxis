import logging
import configparser
import os

default_config = {
    'firebase':{
        'url':'https://firebasedatabase.app/'
    }
}

def load_config():
    miss_config = []
    current_directory = os.getcwd()

    entries = os.listdir(current_directory)

    if "singleAxis.ini" in entries:
        config = configparser.ConfigParser()
        config.read('singleAxis.ini')

        if 'firebase' in config:
            if 'url' in config['firebase']:
                default_config['firebase']['url'] = config['firebase']['url']

            else:
                miss_config.append('firebase.url')
        
        if miss_config:
            logging.error("missing parameter " + str(miss_config))
    
    return default_config

config = load_config()