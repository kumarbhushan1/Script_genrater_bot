import os
import google.generativeai as genai

def generate_video_script(choices):
    # API Key को सुरक्षित तरीके से लेना
    api_key = os.environ.get("GEMINI_API_KEY").strip()
    genai.configure(api_key=api_key)
    
    # AI के लिए निर्देश (Prompt) तैयार करना
    prompt = f"""
    You are an expert video script writer. Write a highly engaging video script based on the following details:
    - Language: {choices.get('language')}
    - Video Format: {choices.get('format')}
    - Category: {choices.get('category')}
    - Tone: {choices.get('tone')}
    - Target Audience: {choices.get('audience')}
    - Duration: {choices.get('duration')}
    - Topic: {choices.get('topic')}
    
    Provide the output clearly with Title, Intro, Body/Scenes, and Outro.
    """
    
    try:
        # पहली कोशिश: सबसे तेज़ और नए मॉडल (gemini-1.5-flash) के साथ
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"Primary model failed: {e}. Switching to backup...")
        
        try:
            # दूसरी कोशिश (Backup Plan): अगर पहला फेल हो जाए तो 'gemini-pro' इस्तेमाल करें
            fallback_model = genai.GenerativeModel('gemini-pro')
            response = fallback_model.generate_content(prompt)
            return response.text
            
        except Exception as fallback_error:
            # अगर दोनों मॉडल फेल हो जाएँ
            return f"माफ़ करें, अभी Google के सर्वर बहुत व्यस्त हैं। कृपया कुछ देर बाद दोबारा प्रयास करें।"
