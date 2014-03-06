import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
FILEPATH = os.path.join(BASE_DIR,'..')

SUBJECT = "Upload Verification Mail"
MESSAGE = "Please click the below link to verify your email address"
FROM = "Upload-Admin@gmail.com"

URL = "http://nirav-desktop.lan.coriolis.co.in:8000/upload/"
