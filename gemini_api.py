import os
import json
import urllib.request
import urllib.error
import time

def generate_video_script(choices):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "❌ सर्वर एरर: Render पर GROQ_API_KEY सेट नहीं है।"
    api_key = api_key.strip()
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    prompt = f"""
    तुम एक प्रोफेशनल वीडियो और फिल्म डायरेक्टर और स्क्रिप्ट राइटर हो।
    तुम्हारा काम नीचे दिए गए इनपुट के आधार पर एक बहुत ही डिटेल्ड (Detailed) और लंबी वीडियो स्क्रिप्ट तैयार करना है।

    ━━━━━━━━━━━━━━━━━━━━━━━
    🎯 यूज़र इनपुट:
    - वीडियो की भाषा: {choices.get('language')}
    - वीडियो की कैटेगरी: {choices.get('category')}
    - वीडियो का टोन: {choices.get('tone')}
    - टारगेट ऑडियंस: {choices.get('audience')}
    - वीडियो की अवधि: {choices.get('duration')}
    - वीडियो का टॉपिक: {choices.get('topic')}

    ━━━━━━━━━━━━━━━━━━━━━━━
    📌 डायरेक्टर के सख्त निर्देश (Strict Instructions):
    1. यह वीडियो {choices.get('duration')} की है। स्क्रिप्ट बहुत लंबी, डिटेल में और गहराई (Depth) के साथ होनी चाहिए। शॉर्टकट मत मारना।
    2. स्क्रिप्ट को अलग-अलग सीन्स (Scenes) में बाँटो: [Hook], [Intro], [Main Content Parts], [Climax], [Outro]।
    3. हर सीन में मुझे 3 चीज़ें अनिवार्य रूप से चाहिए:
       - 👁️ Visual (स्क्रीन पर क्या दिख रहा है? कैमरा एंगल क्या है?)
       - 🎵 Audio/SFX (बैकग्राउंड म्यूजिक कैसा है? कोई साउंड इफ़ेक्ट है क्या?)
       - 🗣️ Voiceover (होस्ट क्या बोल रहा है?)

    ━━━━━━━━━━━━━━━━━━━━━━━
    🎬 आउटपुट का कड़क फॉर्मेट (इसी फॉर्मेट में जवाब दो):

    🎥 Title: [आकर्षक टाइटल]
    ⏱ Target Duration: {choices.get('duration')}

    --- [Scene 1: Hook (0:00 - 0:30)] ---
    👁️ Visual: [यहाँ विस्तार से बताओ कि स्क्रीन पर क्या दिखेगा]
    🎵 Audio: [म्यूजिक या साउंड इफेक्ट्स]
    🗣️ Voiceover: [यहाँ होस्ट के डायलॉग लिखो - {choices.get('language')} भाषा में]

    --- [Scene 2: Introduction] ---
    👁️ Visual: [...]
    🎵 Audio: [...]
    🗣️ Voiceover: [...]

    (इसी तरह पूरे Main Content, Emotional Peak और Conclusion को बहुत गहराई से विस्तार में लिखो)
    ━━━━━━━━━━━━━━━━━━━━━━━
    अब एक मास्टरपीस स्क्रिप्ट लिखना शुरू करो!
    """
    
    data = {
        "model": "llama-3.3-70b-versatile", 
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 8000  # 🚨 सबसे ज़रूरी फिक्स: बॉट को लंबी स्क्रिप्ट लिखने की आज़ादी देना!
    }
    json_data = json.dumps(data).encode('utf-8')
    
    req = urllib.request.Request(url, data=json_data)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', f'Bearer {api_key}')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36')
    
    max_retries = 3 
    wait_times = [3, 6, 10] 
    
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req) as response:
                result_json = json.loads(response.read().decode('utf-8'))
                return result_json['choices'][0]['message']['content']
                
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries - 1:
                time.sleep(wait_times[attempt]) 
                continue
            try:
                error_msg = json.loads(e.read().decode('utf-8'))
                return f"❌ API Error: {error_msg.get('error', {}).get('message', e.code)}"
            except:
                return f"❌ API Error: {e.code}"
                
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(wait_times[attempt])
                continue
            return f"❌ सिस्टम एरर: {str(e)}"
            
    return "⏳ माफ़ करें, अभी सर्वर बहुत व्यस्त है। कृपया 1 मिनट बाद दोबारा प्रयास करें।"
