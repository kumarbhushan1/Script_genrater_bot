import os
import json
import urllib.request
import urllib.error
import time

def generate_video_script(choices):
    api_key = os.environ.get("GEMINI_API_KEY").strip()
    
    # अब हम सिर्फ उसी 1 मॉडल का इस्तेमाल करेंगे जो ज़िंदा है (gemini-2.5-flash)
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
    
    # ज़िद्दी बॉट की सेटिंग (बॉट 5 बार खुद कोशिश करेगा और हर बार ज़्यादा इंतज़ार करेगा)
    max_retries = 5 
    wait_times = [3, 5, 8, 12, 15] # पहले 3 सेकंड रुकेगा, फिर 5, फिर 8...
    
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req) as response:
                result_json = json.loads(response.read().decode('utf-8'))
                return result_json['candidates'][0]['content']['parts'][0]['text']
                
        except urllib.error.HTTPError as e:
            # अगर सर्वर बिज़ी (503) है, तो वहीं रुक कर दोबारा ट्राई करो
            if e.code == 503 and attempt < max_retries - 1:
                time.sleep(wait_times[attempt]) 
                continue
            
            # अगर 45 सेकंड ज़िद्द करने के बाद भी गूगल ना माने
            if e.code == 503:
                return "⏳ माफ़ करें, अभी बहुत सारे लोग स्क्रिप्ट बना रहे हैं। कृपया कुछ मिनट बाद दोबारा प्रयास करें।"
            
            # अगर कोई और एरर आ जाए
            return f"❌ API Error: {e.code}"
            
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(wait_times[attempt])
                continue
            return "❌ सिस्टम में कोई खराबी आ गई है। कृपया बाद में प्रयास करें।"
