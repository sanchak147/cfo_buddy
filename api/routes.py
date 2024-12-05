from flask import Blueprint, request, jsonify, current_app
from services.pdf_processor import process_pdfs
from services.gemini_service import analyze_financial_data
import os
import logging
from werkzeug.utils import secure_filename
import uuid

api_bp = Blueprint('api', __name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_bp.route('/upload', methods=['POST'])
def upload():
    try:
        # Retrieve form data
        employee_size = request.form.get('employee_size')
        domain = request.form.get('domain')
        main_product = request.form.get('main_product')

        # Check if employee_size is None
        if employee_size is None:
            raise ValueError("Employee size is not provided")

        # Use Render's tmp directory
        UPLOAD_FOLDER = '/tmp'
        
        # Process files
        files = request.files.getlist('files[]')
        processed_files = []
        
        for file in files:
            if file and allowed_file(file.filename):
                # Create unique filename
                filename = secure_filename(str(uuid.uuid4()) + '_' + file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                processed_files.append(filepath)
            else:
                logger.error(f"Invalid file type for file: {file.filename}")
                return jsonify({
                    'status': 'error',
                    'message': f'Invalid file type. Only PDF files are allowed.'
                }), 400

        # Extract text from PDFs
        logger.debug("Extracting text from PDFs")
        extracted_text = process_pdfs(processed_files)
        logger.debug(f"Extracted text length: {len(extracted_text) if extracted_text else 0}")
        
        # Analyze the extracted text using Gemini
        logger.debug("Starting Gemini analysis")
        analysis_result = analyze_financial_data(
            extracted_text, 
            context={
                'employee_size': employee_size,
                'domain': domain,
                'main_product': main_product
            }
        )
        
        logger.debug(f"Analysis result structure: {analysis_result}")
        
        # Check for quota errors
        if 'quota' in str(analysis_result.get('financial_metrics', '')).lower():
            return jsonify({
                'status': 'error',
                'message': 'API quota exceeded. Please try again later.'
            }), 429
        
        logger.debug(f"Analysis result: {analysis_result}")
        
        # Clean up uploaded files
        for filepath in processed_files:
            try:
                os.remove(filepath)
                logger.debug(f"Removed temporary file: {filepath}")
            except Exception as e:
                logger.warning(f"Failed to remove temporary file {filepath}: {str(e)}")

        response_data = {
            'status': 'success',
            'analysis': {
                'financial_metrics': analysis_result.get('financial_metrics', 'No financial metrics available'),
                'business_health': analysis_result.get('business_health', 'No business health analysis available'),
                'recommendations': analysis_result.get('recommendations', 'No recommendations available')
            }
        }
        logger.debug(f"Sending response: {response_data}")
        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error in upload: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500