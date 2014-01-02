import os


LOG_FILE_NAME = 'chickens.txt'
SERIAL_PORT = '/dev/ttyAMA0'
API_BASE_URL = 'http://localhost:8000'

if os.environ['USER'] == 'pi':
    API_BASE_URL = 'http://chickens.vegan-oasis.tk'