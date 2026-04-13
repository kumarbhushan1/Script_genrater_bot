import os
import json
import urllib.request
import urllib.error

def generate_video_script(choices):
    # API Key लेना
    api_key = os.environ.get("GEMINI_API_KEY").strip()
    
    # गूगल का नया लाइव मॉडल (gemini-2.5-flash)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    # AI के लिए निर्देश
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
    
    # Google को भेजने के लिए डेटा का पैकेट बनाना
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    json_data = json.dumps(data).encode('utf-8')
    
    # रिक्वेस्ट भेजना
    req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})
    
    try:
        # Google से सीधा जवाब लेना
        with urllib.request.urlopen(req) as response:
            result_json = json.loads(response.read().decode('utf-8'))
            return result_json['candidates'][0]['content']['parts'][0]['text']
            
    except urllib.error.HTTPError as e:
        error_message = e.read().decode('utf-8')
        return f"❌ API Error: {e.code} - {error_message}"
    except Exception as e:
        return f"❌ System Error: {str(e)}"
