import logging, os, signal, time
import numpy as np
from typing import Text
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.messagehandler import MessageHandler  
from Auxiliares import Medidas
Token = "1856897280:AAG-X-LqbFDk16PC9YVtm3jtpwPaAR76e44"

logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s', level=logging.INFO)
logger = logging.getLogger('SensoresICNBot')

a = 'Temperatura135.txt'
b = 'TemperaturaM.txt'
c = 'Presion.csv'
tiempos = []
door = False
n=0

def refrescar(update,context):
    global d1, d2, d3, d4, c5, c6, ca, cb, pf, now, n, f1, f2, f3
    logger.info('Refresqué')
    meds = Medidas(a,b,c)
    d1, d2, d3, d4, c5, c6, ca, cb, pf, time1, time2, time3 = meds
    now=time.strftime("%X")
    tiempos.append([time1,time2,time3])
    if n == 1:
        f1 = tiempos[n][0] == tiempos[n-1][0]
        f2 = tiempos[n][1] == tiempos[n-1][1]
        f3 = tiempos[n][2] == tiempos[n-1][2]
        if f1 or f2 or f3: 
            Error(update,context) 
    n = n + 1

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
    \n\n/start - Inicia el bot. \
    \n\n/mediciones - Regresa las últimas mediciones del la temperatura del Cernox B y de la temperatura del MKS.\
    \n\n/temperatura - Regresa el último valor de temperatura de cada sensor.  \
    \n\n/presion - Regresa el último valor de presión del sensor. \
    \n\n/config - Configuraciones del bot.\
    \n\n/help - Regresa la lista de los comandos y su descripción. \
    \n\n/kill - Detiene el bot."
    chat_id = update.effective_chat.id
    keyboard(chat_id, text, context)

def mediciones(update,context):
    global r
    logger.info('He recibido un comando mediciones')
    refrescar(update,context)
    text= "La últimas mediciones son: \n \
        \n🌡 Temperatura:\n" + cb + "\n \n💨 Presión: \n" + pf + \
            "\n\nHora de Actualización {}".format(now)
    chat_id = update.effective_chat.id
    keyboard = [[InlineKeyboardButton("Refrescar", callback_data='1')]]
    context.bot.send_message(chat_id, text, reply_markup=InlineKeyboardMarkup(keyboard))
    r = 1
    
def temperatura(update,context):
    global r
    logger.info('He recibido un comando temperatura')
    refrescar(update,context)
    text= "La última medición de las temperaturas 🌡 es: \n \
    " + d1 + d2 + d3 + d4 + c5 + c6 + ca + cb + \
    "\n\nHora de última actualización {}".format(now)
    chat_id = update.effective_chat.id
    keyboard = [[InlineKeyboardButton("Refrescar", callback_data='1')]]
    context.bot.send_message(chat_id, text, reply_markup=InlineKeyboardMarkup(keyboard))
    r = 2
    
def presion(update,context):
    global r
    logger.info('He recibido un comando presión')
    refrescar(update,context)
    text= "La última medición de la presión 💨 es: \n" + pf + \
    "\n\nHora de última actualización {}".format(now)
    chat_id = update.effective_chat.id
    keyboard = [[InlineKeyboardButton("Refrescar", callback_data='1')]]
    context.bot.send_message(chat_id, text, reply_markup=InlineKeyboardMarkup(keyboard))
    r = 3
    
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
    text = "Lo siento, " + name + ".\nEse no es un comando válido. 😓" 
    chat_id = update.effective_chat.id
    keyboard(chat_id, text, context)
    
def Options(update,context):
    global door, s
    logger.info('Estoy en Options')
    query = update.callback_query
    query.answer()
    
    choice = query.data
    door = True 
    
    if choice == '2':
        chat_id = update.effective_chat.id
        text = "Ingresa la ruta del archivo, por ejemplo: \
            \n\\home\\Usuario\\Documentos\\ArchivoTemperaturas.txt"
        context.bot.send_message(chat_id, text)
        text = "El archivo que actualmente estoy leyendo es {}".format(a) 
        context.bot.send_message(chat_id, text)
        s=2
    elif choice == '3':
        chat_id = update.effective_chat.id
        text = "Ingresa la ruta del archivo, por ejemplo: \
            \n\\home\\Usuario\\Documentos\\ArchivoTemperaturas.txt."
        context.bot.send_message(chat_id, text)
        text = "El archivo que actualmente estoy leyendo es {}.".format(b) 
        context.bot.send_message(chat_id, text)
        s=3
    elif choice == '4':
        chat_id = update.effective_chat.id
        text = "Ingresa la ruta del archivo, por ejemplo: \
            \n\\home\\Usuario\\Documentos\\ArchivoPresiones.txt"
        context.bot.send_message(chat_id, text)
        text = "El archivo que actualmente estoy leyendo es {}.".format(c)
        context.bot.send_message(chat_id, text)
        s=4
        
    elif choice == '1':
        if r==1:
            mediciones(update,context)
        elif r==2:
            temperatura(update,context)
        elif r==3:
            presion(update,context)

def Text(update,context):
    global a, b, c, door
    logger.info('Ando en Text')
    if door:
        nueva_ruta = update.message.text
        try:
            if s==2:
                a='{}'.format(nueva_ruta)
            elif s==3:
                b='{}'.format(nueva_ruta)
            elif s==4:
                c='{}'.format(nueva_ruta)
            refrescar()
            chat_id = update.effective_chat.id
            text = "La ruta del archivo ha sido actualizada. 😎"
            context.bot.send_message(chat_id, text)
        except:
            chat_id = update.effective_chat.id
            text = "La ruta del archivo que ingresaste es inválida. 😕"
            context.bot.send_message(chat_id, text)
        door =  False
    else:
        chat_id = update.effective_chat.id
        name = update.effective_chat.first_name
        text = "Lo siento, " + name + ". 😕" + "\nNo entiendo que me quieres decir. \
        revisa la lista de comandos con /help."
        context.bot.send_message(chat_id, text)
        
def Error(update,context):
    chat_id = update.effective_chat.id
    name = update.effective_chat.first_name
    if f1 and f2 and f3:
        text1 = name + ", revisa que se estén actualizando los archivos. 🧐 \
    \nMe parece que no se están guardando nuevos datos." 
        context.bot.send_message(chat_id, text1)
    elif (f1 and f2) or (f1 and f3) or (f3 and f2) :
        text1 = name + ", revisa que se estén actualizando los archivos. 🧐 \
    \nMe parece que no se están guardando nuevos datos." 
        context.bot.send_message(chat_id, text1)
    elif f1:
        archivo="Temperatura Diodos y Cernox 5 y 6"
    elif f2:
        archivo="Temperaturas Cernox A y B"
    elif f3:
        archivo="Presión"
    text = name + ", revisa que se esté actualizando el archivo de " + archivo + ". 🧐 \
    \nMe parece que no se están guardando nuevos datos." 
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
    
    dispatcher.add_handler(MessageHandler(Filters.text, Text))
    dispatcher.add_handler(CallbackQueryHandler(Options))
    
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    
    updater.start_polling()
    updater.idle()    