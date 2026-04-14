import os
import json
import urllib.request
import urllib.error
import time

def generate_video_script(choices):
    # Render से आपकी नई Groq चाबी लेना
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    
    # अगर आपने पुरानी जगह (GEMINI_API_KEY) ही पेस्ट कर दिया हो, तो वहां से उठा लेगा
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    # Groq API का मेन दरवाज़ा
    url = "https://api.groq.com/openai/v1/chat/completions"
    
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
    
    # Meta का सबसे पावरफुल और स्मार्ट फ्री मॉडल (Llama 3 70B)
    data = {
        "model": "llama3-70b-8192", 
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    json_data = json.dumps(data).encode('utf-8')
    
    # रिक्वेस्ट बनाना
    req = urllib.request.Request(url, data=json_data)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', f'Bearer {api_key}')
    
    # ऑटो-रिट्राई (अगर कभी 1% चांस में सर्वर बिज़ी हो)
    max_retries = 3 
    wait_times = [2, 4, 6] 
    
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req) as response:
                result_json = json.loads(response.read().decode('utf-8'))
                # स्क्रिप्ट निकालकर भेजना
                return result_json['choices'][0]['message']['content']
                
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries - 1:
                time.sleep(wait_times[attempt]) 
                continue
            
            # अगर एरर आए तो उसका असली कारण निकालो
            try:
                error_msg = json.loads(e.read().decode('utf-8'))
                return f"❌ API Error: {error_msg.get('error', {}).get('message', e.code)}"
            except:
                return f"❌ API Error: {e.code}"
                
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(wait_times[attempt])
                continue
            return "❌ सिस्टम में कोई खराबी आ गई है। कृपया बाद में प्रयास करें।"
            
    return "⏳ माफ़ करें, अभी सर्वर बहुत व्यस्त है। कृपया 1 मिनट बाद दोबारा प्रयास करें।"
