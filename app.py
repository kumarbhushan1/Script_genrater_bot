from flask import Flask, request, render_template, redirect, url_for, flash
import telebot
import os
from bot import bot, TOKEN
from database import get_all_scripts, delete_script_by_id

app = Flask(__name__)
app.secret_key = "super_secret_key" # Flash messages के लिए
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
RENDER_URL = os.environ.get("RENDER_URL") # उदाहरण: https://mybot.onrender.com

# 1. Telegram Webhook Route
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

# Webhook सेट करने का URL
@app.route("/set_webhook")
def webhook_setup():
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + '/' + TOKEN)
    return "Webhook is Set!"

# 2. Web Dashboard Route
@app.route('/', methods=['GET'])
def index():
    category_filter = request.args.get('category')
    scripts = get_all_scripts(category_filter)
    return render_template('index.html', scripts=scripts)

# 3. Delete Script Route
@app.route('/delete/<script_id>', methods=['POST'])
def delete_script(script_id):
    password = request.form.get('password')
    if password == ADMIN_PASSWORD:
        delete_script_by_id(script_id)
        flash("Script deleted successfully!", "success")
    else:
        flash("Incorrect Admin Password!", "danger")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
