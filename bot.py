import logging, os, signal
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.messagehandler import MessageHandler  
Token = "1623948894:AAEPSfMTtW7q9mu96Y-7Ftvdl5JkYtEsj9c"

logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s', level=logging.INFO)
logger = logging.getLogger('SensoresICNBot')

FIRST, SECOND = range(2)
# Callback data
ONE, TWO, THREE, FOUR = range(4)

def start(update,context):
    logger.info('He recibido un comando start')
    name = update.effective_chat.first_name
    text = "¡Hola, " + name + "! 👋👋👋\nSoy el bot del Lab. de Detectores del ICN.\
           \nTe puedo dar las últimas mediciones de los sensores de temperatura y de presión."
    chat_id = update.effective_chat.id
    keyboard(chat_id, text, context)
    
def keyboard(chat_id, text, context):
    kb = [[KeyboardButton("/mediciones")], [KeyboardButton("/temperatura")], [KeyboardButton("/presion")],
          [KeyboardButton("/help")], [KeyboardButton("/faq")] ,[KeyboardButton("/stop")]]
    kb1 = ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_message(chat_id, text, reply_markup=kb1)
    
def stop(update,context):
    logger.info('He recibido un comando stop')
    name = update.effective_chat.first_name
    text = "¡Hasta pronto, " + name + "! 👋👋👋"
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id, text)
    updater.is_idle = False
    os.kill(os.getpid(), signal.SIGINT)   
    
def help1(update,context):
    logger.info('He recibido un comando help')
    text = "Los comandos válidos son los siguientes: \
    \n\nstart - Inicia el bot. \
    \n\nkill - Detiene el bot. \
    \n\nmediciones - Regresa las últimas mediciones de la temperatura y presión.\
    \n\ntemperatura - Regresa el último valor de temperatura de cada sensor.  \
    \n\npresion - Regresa el último valor de presión del sensor. \
    \n\nhelp - Regresa la lista de los comandos y su descripción. \
    \n\nfaq - Preguntas frecuentes."
    chat_id = update.effective_chat.id
    keyboard(chat_id, text, context)

def mediciones(update,context):
    logger.info('He recibico un comando mediciones')
    text= "La últimas mediciones son: \n✅ Temperatura:\n✅ Presión:"
    chat_id = update.effective_chat.id
    keyboard = [[InlineKeyboardButton("Refrescar", callback_data=str(ONE))]]
    context.bot.send_message(chat_id, text, reply_markup=InlineKeyboardMarkup(keyboard))
    
def temperatura(update,context):
    logger.info('He recibico un comando temperatura')
    text= "La última medición de la temperatura es: \n🌡"
    chat_id = update.effective_chat.id
    keyboard = [[InlineKeyboardButton("Refrescar", callback_data=str(ONE))]]
    context.bot.send_message(chat_id, text, reply_markup=InlineKeyboardMarkup(keyboard))
    
def presion(update,context):
    logger.info('He recibico un comando presión')
    text= "La última medición de la presión es: \n💨"
    chat_id = update.effective_chat.id
    keyboard = [[InlineKeyboardButton("Refrescar", callback_data=str(ONE))]]
    context.bot.send_message(chat_id, text, reply_markup=InlineKeyboardMarkup(keyboard))
    
def faq(update,context):
    logger.info('He recibido un comando faq')
    name = update.effective_chat.first_name
    text = "Lo siento, " + name + ".\nEse no es un comando válido. 😓😓" 
    chat_id = update.effective_chat.id
    keyboard(chat_id, text, context)

def unknown(update,context):
    logger.info('He recibido un comando inválido')
    name = update.effective_chat.first_name
    text = "Lo siento, " + name + ".\nEse no es un comando válido. 😓😓" 
    chat_id = update.effective_chat.id
    keyboard(chat_id, text, context)

if __name__ == '__main__':
    updater = Updater(token=Token, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('kill', stop))
    dispatcher.add_handler(CommandHandler('help', help1))
    dispatcher.add_handler(CommandHandler('mediciones', mediciones))
    dispatcher.add_handler(CommandHandler('temperatura', temperatura))
    dispatcher.add_handler(CommandHandler('presion', presion))
    dispatcher.add_handler(CommandHandler('faq', faq))
      
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    
    updater.start_polling()
    updater.idle()    