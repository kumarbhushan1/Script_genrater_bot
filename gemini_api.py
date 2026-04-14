import os
import json
import urllib.request
import urllib.error
import time

def generate_video_script(choices):
    api_key = os.environ.get("GEMINI_API_KEY").strip()
    
    # गूगल का नया लाइव मॉडल
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
    
    # परमानेंट फिक्स: बॉट अब 5 बार ट्राई करेगा और हर बार ज़्यादा इंतज़ार करेगा
    max_retries = 5 
    wait_times = [3, 6, 10, 15, 20] # Exponential Backoff
    
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req) as response:
                result_json = json.loads(response.read().decode('utf-8'))
                return result_json['candidates'][0]['content']['parts'][0]['text']
                
        except urllib.error.HTTPError as e:
            # अगर सर्वर बिजी है (503) या लिमिट क्रॉस हो गई (429)
            if e.code in [503, 429] and attempt < max_retries - 1:
                time.sleep(wait_times[attempt]) # लिस्ट के हिसाब से रुकेगा और फिर ट्राई करेगा
                continue
            
            # अगर 1 मिनट ज़िद्द करने के बाद भी गूगल ना माने
            if attempt == max_retries - 1:
                return "⏳ माफ़ करें, Google के सर्वर इस समय बहुत अधिक व्यस्त हैं। बॉट ने कई बार कोशिश की है। कृपया कुछ मिनट बाद दोबारा कोशिश करें।"
            
            return "❌ माफ़ करें, स्क्रिप्ट बनाते समय पीछे से कोई तकनीकी समस्या आ गई है। कृपया कुछ देर बाद कोशिश करें।"
            
        except Exception as e:
            # इंटरनेट या सिस्टम की कोई और दिक्कत हो तब भी ट्राई करो
            if attempt < max_retries - 1:
                time.sleep(wait_times[attempt])
                continue
            return "❌ सिस्टम में कोई खराबी आ गई है। कृपया बाद में प्रयास करें।"
