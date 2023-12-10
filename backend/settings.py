import os
from dotenv import load_dotenv


load_dotenv()

IMAGE_FOLDER = 'images'
STATIC_ROOT = 'static'
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))