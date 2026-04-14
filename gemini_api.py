import os
import json
import urllib.request
import urllib.error
import time

def generate_video_script(choices):
    api_key = os.environ.get("GEMINI_API_KEY").strip()
    
    # 3 पावरफुल मॉडल्स की सेना (अगर एक फेल हुआ, तो बॉट तुरंत दूसरे पर जाएगा)
    models = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-8b", # Google का नया हल्का मॉडल, जो बहुत तेज़ है और कम बिज़ी रहता है
        "gemini-1.0-pro"       # पुराना लेकिन बहुत भरोसेमंद मॉडल
    ]
    
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
    
    # बॉट हर मॉडल को बारी-बारी चेक करेगा
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})
        
        # हर मॉडल से 2 बार रिक्वेस्ट करेगा
        for attempt in range(2):
            try:
                with urllib.request.urlopen(req) as response:
                    result_json = json.loads(response.read().decode('utf-8'))
                    return result_json['candidates'][0]['content']['parts'][0]['text']
                    
            except urllib.error.HTTPError as e:
                # अगर मॉडल बिज़ी है (503) या लिमिट फुल है (429)
                if e.code in [503, 429]:
                    time.sleep(2) # 2 सेकंड रुको और उसी मॉडल पर दोबारा ट्राई करो
                    continue 
                # अगर कोई और एरर है (जैसे 404), तो तुरंत लूप तोड़ो और अगला नया मॉडल ट्राई करो
                break 
            except Exception:
                time.sleep(2)
                continue
                
    # अगर तीनों मॉडल और उनके सारे प्रयास फेल हो जाएं (जो कि बहुत ही कम होगा)
    return "⏳ माफ़ करें, अभी बहुत सारे यूज़र्स एक साथ स्क्रिप्ट बना रहे हैं। कृपया 1 मिनट बाद दोबारा प्रयास करें।"
