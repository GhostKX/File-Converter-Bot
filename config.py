from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()
API_KEY = str(os.getenv('API_KEY'))
