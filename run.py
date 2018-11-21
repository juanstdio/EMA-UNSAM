# -*- coding: utf-8 -*-
import telebot
import time
import data
import urllib
import os
import signal
import sys
API_TOKEN = 'Find it on telegram' 

bot = telebot.TeleBot(API_TOKEN)
print "Sistema iniciado"
bandera = 0
bienvenida = 0
print 'Cantidad de solicitudes:' + str(bandera)
def signal_handler(sig, frame):
        print('Terminando ejecucion')
        archivo = open('RegistroDeUsuarios.txt', 'a')
        archivo.write(time.strftime("%d/%m/%y"))
        archivo.write("|")
        archivo.write(time.strftime("%H:%M:%S"))
        archivo.write("|")
        archivo.write('Solicitudes Procesadas antes del cierre= ')
        archivo.write(str(bandera))
        archivo.write("|")
        archivo.write("Usuarios Nuevos= "+ str(bienvenida))
        archivo.write("\n")
        archivo.close()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
print('Presionar Ctrl y C en cualquier momento para finalzar')

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    global bienvenida    
    bot.send_message(message.chat.id,"<- E.M.A. UNSAM -> by @Juanstdio")
    bot.send_message(message.chat.id,"Envia la palabra 'Clima' o 'Tiempo' ")
    bienvenida = bienvenida + 1    
    print 'Bienvenida enviada'



@bot.message_handler(func=lambda message: True)
def echo_message(message):
        global bandera
        mensaje= message.text
        chat_id= message.chat.id
        
        #Micro Registro de usuarios
        archivo = open('RegistroDeUsuarios.txt', 'a')
        archivo.write(time.strftime("%d/%m/%y"))
        archivo.write("|")
        archivo.write(time.strftime("%H:%M:%S"))
        archivo.write("|")
        archivo.write(str(chat_id))
        archivo.write("|")
        archivo.write(mensaje)
        archivo.write("\n")
        archivo.close()
        #Fin Micro registro de usuarios
        
        # Ejecución de ordenes #         
        if 'CLIMA' in mensaje.upper() or 'TEMP' in mensaje.upper():
                general = ''
                post = data.datos()
                if len(post) < 1:
                    bot.send_message(chat_id,'El servicio esta fallando y no es por este software')
                    bot.send_message(chat_id,"¿Servidor Caído?" )
                else:
                    
                    for lista in post:
                        general += lista
                    bot.send_message(chat_id, general)
                    print 'Todo bien, mensaje enviado a: ' + str(chat_id)
                    bandera = bandera + 1
                
        elif 'GRAPH' in mensaje.upper() or 'DIBU' in mensaje.upper():
                print 'Pidieron graficos'
                
                #urllib.urlretrive("http://ema.unsam.edu.ar/OutsideTempHistory.gif",'temperatura.gif')
                #img = open('temperatura.gif', 'rb')
                
                #img.close()
                temp='http://ema.unsam.edu.ar/OutsideTempHistory.gif'
                hum ='http://ema.unsam.edu.ar/OutsideHumidityHistory.gif'
                pre ='http://ema.unsam.edu.ar/BarometerHistory.gif'
                
                bot.send_message(chat_id, 'Estamos preparando las Imágenes' )
                os.system('wget '+ temp)
                print 'Imagen Descargada, enviando a chat'
                bot.send_chat_action(chat_id, 'upload_photo')
                bot.send_message(chat_id,'Temperatura últimas 24hs')
                img = open('OutsideTempHistory.gif', 'rb')
                bot.send_photo(chat_id, img)
                img.close()

                os.system('wget '+ hum)
                print 'Imagen Descargada, enviando a chat'
                bot.send_chat_action(chat_id, 'upload_photo')
                img = open('OutsideHumidityHistory.gif', 'rb')
                bot.send_message(chat_id,'Humedad últimas 24hs')
                bot.send_photo(chat_id, img)
                img.close()

                os.system('wget '+ pre)
                print 'Imagen Descargada, enviando a chat'
                bot.send_chat_action(chat_id, 'upload_photo')
                img = open('BarometerHistory.gif', 'rb')
                bot.send_message(chat_id,'Presión últimas 24hs')
                bot.send_photo(chat_id, img)
                img.close()
                os.system('rm *.gif')
                print 'Archivos gifs borrados'
                bot.send_message(chat_id,'Para más información, consulte la ayuda')
                bandera = bandera + 1
            
        elif 'SOLAR' in mensaje.upper():
                sol='http://ema.unsam.edu.ar/SolarRadHistory.gif'
                os.system('wget '+ sol)
                print 'Imagen Descargada, enviando a chat'
                bot.send_chat_action(chat_id, 'upload_photo')
                img = open('SolarRadHistory.gif', 'rb')
                bot.send_message(chat_id,'Radiación solar, últimas 24hs')
                bot.send_photo(chat_id, img)
                img.close()
                os.system('rm *.gif')
                print 'Archivos gifs borrados'
                bot.send_message(chat_id,'Gracias (:\nPara más información, consulte la ayuda')
                bandera = bandera + 1
                
        elif 'WIND' in mensaje.upper():
                v1='http://ema.unsam.edu.ar/WindDirection.gif'
                v2='http://ema.unsam.edu.ar/WindSpeedHistory.gif'
                v3='http://ema.unsam.edu.ar/WindSpeed.gif'
                os.system('wget '+ v1)
                os.system('wget '+ v2)
                os.system('wget '+ v3)
                bot.send_message(chat_id,'Vientos, últimas 24hs')
                #v1
                bot.send_chat_action(chat_id, 'upload_photo')
                img = open('WindDirection.gif', 'rb')
                bot.send_photo(chat_id, img)
                img.close()
                #v2
                bot.send_chat_action(chat_id, 'upload_photo')
                img = open('WindSpeedHistory.gif', 'rb')
                bot.send_photo(chat_id, img)
                img.close()
                #v3
                bot.send_chat_action(chat_id, 'upload_photo')
                img = open('WindSpeed.gif', 'rb')
                bot.send_photo(chat_id, img)
                img.close()
                bot.send_message(chat_id,'Gracias (:\nPara mas información, consulte la ayuda.')
                print 'Borrando Archivos utilizados...'
                os.system('rm *.gif')

                
        else:
                msg104 = " No Entendi..\nFijate las opciones a la izquierda del -Clip-"
                bot.send_message(chat_id,msg104)
                print '-> enviado a ' + str(chat_id)
                bandera = bandera + 1
                print 'Se equivocaron,Registro= ' + str(bandera)
#
#os.system('rm /home/juan/emaunsam/*.gif')

      
bot.polling()


