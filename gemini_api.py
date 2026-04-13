import os
import json
import urllib.request
import urllib.error
import time

def generate_video_script(choices):
    api_key = os.environ.get("GEMINI_API_KEY").strip()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
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
    
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})
    
    max_retries = 3 # बॉट 3 बार खुद कोशिश करेगा
    
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req) as response:
                result_json = json.loads(response.read().decode('utf-8'))
                return result_json['candidates'][0]['content']['parts'][0]['text']
                
        except urllib.error.HTTPError as e:
            # अगर 503 (सर्वर बिजी) एरर आए, तो 3 सेकंड रुक कर दोबारा ट्राई करो
            if e.code == 503 and attempt < max_retries - 1:
                time.sleep(3) 
                continue
            
            error_message = e.read().decode('utf-8')
            return f"❌ API Error: {e.code} - {error_message}"
            
        except Exception as e:
            # सिस्टम की कोई और दिक्कत हो तब भी एक बार ट्राई करो
            if attempt < max_retries - 1:
                time.sleep(3)
                continue
            return f"❌ System Error: {str(e)}"
