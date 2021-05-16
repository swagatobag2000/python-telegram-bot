import logging

from flask import Flask, request
from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, Dispatcher, CallbackContext
from utils import get_reply, fetch_news, topics_keyboard

# enable logging
# logging: any kind of error happen or warning is raised, so this is used to parse it in a systematic manner 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level = logging.INFO)
# logger object can create logs for your program
logger = logging.getLogger(__name__)

TOKEN = "1842902902:AAHXMq7cs0v8DnBIgQNuAHX13J8eyFf7Vo0"
app = Flask (__name__)

@app.route('/')
def index():
	return "Hello!"

@app.route(f'/{TOKEN}', methods=['GET', 'POST'])
def webhook():
    """webhook view which receives updates from telegram"""
    # create update object from json-format request data
    update = Update.de_json(request.get_json(), bot)
    # process update
    dp.process_update(update)
    return "ok"

def greeting(update: Update,context: CallbackContext):
    first_name = update.to_dict()['message']['chat']['first_name']
    update.message.reply_text("Hi {}".format(first_name))

def _help(update: Update,context: CallbackContext):
	help_text = "Hey!, This is a help text"
	update.message.reply_text(text  = help_text)

def news(update: Update,context: CallbackContext):
	update.message.reply_text(text  = "Choose a Category", reply_markup = ReplyKeyboardMarkup(keyboard = topics_keyboard, one_time_keyboard = True))

def message_handler(update: Update,context: CallbackContext):
    """callback function for text message handler"""
    intent, reply = get_reply(update.message.text, update.message.chat_id)
    if intent == "get_news":
        articles = fetch_news(reply)
        for article in articles:
            update.message.reply_text(text=article['link'])
    else:
        update.message.reply_text(text=reply)

def echo_sticker(bot,update):
	bot.send_sticker(chat_id=update.message.chat_id , sticker=update.message.sticker.file_id)

def error(bot, update):
	logger.error("Update %s caused error %s",update,update.error)


# Create Updater
# updator will keep polling and receive the updates from telegram and move it to the dispatcher
bot = Bot(TOKEN)
try:
	bot.set_webhook("https://protected-fjord-75558.herokuapp.com/" + TOKEN)
except Exception as e:
	print(e)

# Create dispatcher
# dispatcher handles those updates
# all the response will be handled
dp = Dispatcher(bot, None)

# Add Handlers
# dispatcher needs multiple handlers
# former start is for: if the user writes / with start then it will call the start(latter) function
dp.add_handler(CommandHandler("start",greeting))
dp.add_handler(CommandHandler("help",_help))
dp.add_handler(CommandHandler("news",news))
# messageHandler class is for handling stickers and other text and if the msg is in text form user .text
dp.add_handler(MessageHandler(Filters.text,message_handler))
dp.add_handler(MessageHandler(Filters.sticker,echo_sticker))
dp.add_error_handler(error)

if __name__ == '__main__':
	app.run(port = 8443)