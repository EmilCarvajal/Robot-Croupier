#!/usr/bin/env python
# coding: utf-8

# IMPORTS 
import sys 
# importamos las librerías necesarias
import numpy as np
import sympy as sp
import cv2                      # opencv
import matplotlib.pyplot as plt # pyplot
from sympy import *
from sympy.physics.vector import init_vprinting
import time
from math import *
import math as mt
 
from Variables_Main import *

# control arduino
import serial

arduino = 1

if (arduino != 0):
    serialArduino = serial.Serial("COM18",9600)



# In[1]:

"""
init_vprinting(use_latex='mathjax', pretty_print=False)
from sympy.physics.mechanics import dynamicsymbols
theta1, theta2, theta4, d3, lc, la, lb, l4, theta, alpha, a, d = dynamicsymbols('theta1 theta2 theta4 d3 lc la lb l4 theta alpha a d')
theta1, theta2, theta4, d3, lc, la, lb, l4, theta, alpha, a, d 
"""

# In[2]:
def sortJugadores(arr):
    if arr[2] <= 0:
        return arr[2]
    else:
        return arr[0]

def posicionJugadores(numJugadores):
    r=0.4
    points = []
    lado = int(numJugadores/2)
    angulo = np.pi/(2*(lado + 1))
    for index in range(lado):
        points.append([round(r*cos((index+1)*angulo), 4), round(r*sin((index+1)*angulo), 4), (index+1)*angulo])
        points.append([round(r*cos((index+1)*angulo), 4), -round(r*sin((index+1)*angulo), 4), -(index+1)*angulo])
    if numJugadores%2 == 1:
        points.append([round((r)*cos(0), 4), round(r*sin(0), 4), 0])
    points.sort(reverse=True, key=sortJugadores)
    return points


# In[3]: MOVER BRAZO

largo1 = 20
largo2 = 20
#angulo1,angulo2, angulo4
Pi = 3.14159

global gradosAnteriores 
gradosAnteriores = [90,180,0,0]

def distancia( x,  y) :
    """
    Calcula la distancia de un punto al origen (eje del robot).

    Parameters
    ----------
    x : Valor de un costado
    x : Valor de otro costado

    Returns
    -------
    Raiz quadrada
    """
    return sqrt(x*x + y*y)


def radianesAGrados(radianes):
    return radianes * 180.0 / Pi


def leyDelCoseno( A,  B,  C):
    div = (A*A + B*B - C*C) / (2*A*B)
    if (div < -1.0):
        div = -1.0
    if(div > 1.0):
        div = 1.0
   
    return acos(div)


def calculate( x,  y):
    dist = distancia(x, y)
    D1 = atan2(y, x)
    D2 = leyDelCoseno(dist, largo1, largo2)
    a1Radianes = D1 + D2
    a2Radianes = leyDelCoseno(largo1, largo2, dist)  
     
    angulo1 = radianesAGrados(a1Radianes)
    angulo2 = radianesAGrados(a2Radianes)
    
    # calculamos angulo del manipulador: siempre en 0 lado derecho, siempre 180 lado izquierdo
    difX = (angulo1 - gradosAnteriores[0])
    difY = (angulo2 - gradosAnteriores[1])
    difXY = difX + difY
    angulo4 = gradosAnteriores[2];
    
    if(gradosAnteriores[0] > 90 and angulo1 <= 90): # de izquierda a derecha
        difXY = -difXY
        
    angulo4 = angulo4-difXY
    
    if(angulo4<0):
        angulo4 = angulo4 + 180
    if(angulo4 >180):
        angulo4 = angulo4 - 180
        
    angulo1 = round(angulo1,1); 
    angulo2 = round(angulo2,1);
    angulo4 = round(angulo4,1);
  
    print("Eje 1: ", angulo1, " grados")
    print("Eje 2: ", angulo2, " grados")
    print("Eje 4: ", angulo4, " grados")
    
    return int(angulo1), int(angulo2), int(angulo4)


def MoverBrazo(x, y):
    """
    obtiene los angulos que tiene que mover el robot y se lo envia al arduino
    el angulo 4 corresponde al angulo del manipular que gira las cartas
    """
    global gradosAnteriores 
    print('Moviendo a posiciones XY: ',x,',',y,' -------')

    angulo1, angulo2, angulo4 = calculate(x,y)
    
    # ordenes a arduino
    time.sleep(3)
    cad = "s,1," + str(angulo1)
    serialArduino.write(cad.encode('ascii'))
    time.sleep(2)
      
    cad = "s,2," + str(angulo2)
    serialArduino.write(cad.encode('ascii'))
    time.sleep(2)
      
    cad = "s,4," + str(angulo4)
    serialArduino.write(cad.encode('ascii'))
    time.sleep(2)
    
    gradosAnteriores[0] = angulo1
    gradosAnteriores[1] = angulo2
    gradosAnteriores[2] = angulo4
    
    #serialArduino.close()
    
    return angulo1, angulo2, angulo4

def MoverEje3(posZ):
    print('Moviendo a posicion z: ',posZ,' -------')
    
    # ordenes a arduino
    cad = "s,3," + str(posZ)
    serialArduino.write(cad.encode('ascii'))
    time.sleep(2)
    
def MoverEje4(angulo4):
    
    print('Girando manipulador: ',angulo4,' grados -------')

    ang4Anterior = gradosAnteriores[2]
    if(ang4Anterior + angulo4 >180):
        angulo4 = ang4Anterior - angulo4
    else:
        aux_angulo4 = ang4Anterior + angulo4
        if aux_angulo4 < 0: # casos de -45 ==> -(-45) = 45
            angulo4 = ang4Anterior - angulo4
        elseangulo4 = aux_angulo4
            
    print('Grados servomotor real: ',angulo4)
        
    # ordenes a arduino
    cad = "s,4," + str(angulo4)
    serialArduino.write(cad.encode('ascii'))
    
    gradosAnteriores[2] = angulo4
    
    time.sleep(2)

def MoverBrazo2(angulo1, angulo2, angulo4):
    """
    Obtiene los angulos que tiene que mover el robot y se lo envia al arduino
    el angulo 3 corresponde al angulo del manipular que gira las cartas
    """
    
    # ordenes a arduino
    time.sleep(2)
    cad = "s,1," + str(angulo1)
    serialArduino.write(cad.encode('ascii'))
    time.sleep(2)
      
    cad = "s,2," + str(angulo2)
    serialArduino.write(cad.encode('ascii'))
    time.sleep(2)
      
    cad = "s,4," + str(angulo4)
    serialArduino.write(cad.encode('ascii'))
    
    gradosAnteriores[0] = angulo1
    gradosAnteriores[1] = angulo2
    gradosAnteriores[2] = angulo4
    
    #serialArduino.close()
    
    return angulo1, angulo2, angulo4


    
# In[4]: COGER / DEJAR ITEM CON LA VENTOSA

def Distancia():
    cad = "d"
    serialArduino.write(cad.encode('ascii'))
    time.sleep(2)
    return 0

def CogerItem():
    cad = "c"
    serialArduino.write(cad.encode('ascii'))
    time.sleep(2)
    return 0

def DejarItem():
    cad = "d"
    serialArduino.write(cad.encode('ascii'))
    time.sleep(2)    
    return 0


# In[5]: STANDBY
def Standby():
    """
    Funcion que se encarga de colocar el brazo en posición de 'Stanby'

    Returns
    -------
    None.

    """
    
    MoverBrazo(posStandby['x'], posStandby['y'])
    MoverEje3(posStandby['z'])

# In[6]: GESTION DE LAS CARTAS

def CogerCarta(x,y,distEje3,angEje4):
    """
    Secuencia de movimientos para recoger una carta.

    Parameters
    ----------
    x : Posición X.
    y : Posición Y.
    distEje3 : Posición Z (altura).
    angEje4 : Oridentación de la carta. Angulo del manipulador.

    Returns
    -------
    None.

    """
    # mover a posicion x,y
    MoverBrazo(x,y)
    time.sleep(3)
    # colocar eje 4 angulo baraja...
    MoverEje4(angEje4)
    time.sleep(2)
    # bajamos brazo
    MoverEje3(distEje3)
    time.sleep(4)
    # cogemos carta
    #CogerItem()
    #time.sleep(3)
    # subimos brazo
    MoverEje3(posMaxSuperior)
    time.sleep(4)
    # recolocar eje 4 pos inicio
    MoverEje4(-angEje4)
    time.sleep(1) 


def DejarCarta(x, y, distEje3, angEje4):
    # mover a posicion x,y
    MoverBrazo(x,y)
    time.sleep(3)
    # colocar eje 4 angulo a dejar
    MoverEje4(angEje4)
    time.sleep(2)
    # bajamos brazo
    MoverEje3(distEje3)
    time.sleep(2)
    # dejamos carta
    DejarItem()
    time.sleep(3)
    # subimos brazo
    MoverEje3(posMaxSuperior)
    time.sleep(2)
    # recolocar eje 4 pos inicio
    MoverEje4(-angEje4)
    time.sleep(1)

    
def quemarCarta():
    global cartasQuemadas
    global cartasReveladas
    
    # coger carta baraja
    #retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0543 -(0.0007 * cartasReveladas), sim.simx_opmode_oneshot)
    CogerCarta(posBaraja['x'], posBaraja['y'], posBaraja['z'], posBaraja['angulo4'])
    cartasReveladas = cartasReveladas + 1
    time.sleep(2)
    
    # dejar carta en posicion de cartas quemadas 

    #retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0745 + (cartasQuemadas*0.0007), sim.simx_opmode_oneshot)
    DejarCarta(posCartasQuemadas['x'], posCartasQuemadas['y'], posCartasQuemadas['z'], posCartasQuemadas['angulo4'])
    cartasQuemadas = cartasQuemadas + 1
    time.sleep(2)
    
# In[8]: COLOCAR CARTAS CENTRALES

def ColocarCartaCentral(x,y,z, angulo4):
    global cartasReveladas
    # coger carta baraja
    #retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0543 -(0.0007 * cartasReveladas), sim.simx_opmode_oneshot)
    CogerCarta(posBaraja['x'], posBaraja['y'], posBaraja['z'], posBaraja['angulo4'])
    cartasReveladas = cartasReveladas + 1
    time.sleep(2)
    
    # dejar carta en flipeador
    DejarCarta(posFlipeador['x'], posFlipeador['y'],posFlipeador['z'], posFlipeador['angulo4'])
    time.sleep(2)
    
    # coger carta en bandeja
    CogerCarta(posBandeja['x'], posBandeja['y'],posBandeja['z'], posBandeja['angulo4'])
    time.sleep(2)
    
    # dejar carta en su posición del centro
    DejarCarta(x, y, -0.12, 90)
    time.sleep(2)
           
def Colocar3CartasCentrales():
                          
    for numCard in range(3):
        x = -15.2 + (numCard*6.95)#-0.152 + (numCard*0.0695)
        y = 19#0.19
        
        ColocarCartaCentral(x, y, -0.12, 90)


def Colocar4CartaCentral():
    x = -0.152 + (3*0.0695)
    y = 0.19
    
    ColocarCartaCentral(x, y, -0.12, 90)
        

def Colocar5CartaCentral():
    x = -0.152 + (4*0.0695)
    y = 0.19
    
    ColocarCartaCentral(x, y, -0.12, 90)
        

# In[9]: REPARTIR CARTAS

def darCartaJugador(x, y, angulo):
    valY = [round(0.4*mt.cos(angulo+(np.pi/34)), 4), round(0.4*mt.cos(angulo-(np.pi/34)), 4)]
    valX = [round(0.4*mt.sin(angulo+(np.pi/34)), 4), round(0.4*mt.sin(angulo-(np.pi/34)), 4)]
    print(valY)
    print("-----")
    print(valX)
    #z = 0.2

    global cartasReveladas         
    for i in range(2):
        print("valX[i]: ", valX[i])
        print("valY[i]: ", valY[i])
        print("valX[i]/valY[i]: ", valX[i]/valY[i])
        angulo4 = int(round(np.arctan(valX[i]/valY[i]),1)) # alpha = arcsin(b/a)
        print('x' + str(i+1))
 
        # coger carta baraja
        #retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0543 -(0.0007 * cartasReveladas), sim.simx_opmode_oneshot)
        CogerCarta(posBaraja['x'], posBaraja['y'], posBaraja['z']+(0.0007 * cartasReveladas), posBaraja['angulo4'])
        cartasReveladas = cartasReveladas + 1
        time.sleep(2)
        
        # dejar carta en area de jugador
        DejarCarta(valX[i]*100, valY[i]*100, posMaxInferior, angulo4)
        time.sleep(2)

