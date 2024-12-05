import google.generativeai as genai
import os
from langchain_google_genai import GoogleGenerativeAI
import logging

logger = logging.getLogger(__name__)

def analyze_financial_data(text, context=None):
    try:
        # Configure the model
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        model = genai.GenerativeModel('gemini-pro')
        
        # Check text length and chunk if necessary
        max_length = 30000  # Adjust this value based on Gemini's limits
        if len(text) > max_length:
            text = text[:max_length] + "..."
        
        # Create the prompt with context if available
        context_info = ""
        if context:
            context_info = f"""
            Organization Context:
            - Employee Size: {context.get('employee_size', 'N/A')}
            - Domain: {context.get('domain', 'N/A')}
            - Main Product: {context.get('main_product', 'N/A')}
            """

        prompt = f"""
        You are a financial analyst. Analyze the following financial document for an organization with these details:

        {context_info}

        Provide a detailed analysis with these sections:

        1. Key Financial Metrics
        - Revenue and growth
        - Profit margins
        - Cash flow
        - Key ratios

        2. Business Health Assessment
        - Overall financial position
        - Market position
        - Risk factors
        - Growth potential

        3. Recommendations
        - Strategic opportunities
        - Areas for improvement
        - Risk mitigation strategies
        - Investment recommendations

        Document text:
        {text}

        Format each section with clear bullet points and specific numbers where available.
        """
        
        # Generate the response
        response = model.generate_content(prompt)
        
        # Process and structure the response
        analysis_text = response.text
        
        # Split the analysis into sections
        sections = {
            'financial_metrics': extract_section(analysis_text, "Key Financial Metrics"),
            'business_health': extract_section(analysis_text, "Business Health Assessment"),
            'recommendations': extract_section(analysis_text, "Recommendations")
        }
        
        return sections
        
    except Exception as e:
        error_message = str(e)
        logger.error(f"Error in Gemini analysis: {error_message}")
        
        if "429" in error_message:
            return {
                'financial_metrics': 'API quota exceeded. Please try again later.',
                'business_health': 'API quota exceeded. Please try again later.',
                'recommendations': 'API quota exceeded. Please try again later.'
            }
        elif "quota" in error_message.lower():
            return {
                'financial_metrics': 'API quota reached. Please try again in a few minutes.',
                'business_health': 'API quota reached. Please try again in a few minutes.',
                'recommendations': 'API quota reached. Please try again in a few minutes.'
            }
        else:
            return {
                'financial_metrics': 'Error analyzing financial metrics',
                'business_health': 'Error analyzing business health',
                'recommendations': 'Error generating recommendations'
            }

def extract_section(text, section_name):
    try:
        # Find the section
        start = text.find(section_name)
        if start == -1:
            return f"No {section_name} found"
            
        # Find the next section or end of text
        next_section = float('inf')
        for section in ["Key Financial Metrics", "Business Health", "Recommendations"]:
            pos = text.find(section, start + len(section_name))
            if pos != -1 and pos < next_section:
                next_section = pos
                
        end = next_section if next_section != float('inf') else len(text)
        
        # Extract and clean the section content
        content = text[start + len(section_name):end].strip()
        return content
        
    except Exception as e:
        logger.error(f"Error extracting section {section_name}: {str(e)}")
        return f"Error processing {section_name}" 