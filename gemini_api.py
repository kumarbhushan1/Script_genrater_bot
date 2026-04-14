import os
import json
import urllib.request
import urllib.error
import time

def generate_video_script(choices):
    api_key = os.environ.get("GEMINI_API_KEY").strip()
    
    model = "gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
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
    
    max_retries = 5 
    wait_times = [3, 5, 8, 12, 15] 
    
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req) as response:
                result_json = json.loads(response.read().decode('utf-8'))
                return result_json['candidates'][0]['content']['parts'][0]['text']
                
        except urllib.error.HTTPError as e:
            # फिक्स: अब 503 (सर्वर बिजी) और 429 (लिमिट क्रॉस) दोनों में बॉट इंतज़ार करेगा
            if e.code in [503, 429] and attempt < max_retries - 1:
                time.sleep(wait_times[attempt]) 
                continue
            
            # अगर 45 सेकंड के बाद भी गूगल ना माने
            if e.code in [503, 429]:
                return "⏳ माफ़ करें, अभी Google के सर्वर पर बहुत ट्रैफ़िक है या फ्री लिमिट पूरी हो गई है। कृपया 1 मिनट रुककर दोबारा प्रयास करें।"
            
            return f"❌ API Error: {e.code}"
            
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(wait_times[attempt])
                continue
            return "❌ सिस्टम में कोई खराबी आ गई है। कृपया बाद में प्रयास करें।"
