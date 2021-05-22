import logging, os, signal
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, keyboardbutton
from telegram.ext.messagehandler import MessageHandler  
from Auxiliares import Medidas
Token = "1623948894:AAEPSfMTtW7q9mu96Y-7Ftvdl5JkYtEsj9c"

logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s', level=logging.INFO)
logger = logging.getLogger('SensoresICNBot')

a='Temperatura135.txt'
b='TemperaturaM.txt'
c='Presion.csv'

meds=Medidas(a,b,c)
d1, d2, d3, d4, c5, c6, ca, cb, pf = meds

def start(update,context):
    logger.info('He recibido un comando start')
    name = update.effective_chat.first_name
    text = "¡Hola, " + name + "! 👋👋👋\n\nSoy el bot 🤖 del Lab. de Detectores del ICN.\
           \n\nTe puedo dar las últimas mediciones de los sensores de temperatura y de presión."
    chat_id = update.effective_chat.id
    keyboard(chat_id, text, context)
    
def keyboard(chat_id, text, context):
    kb = [[KeyboardButton("/mediciones")], [KeyboardButton("/temperatura")], [KeyboardButton("/presion")],
          [KeyboardButton("/help"), KeyboardButton("/config")], [KeyboardButton("/kill")]]
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
    \n\nmediciones - Regresa las últimas mediciones de la temperatura y presión de los distintos sensores.\
    \n\ntemperatura - Regresa el último valor de temperatura de cada sensor.  \
    \n\npresion - Regresa el último valor de presión del sensor. \
    \n\nconfig - Configuraciones del bot.\
    \n\nhelp - Regresa la lista de los comandos y su descripción."
    chat_id = update.effective_chat.id
    keyboard(chat_id, text, context)

def mediciones(update,context):
    logger.info('He recibido un comando mediciones')
    text= "La últimas mediciones son: \n \
        \n🌡 Temperatura:\n" + d1 + d2 + d3 + d4 + c5 + c6 + ca + cb + "\n \n💨 Presión: \n" + pf
    chat_id = update.effective_chat.id
    keyboard = [[InlineKeyboardButton("Refrescar", callback_data='1')]]
    context.bot.send_message(chat_id, text, reply_markup=InlineKeyboardMarkup(keyboard))
    
def temperatura(update,context):
    logger.info('He recibido un comando temperatura')
    text= "La última medición de las temperaturas 🌡 es: \n \
    " + d1 + d2 + d3 + d4 + c5 + c6 + ca + cb  
    chat_id = update.effective_chat.id
    keyboard = [[InlineKeyboardButton("Refrescar", callback_data='1')]]
    context.bot.send_message(chat_id, text, reply_markup=InlineKeyboardMarkup(keyboard))
    
def presion(update,context):
    logger.info('He recibico un comando presión')
    text= "La última medición de la presión 💨 es: \n" + pf
    chat_id = update.effective_chat.id
    keyboard = [[InlineKeyboardButton("Refrescar", callback_data='1')]]
    context.bot.send_message(chat_id, text, reply_markup=InlineKeyboardMarkup(keyboard))
    
def config(update,context):
    logger.info('He recibido un comando config')
    text= "⚙ ¿Qué deseas configurar? ⚙"
    chat_id = update.effective_chat.id
    keyboard = [[InlineKeyboardButton("Cambiar archivo de temperatura para Diodos y Cernox 5 y 6.", callback_data='2')],
                 [InlineKeyboardButton("Cambiar archivo de temperatura para Cernox A y B.", callback_data='3') ],
                 [InlineKeyboardButton("Cambiar archivo de presión.", callback_data='4')]]
    context.bot.send_message(chat_id, text, reply_markup=InlineKeyboardMarkup(keyboard))
    
def unknown(update,context):
    logger.info('He recibido un comando inválido')
    name = update.effective_chat.first_name
    text = "Lo siento, " + name + ".\nEse no es un comando válido. 😓😓" 
    chat_id = update.effective_chat.id
    keyboard(chat_id, text, context)
    
def CambioArchivo(update,context):
    query = update.callback_query
    query.answer()
    
    choice = query.data
    
    if choice == '2':
        chat_id = update.effective_chat.id
        text = "Ingresa la ruta del archivo, por ejemplo: \
            \nC:\\Usuario\\Documentos\\ArchivoTemperaturas.txt"
        context.bot.send_message(chat_id, text) 
    elif choice == '3':
        chat_id = update.effective_chat.id
        text = "Ingresa la ruta del archivo, por ejemplo: \
            \nC:\\Usuario\\Documentos\\ArchivoTemperaturas.txt"
        context.bot.send_message(chat_id, text)
    elif choice == '4':
        chat_id = update.effective_chat.id
        text = "Ingresa la ruta del archivo, por ejemplo: \
            \nC:\\Usuario\\Documentos\\ArchivoPresiones.txt"
        context.bot.send_message(chat_id, text)
        

if __name__ == '__main__':
    updater = Updater(token=Token, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('kill', stop))
    dispatcher.add_handler(CommandHandler('help', help1))
    dispatcher.add_handler(CommandHandler('mediciones', mediciones))
    dispatcher.add_handler(CommandHandler('temperatura', temperatura))
    dispatcher.add_handler(CommandHandler('presion', presion))
    dispatcher.add_handler(CommandHandler('config', config))
      
    dispatcher.add_handler(CallbackQueryHandler("CambioArchivo"))
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    
    updater.start_polling()
    updater.idle()    