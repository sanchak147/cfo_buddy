import PyPDF2
from werkzeug.utils import secure_filename
import os

def process_pdfs(files):
    try:
        all_text = ""
        
        for filepath in files:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page in pdf_reader.pages:
                    all_text += page.extract_text() + "\n\n"
        
        return all_text
        
    except Exception as e:
        logger.error(f"Error processing PDFs: {str(e)}")
        return ""