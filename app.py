from flask import Flask, render_template
from api.routes import api_bp
from config import Config
import os
from flask_cors import CORS
import logging

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Configure logging for Render
if os.environ.get('RENDER'):
    # Use Render's tmp directory and configure for production
    app.config.update(
        UPLOAD_FOLDER='/tmp',
        MAX_CONTENT_LENGTH=100 * 1024 * 1024,  # 100MB limit
        DEBUG=False,  # Disable debug mode in production
        TEMPLATES_AUTO_RELOAD=False  # Disable template auto-reload
    )
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

# Health check endpoint for Render
@app.route('/health')
def health_check():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    # Only enable debug mode during local development
    debug_mode = not os.environ.get('RENDER')
    app.run(debug=debug_mode)