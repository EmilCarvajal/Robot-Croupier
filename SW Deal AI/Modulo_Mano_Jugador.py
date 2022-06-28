# -*- coding: utf-8 -*-

import numpy as np
import eval7 #instalar :  pip install eval7
from pokereval.card import Card# install pip install pokereval
from pokereval.hand_evaluator import HandEvaluator 
#--
import cv2  
import matplotlib.pyplot as plt # pyplot
from PIL import Image
import glob
import os
import math

from Modulo_Vision_Computador import *


#---- VAR GLOABLES

#AREAS DONDE SE VEN LAS CARTAS DE CADA: 5JUGADORES (PARA JOFRE)

areas5jugC =[
        [175, 410, 780 , 1012],
        [20 , 250 , 630,860 ],
        [20,200, 400,640],
        [20 , 250 , 180,420 ],
        [175, 394, 30 , 258], [240,380,350,720]   #pos 5 es cartas centrales
]



def procesarCartasYolo(cartas):
    cartasProcesadas = []
    cartasProcesadas2 = []
    
    for carta in cartas:
        print(carta)
        objeto = carta[0].split() # "A Spades"
        numero = objeto[0]                      # "A"
        tipo   = objeto[1][0].lower()           # "s"
        if (tipo == 't'):
            tipo = 'c'
        cartasProcesadas.append(Card(numero, tipo)) # Card(A,"s")
        cartasProcesadas2.append(eval7.Card(numero + tipo)) # Card('As')
        
    return cartasProcesadas, cartasProcesadas2


def decirGanador(players_p, ronda):
    cartasTablero = []
    cartasTablero2 = []
    
    if (ronda != 0):
        f_inicial = areas5jugC[5][0] #[5] es zona tablero
        f_final   = areas5jugC[5][1] 
        c_inicial = areas5jugC[5][2] 
        c_final   = areas5jugC[5][3] 

        imageCam = obtenerImagen()

        imagenTablero = imageCam[f_inicial:f_final,c_inicial:c_final]#get_image()
        yoloCartasTablero = 0
        # Yolo hasta detectar objetos
        while yoloCartasTablero == 0:
            yoloCartasTablero  = valorObjetos(imagenTablero)
        
        cartasTablero, cartasTablero2 = procesarCartasYolo(yoloCartasTablero) # [Card(A,"s"), Card(2,"s") ]


    puntuacionMax =0
    ganador = -1
    combo_ganador = -1
    for p in players_p: 
        f_inicial = areas5jugC[p-1][0] 
        f_final   = areas5jugC[p-1][1] 
        c_inicial = areas5jugC[p-1][2] 
        c_final   = areas5jugC[p-1][3] 
        
        # el jpg es pruevaa
        imagenCartasJugador = cv2.imread('IMG_ASpades.jpg', 1)
        imagenCartasJugador = cv2.cvtColor(imagenCartasJugador,cv2.COLOR_BGR2RGB)
        #imageCam = obtenerImagen()
        #imagenCartasJugador = imageCam#[f_inicial:f_final,c_inicial:c_final]#get_image()
        
        yoloCartasJugador = 0
        # Yolo hasta detectar objetos
        while yoloCartasJugador == 0:
            yoloCartasJugador  = valorObjetos(imagenCartasJugador)
        
        cartasJugador, cartasJugador2 = procesarCartasYolo(yoloCartasJugador) # [Card(A,"s"), Card(2,"s") ]

        # obtener puntuacion y mano del jugador
        puntuacion = HandEvaluator.evaluate_hand(cartasJugador, cartasTablero)
        
        manoJugador = eval7.handtype(eval7.evaluate(cartasJugador2 + cartasTablero2))

        if puntuacion > puntuacionMax:
            puntuacionMax = puntuacion #double
            ganador = p
            combo_ganador = manoJugador # string
    print("------------------------------------")
    print("JUGADOR GANADOR : ", p)
    print("MANO del ganador: ", combo_ganador)
    
    return ganador, combo_ganador
#decirGanador2([1],0)
        
"""
cartasJugador = [eval7.Card( '2c'), eval7.Card('5d')]
cartasTablero = [Card(2, 's'), Card(2, 'h'),Card(7, 's')]
#score = HandEvaluator.evaluate_hand(cartasJugador, cartasTablero)
#print('{0:.50f}'.format(score))
#print("SCORE = >>", score)
hand = eval7.handtype(eval7.evaluate(cartasJugador))
print(hand)
hole = [Card(2, 'c'), Card(5,'h')]
board = [Card(2, 's'), Card(2, 'h'),Card(7, 's')]
score = HandEvaluator.evaluate_hand(hole, board)
print('{0:.50f}'.format(score))
print("SCORE = >>", score)

    p = "A Spades".split()

    p[1] = p[1][0] .lower()
"""
    
    


