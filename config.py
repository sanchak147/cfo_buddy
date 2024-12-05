import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Base directory of the project
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Heroku-specific configuration
    UPLOAD_FOLDER = '/tmp'  # Use Heroku's temporary filesystem
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB file size limit
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Environment variables
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Add these configurations for handling large files
    REQUEST_CHUNK_SIZE = 8 * 1024 * 1024    # 8MB chunks

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    # Production specific settings
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

# Dictionary to map config names to config classes
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 

if not os.getenv('GOOGLE_API_KEY'):
    raise ValueError("GOOGLE_API_KEY environment variable is not set") 