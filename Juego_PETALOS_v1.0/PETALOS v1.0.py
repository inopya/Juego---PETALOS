#         _\|/_
#         (O-O)
# -----oOO-(_)-OOo----------------------------------------------------

#######################################################################
# ******************************************************************* #
# *                        Juego PETALOS PyGame                     * #
# *                    Autor: Eulogio López Cayuela                 * #
# *                                                                 * #
# *                  Versión 1.0    Fecha: 8/08/2014               * #
# *                                                                 * #
# ******************************************************************* #
#######################################################################

# Importa las funcionalidades externas


from tkinter import *
import time
import pygame
from pygame.locals import *
from sys import exit
import random

fondo_imagen = 'cielo.jpg'
centro_flor_imagen = 'centro.png'
petalo_imagen = 'petalo.png'
numero_petalos = 6
errores_max = numero_petalos - 1
angulo = 360/ numero_petalos




pygame.init()

#  DEFINIR PANTALLA y CARGAR IMAGENES
# -------------------------------------------------------------------------
#
screen = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption("¡¡ADIVINA LA PALABRA!!")


fondo_pantalla = pygame.image.load(fondo_imagen).convert()
centro_flor = pygame.image.load(centro_flor_imagen)
petalo = pygame.image.load(petalo_imagen)


#  CARGA DE PALABRAS DESDE UN FICHERO TXT EXTERNO. Definicion de Variables
# -------------------------------------------------------------------------
#

# Leemos las palabras desde un fichero TXT
palabras =[]        # Lista para almacenar las palabras contenidas en el fichero de texto
f = open('diccionario.txt', 'r')# Abrimos el fichero para su lectura
almacen=f.read()    # Variable para almacenar todo el contenido del fichero TXT
f.close()           # Cerramos el fichero tras su lectura

# Recorremos el almacen para encontrar las palabras que están separadas por un INTRO
# y almacenamos dichas palabras en la lista 'PALABRAS'
for palabra in almacen.split('\n'): 
    palabras.append(palabra)

palabra_oculta = []     # lista que contiene los caracteres de la palabra buscada

palabra_jugador = []    # lista que contiene los caracteres adivinados y '-' en
                        # las posiciones que no se conoce la letra

visor =''               # Muestra lineas - en el lugar de las letras que aun no se han adivinado
letras_usadas=''       # Cadena que almacena las letras que ya se han utilizado
jugada_en_curso = 0
partida_terminada = 0


# CREAR VISOR (Palabra vacia)
#----------------------------------------------------------------
#

def crear_palabra_vacia():
    global palabra_oculta, palabra_jugador, palabras, secreto #, letras_usadas, visor
    
    indice = random.randint(0,len(palabras)-1)
    for letra in palabras[indice]:
        palabra_oculta.append(letra)
        palabra_jugador.append('-')
    secreto = palabras[indice]
    del palabras[indice]
    i=0
    visor=''
    while i< len(palabra_oculta):
        visor=visor+palabra_jugador[i]
        i=i+1
    return (visor)


# COMPROBAR ACIERTOS Y ERRORES
#----------------------------------------------------------------
#

def comprobar_letra(pulsacion):
    global palabra_oculta, palabra_jugador, visor, palabras
    global numero_petalos, letras_usadas, letra_repetida1
    global preguntar_letra, letra_repetida1, no_has_acertado, has_acertado, sigue_jugando 
    global jugada_en_curso, msg, letras_usadas, partida_terminada

    fallo = 0
    jugada_en_curso = 1
    for m in (str(letras_usadas)):
        if pulsacion == m:
            return (letra_repetida1)
        
    letras_usadas += pulsacion+','
    fallo = 1
    visor = ''
    i = 0
    while i< len(palabra_oculta):
        if palabra_oculta[i] == pulsacion:
            palabra_jugador[i] = pulsacion
            fallo = 0
        visor = visor + palabra_jugador[i]
        i =i+1
        
    numero_petalos = numero_petalos - fallo
    if numero_petalos == 0:
        jugada_en_curso = 2


        msg, letras_usadas = 'La palabra buscada era: ', secreto
        return (no_has_acertado)

    if palabra_jugador == palabra_oculta:
        jugada_en_curso = 2

        return (solucion_correcta)
    return(sigue_jugando) 



# ROTAR UNA IMAGEN POR SU CENTRO (para generar los petalso de la flor)
#-------------------------------------------------------------------
#

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image



# DEFINICION DE MENSAJES EN PANTALLA YLAS CARACTERISICAS DE LOS TEXTOS
#---------------------------------------------------------------------
#

letra25 = pygame.font.SysFont("Courier", 25)
letra30 = pygame.font.SysFont("Arial", 30)
letra50 = pygame.font.SysFont("Arial", 50)
letra101 = pygame.font.SysFont("Courier", 50)


preguntar_letra = letra30.render("dime una letra: ", True, (0,0,0))

solucion_correcta = letra50.render("¡Enhorabuena, has acertado!", True, (0,255,0),(255,100,25))
letra_repetida1 = letra50.render("Letra ya usada. Dime otra",
                                  True, (255,0,0),(0,0,0))
no_has_acertado = letra50.render("Lo siento, has fallado  :( ", True, (255,0,0) )
sigue_jugando = letra30.render (" ", True, (0,0,255))
mensaje = letra50.render ("", True, (0,0,255))
rectanguloMensaje = (0,0)
                                
pulsacion = ""
respuesta = letra30.render(pulsacion, True, (0,0,255))
msg = 'Letras utilizadas: '
visor_letras_usadas = ""
mensaje_usadas = letra25.render(visor_letras_usadas, True, (0,0,0), (255,255,0)) 
rectanguloMensajeUsadas = (0,0) 

#***************************************************************
#                   INICIO DEL BUCLE DEL PROGRAMA
#***************************************************************
terminarJuego = False
while not terminarJuego:
    for event in pygame.event.get():
        if event.type == QUIT:
            terminarJuego = True
        if jugada_en_curso == 2:
            esperar = True
            while esperar:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        numero_petalos = errores_max + 1
                        jugada_en_curso = 0
                        palabra_oculta = []
                        palabra_jugador = []
                        letras_usadas = ''
                        visor = ''
                        mensaje = letra50.render ("", True, (0,0,255))
                        pulsacion = ""
                        respuesta = letra30.render(pulsacion, True, (0,0,255))
                        esperar = False
                        msg, letras_usadas = '', ''



        if event.type is KEYDOWN:
                pulsacion = str(event.unicode)
                respuesta = letra50.render(pulsacion, True, (255,255,0) )
                mensaje = comprobar_letra(pulsacion)
                rectanguloMensaje = mensaje.get_rect()
                rectanguloMensaje.centerx = screen.get_rect().centerx
                rectanguloMensaje.centery = 425
                visor_letras_usadas = msg + letras_usadas
                mensaje_usadas = letra25.render(visor_letras_usadas, True, (0,0,0), (255,255,0))
                rectanguloMensajeUsadas = mensaje_usadas.get_rect()
                rectanguloMensajeUsadas.centerx = screen.get_rect().centerx
                rectanguloMensajeUsadas.centery = 475


    # llamada a la funcion que inicializa el acertijo y pregunta letra
    if jugada_en_curso == 0 and visor == '':
        visor = crear_palabra_vacia()
    contenido_visor = letra101.render (visor, True, (240,240,240),(0,0,0))

   

# REGENERAR PANTALLA GRAFICA
#--------------------------------------------------------------------------
#

    screen.blit(fondo_pantalla, (0,0))

    for i in range (numero_petalos):
        petalo_rotado = rot_center(petalo, angulo*i)
        screen.blit(petalo_rotado, (50,50))
    screen.blit(centro_flor, (50,50))
    
    screen.blit(preguntar_letra , (450,50))
    screen.blit(respuesta, (680,35))    
    screen.blit(contenido_visor , (350,150))
    screen.blit(mensaje , rectanguloMensaje)
    screen.blit(mensaje_usadas , rectanguloMensajeUsadas)
    
    pygame.display.update()


pygame.quit ()

# FINALIZAR PROGRAMA
#-------------------------------------------------------------------



