# -*- coding: utf-8 -*-


import urllib

from bs4 import BeautifulSoup

# Como la web de la UNSAM tiene una proteccion contra "bots" (que este es el caso de uno)
# utilizamos la librería cfscrape para "saltear" dicha protección
import cfscrape
def datos():
    
    #aca viene la magia del salteo de CloudFlare
    bypass = cfscrape.create_scraper()
    respuesta = bypass.get('http://ema.unsam.edu.ar/').content

    #cuando tenemos la respuesta, la parseamos como lxdl
    sopa = BeautifulSoup(respuesta,'lxml')
    
    #luego de ese lxml, nos quedamos con el texto
    raw = sopa.get_text()
    
    #Solo para obtener las cadenas cortadas (Muy defectuoso)
    #raw = sopa.stripped_strings
    
    #armamos una cadena vacía
    general = ''

    #Como el texto está lleno de /n, usamos rstrip para recortar
    raw = raw.rstrip('\n')
    filtrado = raw.splitlines()

    #Esta parte sólo se utiliza para ubicar en el código web, en que -renglón- se ubica
    #cada valor que estamos necesitando
    
    #for l in range(len(filtrado)):
        #print(l,filtrado[l])

    #Una vez que tenemos las posiciones de los valores que estamos buscando, las reorganizamos
    #en un texto mas lindo...Lo que está comentado es porque lo usaba para monitorear en algún momento...
    
    #print 'Temperatura'
    general += 'Temperatura: ' + filtrado[42].rstrip('&nbsp') + '\n'
    #print 'Humedad'
    general += 'Humedad: '+filtrado[98].rstrip('&nbsp') + '\n'
    #print 'Presion atmosferica'
    general += 'Presion atmosferica: '+filtrado[233].rstrip('&nbsp')+'\n'
    #print 'Velocidad del viento'
    general += 'Velocidad del viento: '+filtrado[261].rstrip('&nbsp')+'\n'
    #print 'Direccion'
    general += 'Direccion: '+filtrado[267].rstrip('&nbsp')+'\n'
    #print 'Lluvia'
    general += 'Lluvia: '+ filtrado[321].rstrip('&nbsp')+'\n'
    #print 'Intensidad de lluvia'
    general += 'Intensidad de lluvia: '+filtrado[325].rstrip(' &nbsp')+'\n'
    #print 'Evapotranspiracion diario'
    general += 'Evapotranspiracion diario: '+ filtrado[361].rstrip(' &nbsp')+'\n'
    #print 'Radiacion solar'
    general += 'Radiacion solar: '+filtrado[400].rstrip('&nbsp')+'\n'
    #print 'Radiacion UV'
    general += 'Radiacion UV: '+ filtrado[429] + '\n'

    #antes usaba la funcion
    #devolver = [filtrado[42],filtrado[98],filtrado[233].rstrip('&nbsp'), filtrado[261].rstrip('&nbsp')
    #la nueva version retorna una cadena procesada renglón por renglón...
    
    return general

