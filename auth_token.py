"""
    Configuration for ChirpStack API
"""

from configparser import RawConfigParser

CFG = RawConfigParser()
CFG.read('config.ini')
API_TOKEN = CFG.get('chirpstack', 'api_token')
AUTH_TOKEN = [("authorization", f"Bearer {API_TOKEN}")]
