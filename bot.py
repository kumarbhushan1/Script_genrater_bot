import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from gemini_api import generate_video_script
from database import save_script

# खाली स्पेस हटाने और थ्रेडिंग बंद करने के लिए
TOKEN = os.environ.get("TELEGRAM_TOKEN").strip()
bot = telebot.TeleBot(TOKEN, threaded=False)

# यूज़र के जवाब सेव करने के लिए एक डिक्शनरी
user_data = {}

# कीबोर्ड बनाने का एक छोटा फंक्शन
def make_keyboard(options, step_name):
    markup = InlineKeyboardMarkup()
    for option in options:
        markup.add(InlineKeyboardButton(option, callback_data=f"{step_name}:{option}"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_data[chat_id] = {} # नया डेटा शुरू करें
    bot.reply_to(message, "नमस्ते! मैं आपका वीडियो स्क्रिप्ट जनरेटर बॉट हूँ। आइए शुरू करते हैं!")
    
    options = ["Hindi", "English", "Hinglish"]
    bot.send_message(chat_id, "सबसे पहले, अपनी वीडियो की भाषा (Language) चुनें:", reply_markup=make_keyboard(options, 'language'))

# बटनों (Popups) के क्लिक को हैंडल करना
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    data = call.data.split(':')
    step = data[0]
    choice = data[1]
    
    user_data[chat_id][step] = choice
    
    # एक के बाद एक सवाल पूछने का लॉजिक
    if step == 'language':
        options = ["YouTube Long", "YouTube Shorts", "Instagram Reels"]
        bot.edit_message_text("वीडियो का फॉर्मेट क्या होगा?", chat_id, call.message.message_id, reply_markup=make_keyboard(options, 'format'))
    
    elif step == 'format':
        options = ["Education", "Comedy", "Tech", "Vlog", "Motivation"]
        bot.edit_message_text("वीडियो की कैटेगरी चुनें:", chat_id, call.message.message_id, reply_markup=make_keyboard(options, 'category'))
    
    elif step == 'category':
        options = ["Funny", "Serious", "Professional", "Casual"]
        bot.edit_message_text("वीडियो का टोन कैसा होना चाहिए?", chat_id, call.message.message_id, reply_markup=make_keyboard(options, 'tone'))
    
    elif step == 'tone':
        options = ["Kids", "Teens", "Adults", "Everyone"]
        bot.edit_message_text("आपकी टारगेट ऑडियंस कौन है?", chat_id, call.message.message_id, reply_markup=make_keyboard(options, 'audience'))
    
    elif step == 'audience':
        options = ["1 Min", "3 Mins", "5 Mins", "10+ Mins"]
        bot.edit_message_text("वीडियो की लंबाई कितनी होगी?", chat_id, call.message.message_id, reply_markup=make_keyboard(options, 'duration'))
        
    elif step == 'duration':
        bot.edit_message_text("शानदार! अब अंत में, मुझे अपनी **वीडियो का टॉपिक** लिखकर मैसेज करें:", chat_id, call.message.message_id)
        # अब हम यूज़र के टेक्स्ट मैसेज का इंतज़ार करेंगे
        bot.register_next_step_handler(call.message, get_topic_and_generate)

import threading

def get_topic_and_generate(message):
    chat_id = message.chat.id
    user_data[chat_id]['topic'] = message.text
    
    bot.send_message(chat_id, "⏳ कृपया प्रतीक्षा करें, मैं आपकी स्क्रिप्ट लिख रहा हूँ (इसमें 30-40 सेकंड लग सकते हैं)...")
    bot.send_chat_action(chat_id, 'typing')
    
    # यह फंक्शन बैकग्राउंड में काम करेगा ताकि सर्वर क्रैश न हो
    def process_script_in_background():
        try:
            # Gemini से स्क्रिप्ट लेना
            script = generate_video_script(user_data[chat_id])
            
            # यूज़र को टेलीग्राम पर भेजना
            bot.send_message(chat_id, f"✅ आपकी स्क्रिप्ट तैयार है:\n\n{script}")
            
            # डेटाबेस में सेव करना
            user_name = message.from_user.first_name
            username = message.from_user.username
            save_script(user_name, chat_id, username, user_data[chat_id], script)
            
        except Exception as e:
            bot.send_message(chat_id, f"माफ़ करें, कोई एरर आ गई: {str(e)}")

    # बैकग्राउंड थ्रेड (Thread) चालू करना
    thread = threading.Thread(target=process_script_in_background)
    thread.start()
