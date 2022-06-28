# -*- coding: utf-8 -*-

"""
MODULO QUE RECOJE LAS FICHAS DE 1 JUGADOR APILADAS EN UNA ZONA
"""
from Variables_Main import *
####################################################
from Modulo_Vision_Computador import *
############################################
"""
global n_FAzul;      n_FAzul = 8
global n_FVerdes;    n_FVerdes = 8
global n_FVermelles; n_FVermelles = 8
global n_FBlanques;  n_FBlanques = 8
global n_FNegres;    n_FNegres = 8
"""

#areas5jug = [[250, 410, 680 , 880],[150 , 300 , 600,780 ],
            # [160,260, 420,600],[150 , 300 , 258,415 ],[250, 410, 170 , 300]]
"""
AREAS DONDE SE VEN LAS CARTAS DE CADA: 5JUGADORES (PARA JOFRE)
j1 = [175, 410, 780 , 1012]
j2 = [20 , 250 , 630,860 ]
j3 = [20,200, 400,640]
j4 = [20 , 250 , 180,420 ]
j5=  [175, 394, 30 , 258]

"""
"""
#areas para cambio de fichas
areas5jug=[[300, 410, 710 , 850], #710 mod, de 680     
           [190 , 281 , 600,740 ] , #281 mod, de 300
           [160,260, 420,600],
           [200 , 300 , 320,415 ], #200 mod, de 210
           [280, 410, 210 , 300]]
"""
"""
c1=  [250, 410, 170 , 300]
c2 = [150 , 300 , 258,415 ]
c3 = [160,260, 420,600]
c4 = [150 , 300 , 600,780 ]
c5 = [250, 410, 680 , 880]
fn = c2
"""

from matplotlib import pyplot as plt
import cv2 as cv2
#import math
import sympy as sp
from sympy import *


def recogerFichasMonton(area):   #Recoge las fichas de 1 jugador y devuelve el Valor total sumado
    global fichasTotales_Banco 

    SumaValorFichas = 0 # valor de retorno
    
    f_inicial = area[0]#325   #100 margen [175: 394, 30 : 258] [250: 410, 170 : 300]
    f_final   = area[1] #425
    c_inicial = area[2]#700  #150 margen
    c_final   = area[3]#850
    
    imageCam = obtenerImagen()
    imageArea = imageCam#[f_inicial:f_final,c_inicial:c_final]#get_image()
    
    #imageArea = cv2.imread('IMG_ASpades.jpg', 1)
    #imageArea = cv2.cvtColor(imageArea,cv2.COLOR_BGR2RGB)
    plt.figure(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k')
    plt.imshow(imageArea)
    return 0
    dimXimageCam = imageCam.shape[1]
    dimYimageCam = imageCam.shape[0]
    # Yolo hasta detectar objetos
    listaResultados = 0
    while listaResultados == 0:
        listaResultados  = valorObjetos(imageArea) #valorObjetos(imageArea[f_inicial:f_final,c_inicial:c_final])
    
    angulosFichas =[0,0,0] # angulos que se enviaran al modulo de coger las fichas de la banca y colocarlas en el area del jugador
    
    if listaResultados == []: 
        return 0
    
    for objeto in listaResultados:
        colorFicha = objeto[0]
        cx = objeto[1]
        cy = objeto[2]
        
        # CALCULO: posiciones X,Y reales
        base = 0
        position = 0
        if c_inicial +cx >= dimXimageCam/2:
            base = c_inicial - dimXimageCam/2 
            position = 1
        else:
            base = c_inicial
        
        xi = ((base+ cx)) 
        yi = (f_inicial)+cy  
        
        if position ==1: #derecha
            x = N(xi*cmTablero/(dimXimageCam/2),3)  
        else:  #izquierda
            x = -N(cmTablero-xi*cmTablero/(dimXimageCam/2),3) 
            
        y = N(cmTablero-yi*cmTablero/dimYimageCam,3)
        
        print("xImg:",xi, "yImg:", yi)
        print("xReal:",x, "yReal:", y)
        
        #return 0
    
        # SECUENCIA DE MOVIMIENTO: cambio de fichas
        # movemos brazo donde se encuentran las fichas y guardamos los angulos
        angulosFichas[0],angulosFichas[1],angulosFichas[2] = MoverBrazo(x,y)
        time.sleep(2)
        # bajamos brazo
        MoverEje3(posMaxInferior)  #MoverEje3(-dist_object()+0.084) 
        time.sleep(2)
        # cogemos ficha
        CogerItem()
        time.sleep(2)
        # subimos brazo
        MoverEje3(distAlta)
        time.sleep(2)
        
        count_c = 0
        # mover brazo a posicion de ficha en banco
        MoverBrazo(posFichas[colorFicha]['x'], posFichas[colorFicha]['y'])
        # obtener fichas totales de ese color en el banco
        count_c = fichasTotales_Banco[colorFicha]
        # acumular suma de valor de las fichas que se recogen
        SumaValorFichas = SumaValorFichas + valorFichas[colorFicha]
        # actualizar numero de fichas en banco
        fichasTotales_Banco[colorFicha]+=1
        
        # bajamos brazo
        f = (count_c+1) * 0.5
        time.sleep(2)
        MoverEje3(-(9.0-f))
        time.sleep(2)
        # dejamos ficha
        DejarItem()
        time.sleep(2)
        # subimos brazo
        MoverEje3(posMaxSuperior)
        time.sleep(2)

        """
        #subir_brazo(0.13) 
        subir_brazo(0.0)
        time.sleep(3)
        f = (count_c+1) * 0.005
        print(count_c)
        time.sleep(2)
        bajar_brazo(-(0.090-f))
        time.sleep(5)
        DejarItem()
        time.sleep(3)
     
        subir_brazo(0.0)
        """
             
    return SumaValorFichas, angulosFichas

recogerFichasMonton([0,400,0,500])

#a,v = recogerFichasMonton(areas5jug[1])

#a,c = recogerFichasMonton(areas5jug[1]) 
#s =3