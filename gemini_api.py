import os
import json
import urllib.request
import urllib.error

def generate_video_script(choices):
    api_key = os.environ.get("GEMINI_API_KEY").strip()
    
    # हम सारे संभावित मॉडल्स को एक साथ चेक करेंगे
    models = [
        "gemini-2.5-flash", 
        "gemini-1.5-flash",
        "gemini-pro"
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
    """
    
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    json_data = json.dumps(data).encode('utf-8')
    
    error_logs = []
    
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})
        
        try:
            with urllib.request.urlopen(req) as response:
                result_json = json.loads(response.read().decode('utf-8'))
                return result_json['candidates'][0]['content']['parts'][0]['text']
                
        except urllib.error.HTTPError as e:
            try:
                # गूगल का असली मैसेज निकाल रहे हैं
                error_message = json.loads(e.read().decode('utf-8')).get('error', {}).get('message', 'Unknown Error')
            except:
                error_message = e.read().decode('utf-8')
            error_logs.append(f"❌ {model}: {e.code} - {error_message}")
            
        except Exception as e:
            error_logs.append(f"❌ {model}: System Error - {str(e)}")
            
    # अगर तीनों फेल हों, तो टेलीग्राम पर पूरी रिपोर्ट भेजो
    return "⏳ असली एरर रिपोर्ट:\n\n" + "\n\n".join(error_logs)
