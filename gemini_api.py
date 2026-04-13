import os
import google.generativeai as genai

def generate_video_script(choices):
    # API Key को सुरक्षित तरीके से लेना
api_key = os.environ.get("GEMINI_API_KEY").strip()
    genai.configure(api_key=api_key)
    
    # Gemini का नया और तेज़ मॉडल
    model = genai.GenerativeModel('gemini-1.5-flash')
    
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
    
    # स्क्रिप्ट जेनरेट करना
    response = model.generate_content(prompt)
    return response.text
