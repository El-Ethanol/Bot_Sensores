#Bot de Sensores.

import logging, os, signal, time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.messagehandler import MessageHandler  
from Auxiliares import Medidas

#Identificador único del bot
Token = "1856897280:AAG-X-LqbFDk16PC9YVtm3jtpwPaAR76e44"

#Esto es para que el bot esté constantemente buscando en el servidor por mensajes nuevos.
logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s', level=logging.INFO)
logger = logging.getLogger('SensoresICNBot')

#Archivos que lee el bot de Temperatura (Diodos y Cernox 5 y 6), Temperatura (Cernox A y B) y Presión, respectivamente.
a='Temperatura135.txt'
b='TemperaturaM.txt'
c='Presion.csv'

#Variables.
tiempos = [] #Este array sirve para que el bot lea cuándo fue la última medición.
door = False #Cuando esto es verdadero, permite cambiar las rutas de los archivos que se leen,
n=0 #Contador para ver si se están actualizando los datos.
interval = 3600 #Tiempo entre alertas

#Parametros.
pd1=100
pd2=100
pd3=100
pd4=100
pc5=100
pc6=100
pca=100
pcb=100
pp1=0.0

#Función que obtiene los datos de los sensores y checa si se están actualizando.
def refrescar(update,context):
    global d1, d2, d3, d4, c5, c6, ca, cb, pf, now, n, f1, f2, f3, valores #Se obtienen los datos.
    logger.info('Refresqué') #El comando logger.info nos informa en dónde está el bot.
    meds = Medidas(a,b,c)
    d1, d2, d3, d4, c5, c6, ca, cb, pf, time1, time2, time3, valores = meds
    now=time.strftime("%X")
    tiempos.append([time1,time2,time3])
    if n >= 1:
        f1 = tiempos[n][0] == tiempos[n-1][0]
        f2 = tiempos[n][1] == tiempos[n-1][1]
        f3 = tiempos[n][2] == tiempos[n-1][2]
        if f1 or f2 or f3: 
            Error(update,context) 
    n = n + 1

#Comando para iniciar el bot.
def start(update,context):
    logger.info('Start')
    name = update.effective_chat.first_name #Se obtiene el nombre del usario.
    text = "¡Hola, " + name + "! 👋👋👋\n\nSoy el bot 🤖 del Lab. de Detectores del ICN.\
           \n\nTe puedo dar las últimas mediciones de los sensores de temperatura y de presión."
    chat_id = update.effective_chat.id #Se obtiene el identificador dónde se mandará el mensaje.
    keyboard(chat_id, text, context) #Se envía el mensaje y sale el comando.
    context.job_queue.run_repeating(parameters, interval = 30, first = 0, name='parametros' , context=update.effective_chat.id)
    
#Función de definiciones de parametros.    
def parameters(context):
    logger.info('Parametros')
    meds = Medidas(a,b,c)
    chat_id=context.job.context
    d1, d2, d3, d4, c5, c6, ca, cb, pf, time1, time2, time3, valores = meds
    if abs(float(valores[0][1]))<pd1:
        text="¡Cuidado! La temperatura del Diodo 1, está en fuera del rango. \nLa temperatura es:" + str(valores[0][1])
        context.bot.send_message(chat_id, text)
    elif abs(float(valores[0][2]))<pd2:
        text="¡Cuidado! La temperatura del Diodo 2, está en fuera del rango. \nLa temperatura es:" + str(valores[0][2])
        context.bot.send_message(chat_id, text)   
    elif abs(float(valores[0][3]))<pd3:
        text="¡Cuidado! La temperatura del Diodo 3, está en fuera del rango. \nLa temperatura es:" + str(valores[0][3])
        context.bot.send_message(chat_id, text)   
    elif abs(float(valores[0][4]))<pd4:
        text="¡Cuidado! La temperatura del Diodo 4, está en fuera del rango. \nLa temperatura es:" + str(valores[0][4])
        context.bot.send_message(chat_id, text)   
    elif abs(float(valores[0][5]))<pc5:
        text="¡Cuidado! La temperatura del Cernox 5, está en fuera del rango. \nLa temperatura es:" + str(valores[0][5])
        context.bot.send_message(chat_id, text)   
    elif abs(float(valores[0][6]))<pc6:
        text="¡Cuidado! La temperatura del Cernox 6, está en fuera del rango. \nLa temperatura es:" + str(valores[0][6])
        context.bot.send_message(chat_id, text)   
    elif abs(float(valores[1][1]))<pca:
        text="¡Cuidado! La temperatura del Cernox A, está en fuera del rango. \nLa temperatura es:" + str(valores[1][1])
        context.bot.send_message(chat_id, text)   
    elif abs(float(valores[1][2]))<pcb:
        text="¡Cuidado! La temperatura del Cernox B, está en fuera del rango. \nLa temperatura es:" + str(valores[1][2])
        context.bot.send_message(chat_id, text)   
    elif abs(float(valores[2][1]))<pp1:
        text="¡Cuidado! La presión está en fuera del rango. \nLa presión es:" + str(valores[2][1])
        context.bot.send_message(chat_id, text)   
    
#Función para activar el teclado con los comandos predeterminados.    
def keyboard(chat_id, text, context):
    kb = [[KeyboardButton("/start")],[KeyboardButton("/mediciones")], [KeyboardButton("/temperatura")], [KeyboardButton("/presion")],
          [KeyboardButton("/startalerts"), KeyboardButton("/stopalerts")],
          [KeyboardButton("/help"), KeyboardButton("/config")], [KeyboardButton("/kill")]]
    kb1 = ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_message(chat_id, text, reply_markup=kb1)

#Comando para matar al bot. (Si es activado se deberá reiniciar el script.)    
def stop(update,context):
    logger.info('Kill')
    name = update.effective_chat.first_name
    text = "¡Hasta pronto, " + name + "! 👋👋👋"
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id, text)
    updater.is_idle = False
    os.kill(os.getpid(), signal.SIGINT)   
    
#Comando para indiciarnos los comandos que existen. 
def help1(update,context):
    logger.info('Help')
    text = "Los comandos válidos son los siguientes: \
    \n\n/start - Inicia el bot. \
    \n\n/mediciones - Regresa las últimas mediciones de la temperatura del Cernox B y de la presión del MKS.\
    \n\n/temperatura - Regresa el último valor de temperatura de cada sensor.  \
    \n\n/presion - Regresa el último valor de presión del sensor. \
    \n\n/startalert - Comienza a enviar alertas. \
    \n\n/stopalert - Detiene el envío de alertas. \
    \n\n/config - Configuraciones del bot.\
    \n\n/help - Regresa la lista de los comandos y su descripción. \
    \n\n/kill - Detiene el bot."
    chat_id = update.effective_chat.id
    keyboard(chat_id, text, context)

#Comando para recibir las ultimas mediciones.
def mediciones(update,context):
    global r
    logger.info('Mediciones')
    refrescar(update,context)
    text= "La últimas mediciones son: \n \
        \n🌡 Temperatura:\n" + cb + "\n \n💨 Presión: \n" + pf + \
            "\n\nHora de Actualización {}".format(now)
    chat_id = update.effective_chat.id
    keyboard = [[InlineKeyboardButton("Refrescar", callback_data='1')]] #Sale un botón en el chat.
    context.bot.send_message(chat_id, text, reply_markup=InlineKeyboardMarkup(keyboard))
    r = 1

#Comando para recibir las últimas mediciones de la temperatura.
def temperatura(update,context):
    global r
    logger.info('Temperatura')
    refrescar(update,context)
    text= "La última medición de las temperaturas 🌡 es: \n \
    " + d1 + d2 + d3 + d4 + c5 + c6 + ca + cb + \
    "\n\nHora de última actualización {}".format(now)
    chat_id = update.effective_chat.id
    keyboard = [[InlineKeyboardButton("Refrescar", callback_data='1')]]
    context.bot.send_message(chat_id, text, reply_markup=InlineKeyboardMarkup(keyboard))
    r = 2

#Comando para recibir la última medición de la presión.    
def presion(update,context):
    global r
    logger.info('Presión')
    refrescar(update,context)
    text= "La última medición de la presión 💨 es: \n" + pf + \
    "\n\nHora de última actualización {}".format(now)
    chat_id = update.effective_chat.id
    keyboard = [[InlineKeyboardButton("Refrescar", callback_data='1')]]
    context.bot.send_message(chat_id, text, reply_markup=InlineKeyboardMarkup(keyboard))
    r = 3
    
#Comando para poder cambiar las rutas de los archivos (y próximamente los parametros).   
def config(update,context):
    logger.info('Config')
    text= "⚙ ¿Qué deseas configurar? ⚙"
    chat_id = update.effective_chat.id
    keyboard = [[InlineKeyboardButton("Cambiar parametros de Temperatura.", callback_data='2')],
                 [InlineKeyboardButton("Cambiar parametros de Presión.", callback_data='3') ],
                 [InlineKeyboardButton("Cambiar tiempo entre Alertas.", callback_data='4')]]
    context.bot.send_message(chat_id, text, reply_markup=InlineKeyboardMarkup(keyboard))
    
#Función para comandos inválidos.    
def unknown(update,context):
    logger.info('Inválido')
    name = update.effective_chat.first_name
    text = "Lo siento, " + name + ".\nEse no es un comando válido. 😓" 
    chat_id = update.effective_chat.id
    keyboard(chat_id, text, context)
        
#Alarmas (activación, detención e información.)
def startalarm(update,context):
    logger.info('Iniciar Alarmas')
    text = "Las alertas están activadas. 🚨"
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id, text)
    newjob2 = context.job_queue.run_repeating(alarma, interval = interval, first = 0, name='Alarmas', context=update.effective_chat.id)
    
def stopalarm(update,context):
    logger.info('Detener Alarmas')
    chat_id = update.effective_chat.id
    text = "Las alertas se han desactivado. 🔕"
    jb = context.job_queue.get_jobs_by_name("Alarmas")
    context.bot.send_message(chat_id, text)
    jb[0].schedule_removal()
    
def alarma(context):
    logger.info('Alarma')
    meds = Medidas(a,b,c)
    chat_id=context.job.context
    d1, d2, d3, d4, c5, c6, ca, cb, pf, time1, time2, time3, valores = meds
    now = time.strftime("%X")
    text = "Las mediciones desde la última alarma son: \n \
        \n🌡 Temperatura:\n" + d1 + d2 + d3 + d4 + c5 + c6 + ca + cb + "\n \n💨 Presión: \n" + pf + \
            "\n\nHora de medición: {}".format(now)
    context.bot.send_message(chat_id, text)
    text = "La gráfica de la presión desde la última alerta es:"
    context.bot.send_message(chat_id, text)
    context.bot.send_photo(chat_id, photo=open('grafica1.png', 'rb'))
    
#Función para administrar los botones en pantalla.
def Options(update,context):
    global door, s, t, f, interval
    logger.info('Options')
    query = update.callback_query
    query.answer()
    
    choice = query.data
    door = True 
       
   #Cambio de parametros de temperatura.
    if choice == '2':
        chat_id = update.effective_chat.id
        text = "Para poder cambiar el parametro, escribe, por ejemplo:\nDiodo_1: 100 K"
        context.bot.send_message(chat_id, text)
        text = "Es importante que respetes los espacios."
        context.bot.send_message(chat_id, text)
        text = "Los parametros actualmente son:\n\nDiodo1:" + str(pd1) + \
            "K \nDiodo 2: " + str(pd2) + " K\nDiodo 3: " + str(pd3) + " K\nDiodo 4: " + str(pd4) + \
            "K \nCernox 5: " + str(pc5) + " K\nCernox 6: " + str(pc6) + " K\nCernox A: " + str(pca) + \
            "K \nCernox B: " + str(pcb)  + " K"
        context.bot.send_message(chat_id, text)
        s=2
   #Cambio de parametro de presión.
    elif choice == '3':
        chat_id = update.effective_chat.id
        text = "Para poder cambiar el parametro, escribe, por ejemplo:\nMKS: 100 Torr"
        context.bot.send_message(chat_id, text)
        text = "Es importante que respetes el espacios."
        context.bot.send_message(chat_id, text)
        text = "El parametro actualmente es:\nMKS: " + str(pp1) + " Torr" 
        context.bot.send_message(chat_id, text)
        s=3
   #Cambio de tiempo de alarma.
    elif choice == '4':
        chat_id = update.effective_chat.id
        text = "El tiempo entre alarma y alarma es {} min".format(interval/60)
        context.bot.send_message(chat_id, text)
        text = "Ingresa el tiempo entre alarmas en minutos:"
        context.bot.send_message(chat_id, text)
        s=4
        
   #Botones para refrescar.     
    elif choice == '1':
        if r==1:
            mediciones(update,context)
        elif r==2:
            temperatura(update,context)
        elif r==3:
            presion(update,context)
            
            
#Función para que el bot detecté los mensajes con los parametros.      
def Text(update,context):
    global door, interval, pd1, pd2, pd3, pd4, pc5, pc6, pca, pcb, pp1
    logger.info('Text')
    if door:
        parametro = update.message.text
        try:
            if s==2:
                parametro=parametro.split(' ')
                try: 
                    if 'Diodo_1:'==parametro[0]:
                        pd1 = parametro[1]
                    elif 'Diodo_2:'==parametro[0]:
                        pd2 = parametro[1]
                    elif 'Diodos_3:'==parametro[0]:
                        pd3 = parametro[1]
                    elif 'Diodos_4:'==parametro[0]:
                        pd4 = parametro[1]
                    elif 'Cernox_5:'==parametro[0]:
                        pc5 = parametro[1]
                    elif 'Cernox_6:'==parametro[0]:
                        pc6 = parametro[1]
                    elif 'Cernox_A:'==parametro[0]:
                        pca = parametro[1]
                    elif 'Cernox_B:'==parametro[0]:
                        pcb = parametro[1]
                    elif 'MKS:'==parametro[0]:
                        pp1 = parametro[1]
                    chat_id = update.effective_chat.id
                    text = "El parametro de" + parametro[0] + "ha sido actualizado. 😎"
                    context.bot.send_message(chat_id, text)
                except:
                    chat_id = update.effective_chat.id
                    text = "Revisa que el mensaje esté bien escrito"
                    context.bot.send_message(chat_id, text)
            elif s==3:
                parametro=parametro.split(' ')
            elif s==4:
                interval=float(parametro)*60
                chat_id = update.effective_chat.id
                text = "El tiempo entre alarmas ha sido actualizado. 😎"
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
        
#Función en caso de que los archivos no se estén actualizado.        
def Error(update,context):
    logger.info("Errores")
    chat_id = update.effective_chat.id
    name = update.effective_chat.first_name
    archivo= "HOLA"
    text = name + ", revisa que se esté actualizando el archivo de " + archivo + ". 🧐 \
    \nMe parece que no se están guardando nuevos datos." 
    if f1 and f2 and f3:
        text= name + ", revisa que se estén actualizando los archivos. 🧐 \
    \nMe parece que no se están guardando nuevos datos." 
    elif f1 and f2:
        text = name + ", revisa que se estén actualizando los archivos de Temperatura (Diodos y Cernox). 🧐 \
    \nMe parece que no se están guardando nuevos datos."
    elif f1 and f3:
        text = name + ", revisa que se estén actualizando el archivo de Temperatura (Diodos y Cernox 5 y 6) y el de Presión. 🧐 \
    \nMe parece que no se están guardando nuevos datos."
    elif f2 and f3:
        text = name + ", revisa que se estén actualizando el archivo de Temperatura (Cernox A y B) y el de Presión. 🧐 \
    \nMe parece que no se están guardando nuevos datos."
    elif f1:
        archivo="Temperatura Diodos y Cernox 5 y 6"  
    elif f2:
        archivo="Temperaturas Cernox A y B"
    elif f3:
        archivo="Presión"
    context.bot.send_message(chat_id, text)

#Ejecutar el programa.
if __name__ == '__main__':

   #Variables para que el bot lea los comandos.
    updater = Updater(token=Token, use_context=True)
    dispatcher = updater.dispatcher
    
   #Adición de comandos y conectarlos con su función.
    dispatcher.add_handler(CommandHandler('start', start, pass_job_queue=True))
    dispatcher.add_handler(CommandHandler('kill', stop))
    dispatcher.add_handler(CommandHandler('help', help1))
    dispatcher.add_handler(CommandHandler('mediciones', mediciones))
    dispatcher.add_handler(CommandHandler('temperatura', temperatura))
    dispatcher.add_handler(CommandHandler('presion', presion))
    dispatcher.add_handler(CommandHandler('config', config))
    dispatcher.add_handler(CommandHandler('startalerts', startalarm, pass_job_queue=True)) #pass_job_queue hace que comience el contador para mandar las alarmas.
    dispatcher.add_handler(CommandHandler('stopalerts', stopalarm, pass_job_queue=True)) 
    
   #Conectar los mensajes en texto con la función para las rutas.
    dispatcher.add_handler(MessageHandler(Filters.text, Text))

   #Conectar los botones en pantalla con su función.
    dispatcher.add_handler(CallbackQueryHandler(Options))
    
   #Comandos desconocidos y su error
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    
   #Activadores del bot. 
    updater.start_polling()
    updater.idle()    