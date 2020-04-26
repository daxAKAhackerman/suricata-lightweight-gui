from dotenv import load_dotenv

import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SURICATA_EVE_FILE = os.environ.get('SURICATA_EVE_FILE') or os.path.join(basedir, 'eve.json')