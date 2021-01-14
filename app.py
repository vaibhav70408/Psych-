import logging
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from telegram import Bot, Update, ReplyKeyboardMarkup
from addon import get_reply,topics_keyboard,topics_keyboard1

dict={'Bipolar Disorder':"Bipolar disorder is a mental illness marked by extreme shifts in mood. Symptoms can include an extremely elevated mood called mania. They can also include episodes of depression. Bipolar disorder is also known as bipolar disease or manic depression.", 
'Depression': "Depression (major depressive disorder) is a common and serious medical illness that negatively affects how you feel, the way you think and how you act. Fortunately, it is also treatable. Depression causes feelings of sadness and/or a loss of interest in activities you once enjoyed.",
'Panic attack':"A panic attack is a sudden episode of intense fear that triggers severe physical reactions when there is no real danger or apparent cause. Panic attacks can be very frightening. When panic attacks occur, you might think you're losing control, having a heart attack or even dying." , 
'OCD':"Obsessive-compulsive disorder (OCD) is a disorder in which people have recurring, unwanted thoughts, ideas or sensations (obsessions) that make them feel driven to do something repetitively (compulsions). The repetitive behaviors, such as hand washing, checking on things or cleaning, can significantly interfere with a person’s daily activities and social interactions",
'Dyslexia': "Dyslexia is a specific learning disability that is neurobiological in origin. It is characterized by difficulties with accurate and/or fluent word recognition and by poor spelling and decoding abilities. These difficulties typically result from a deficit in the phonological component of language that is often unexpected in relation to other cognitive abilities and the provision of effective classroom instruction.",
'Schizophrenia':"Schizophrenia is a chronic brain disorder that affects less than one percent of the U.S. population. When schizophrenia is active, symptoms can include delusions, hallucinations, disorganized speech, trouble with thinking and lack of motivation. However, with treatment, most symptoms of schizophrenia will greatly improve and the likelihood of a recurrence can be diminished."
	
}

dict1={"Games":"https://assistant.google.com/services/a/uid/0000007823a4a6b9?hl=en-US&hl=en-IN&jsmode=o&source=web",
'Music': "https://youtu.be/j5-yKhDd64s",
'Fun Facts':"That tiny pocket in jeans was designed to store pocket watches. The original jeans only had four pockets: that tiny one, plus two more on the front and just one in the back." , 
'Quotes':"shorturl.at/tAWZ8"

}

# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# telegram bot token
TOKEN = "1522920050:AAEDn1QvYUzemQkL8vZgEoe9MQs6p4HrtN0"

app = Flask(__name__)


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


def start(bot, update):
    #to get name of author (the person who is using the bot)
	author=update.message.from_user.first_name
	#generating the reply user will recieve
	reply= "Hey! {}".format(author) +"\n"+"Mental Health Awareness Bot welcomes you."+"\n"+" Type '/info' command to get information about mental disorders"
	#to send text to the user ud need chat id and it will be sent via bot argument
	bot.send_message(chat_id=update.message.chat_id,text=reply)


def _help(bot, update):
    """callback function for /help handler"""
    help_txt = "Hey! I am there to help you out."
    bot.send_message(chat_id=update.message.chat_id, text=help_txt)
    bot.send_message(chat_id=update.message.chat_id, text="Choose a category",
                     reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard1, one_time_keyboard=True))


def reply_text(bot, update):
    """callback function for text message handler"""
    intent, reply = get_reply(update.message.text, update.message.chat_id)
    
    if update.message.text in dict:
        bot.send_message(chat_id=update.message.chat_id, text=dict[update.message.text])
        reply= " Choose another category or Type '/help' command if you are feeling low"
        bot.send_message(chat_id=update.message.chat_id,text=reply)
    elif  update.message.text in dict1:
        bot.send_message(chat_id=update.message.chat_id, text=dict1[update.message.text])
    else:
        bot.send_message(chat_id=update.message.chat_id,text=reply)

def info(bot, update):
    """callback function for /news handler"""
    bot.send_message(chat_id=update.message.chat_id, text="Choose a category",
                     reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard, one_time_keyboard=True))

def echo_sticker(bot, update):
    """callback function for sticker message handler"""
    bot.send_sticker(chat_id=update.message.chat_id,
                     sticker=update.message.sticker.file_id)


def error(bot, update,telegramError):
    """callback function for error handler"""
    logger.error("Update '%s' caused error '%s'", update,telegramError )

bot = Bot(TOKEN)
try:
    bot.set_webhook("https://pshych121.herokuapp.com/" + TOKEN)
except Exception as e:
    print(e)
dp = Dispatcher(bot, None)
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", _help))
dp.add_handler(CommandHandler("info",info))
dp.add_handler(MessageHandler(Filters.text, reply_text))
dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
dp.add_error_handler(error)
        
        
   
    
if __name__ == "__main__":    
    app.run(port=8443)
