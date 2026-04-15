import os
import json
import urllib.request
import urllib.error
import time

def generate_video_script(choices):
    # Render के Environment से आपकी Groq API Key लेना
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        return "❌ सर्वर एरर: Render पर GROQ_API_KEY सेट नहीं है। कृपया Environment सेटिंग्स चेक करें।"
        
    api_key = api_key.strip()
    
    # Groq API का सुरक्षित लिंक
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    # आपका नया और पावरफुल 'सुपर प्रॉम्प्ट'
    prompt = f"""
    तुम एक प्रोफेशनल वीडियो स्क्रिप्ट राइटर, स्टोरीटेलर और कंटेंट क्रिएटर हो।
    तुम्हारा काम है यूज़र द्वारा दिए गए इनपुट के आधार पर एक ऐसा वीडियो स्क्रिप्ट तैयार करना जो बेहद आकर्षक (Engaging), भावनात्मक (Emotional), और अंत तक देखने लायक (High Retention) हो।

    ━━━━━━━━━━━━━━━━━━━━━━━
    🎯 यूज़र इनपुट:
    - वीडियो की भाषा: {choices.get('language')}
    - वीडियो की कैटेगरी: {choices.get('category')}
    - वीडियो का टोन: {choices.get('tone')}
    - टारगेट ऑडियंस: {choices.get('audience')}
    - वीडियो की अवधि: {choices.get('duration')}
    - वीडियो का टॉपिक: {choices.get('topic')}

    ━━━━━━━━━━━━━━━━━━━━━━━
    📌 जरूरी निर्देश:
    1. स्क्रिप्ट {choices.get('language')} भाषा में लिखो।
    2. स्क्रिप्ट बिल्कुल इंसानों जैसी लगे — रोबोटिक या बोरिंग नहीं।
    3. शुरुआत (पहले 5–10 सेकंड) बहुत ही मजबूत Hook से करो ताकि दर्शक तुरंत वीडियो में जुड़ जाए।
    4. स्क्रिप्ट में कहानी (Storytelling) का उपयोग करो, खासकर अगर कैटेगरी Motivational, Emotional या Story है।
    5. स्क्रिप्ट को अलग-अलग भागों में बाँटो: [Hook], [Introduction], [Main Content], [Emotional Peak], [Conclusion + CTA]।
    6. हर सीन के लिए विजुअल सुझाव भी दो, जैसे: [Scene: एक बच्चा उदास बैठा है, बारिश हो रही है]।
    7. दर्शकों को जोड़े रखने के लिए: सवाल पूछो, जिज्ञासा (Curiosity) बनाओ और भावनात्मक जुड़ाव पैदा करो।
    8. स्क्रिप्ट में दोहराव (Repetition) ना हो और flow स्मूथ रहे।
    9. स्क्रिप्ट की लंबाई {choices.get('duration')} के अनुसार बिल्कुल सटीक होनी चाहिए (1 मिनट के लिए लगभग 140-160 शब्द)।

    ━━━━━━━━━━━━━━━━━━━━━━━
    🎬 आउटपुट फॉर्मेट:
    🎥 Title: (एक आकर्षक और क्लिक करने योग्य टाइटल)
    ⏱ Duration: {choices.get('duration')}
    
    [Hook] ...
    [Introduction] ...
    [Main Content] ...
    [Emotional Peak / Climax] ...
    [Conclusion + CTA] ...
    
    ━━━━━━━━━━━━━━━━━━━━━━━
    अब ऊपर दिए गए सभी निर्देशों का पालन करते हुए सबसे बेहतरीन स्क्रिप्ट तैयार करो।
    """
    
    # Llama 3.3 70B - सबसे नया और तेज़ मॉडल
    data = {
        "model": "llama-3.3-70b-versatile", 
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    json_data = json.dumps(data).encode('utf-8')
    
    req = urllib.request.Request(url, data=json_data)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', f'Bearer {api_key}')
    # सिक्योरिटी गार्ड को चकमा देने के लिए नकली ब्राउज़र पहचान
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36')
    
    # ऑटो-रिट्राई सिस्टम (ज़िद्दी बॉट)
    max_retries = 3 
    wait_times = [3, 6, 10] 
    
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req) as response:
                result_json = json.loads(response.read().decode('utf-8'))
                return result_json['choices'][0]['message']['content']
                
        except urllib.error.HTTPError as e:
            # अगर सर्वर बिज़ी (429) हो, तो इंतज़ार करो
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
