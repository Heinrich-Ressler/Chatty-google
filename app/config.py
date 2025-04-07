import os
from dotenv import load_dotenv


load_dotenv()

CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', None)
CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', None)
URI_RE = os.environ.get('REDIRECT_URI', None)
