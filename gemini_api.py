import os
import google.generativeai as genai

def generate_video_script(choices):
    try:
        # API Key को सुरक्षित तरीके से लेना
        api_key = os.environ.get("GEMINI_API_KEY").strip()
        genai.configure(api_key=api_key)
        
        prompt = f"""
        You are an expert video script writer. Write a highly engaging video script based on the following details:
        - Language: {choices.get('language')}
        - Video Format: {choices.get('format')}
        - Category: {choices.get('category')}
        - Tone: {choices.get('tone')}
        - Target Audience: {choices.get('audience')}
        - Duration: {choices.get('duration')}
        - Topic: {choices.get('topic')}
        """
        
        try:
            # पहली कोशिश
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            try:
                # दूसरी कोशिश
                fallback_model = genai.GenerativeModel('gemini-pro')
                response = fallback_model.generate_content(prompt)
                return response.text
            except Exception as fallback_error:
                # अब बॉट असली एरर टेलीग्राम पर ही भेज देगा!
                return f"❌ Error 1 (Flash): {str(e)}\n\n❌ Error 2 (Pro): {str(fallback_error)}"
                
    except Exception as setup_error:
        return f"❌ Setup Error: {str(setup_error)}"
