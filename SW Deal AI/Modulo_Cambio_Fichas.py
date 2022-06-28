# -*- coding: utf-8 -*-
"""
MODULO QUE RECOGE FICHAS DE LA BANCA Y DEVUELVE EL CAMBIO
"""

from Modulo_Cinematica_Inversa import (CogerItem,DejarItem,MoverBrazo,MoverEje3,MoverBrazo2)
from Modulo_Vision_Computador import *
from Variables_Main import *


# =============================================================================
#                   1. Recoger fichas del jugador
# =============================================================================
def recogerFichasMonton(area):   #Recoge las fichas de 1 jugador y devuelve el Valor total sumado
    global fichasTotales_Banco 

    SumaValorFichas = 0 # valor de retorno
    
    f_inicial = area[0]#325   #100 margen [175: 394, 30 : 258] [250: 410, 170 : 300]
    f_final   = area[1] #425
    c_inicial = area[2]#700  #150 margen
    c_final   = area[3]#850
    
    imageCam = obtenerImagen()
    imageArea = imageCam[f_inicial:f_final,c_inicial:c_final]#get_image()
    
    #imageArea = cv2.imread('IMG_Fichas2.jpg', 1)
    #imageArea = cv2.cvtColor(imageArea,cv2.COLOR_BGR2RGB)
    plt.figure(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k')
    plt.imshow(imageArea)
    
    dimXimageCam = imageCam.shape[1]
    dimYimageCam = imageCam.shape[0]
    # Yolo hasta detectar objetos
    listaResultados = 0
    while listaResultados == 0:
        listaResultados  = valorObjetos(imageArea) #valorObjetos(imageArea[f_inicial:f_final,c_inicial:c_final])
    #return 0
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

    return SumaValorFichas, angulosFichas

# =============================================================================
#                           2. Greedy
# =============================================================================
def solucio(sol, fitxa):
    return sum(sol) == fitxa
import time 
def cambiar_fichas_greedy(fitxa,mode): #esquema greedy
    Candidats = [5,10,25,50,100]
    Sol = []
       
    if mode == 0 and fitxa !=5:
        if fitxa in Candidats:
          Candidats.remove(fitxa)  
        #Candidats.remove(max(Candidats))
    
    while (not solucio(Sol,fitxa) and Candidats!=[]):
        x = max(Candidats)
        if sum(Sol)+x <= fitxa:
            Sol.append(x)
        else:
            Candidats.remove(x)
    if solucio(Sol,fitxa) == True:
        print(Sol,sum(Sol))
        return Sol
    else:
        print("No hay solución")
#canvi = change_chips(50)
        
# =============================================================================
#                       3. Dar cambio al jugador
# =============================================================================
              
def dar_Cambio(cambio, angulosMonton):#xMonton, yMonton): # q es matriz con posiciones donde deja el robot
    global fichasTotales_Banco
    monton = 3 #valor 0 mas bajo para dejar fichas
    for num in cambio:
        # movemos brazo a poicion de la ficha en la banca
        print('Moviendo brazo a pos de ficha con valor:', num, ' ----------')
        if num == 50:
            MoverBrazo(posFichas['rojo']['x'], posFichas['rojo']['y'])
            fichasTotales_Banco['rojo']-=1
            
        elif num == 25:
            MoverBrazo(posFichas['verde']['x'], posFichas['verde']['y'])
            fichasTotales_Banco['verde']-=1
            
        elif num == 10:
            MoverBrazo(posFichas['azul']['x'], posFichas['azul']['y'])
            fichasTotales_Banco['azul']-=1
            
        elif num == 100:
            MoverBrazo(posFichas['negro']['x'], posFichas['negro']['y'])
            fichasTotales_Banco['negro']-=1
            
        elif num == 5:
            MoverBrazo(posFichas['blanco']['x'], posFichas['blanco']['y'])
            fichasTotales_Banco['blanco']-=1
            

        time.sleep(2)
        # bajamos brazo
        MoverEje3(posMaxInferior) #MoverEje3(-dist_object()+0.01)
        time.sleep(2)
        # cogemos ficha
        CogerItem()
        time.sleep(2)
        # subimos brazo
        MoverEje3(posMaxSuperior)
        time.sleep(2)

        # mover a posicion x,y donde estaba el monton de fichas
        MoverBrazo2(angulosMonton[0],angulosMonton[1],angulosMonton[2]) #MoverBrazo(xMonton,yMonton)
        time.sleep(2)
        # bajamos brazo
        f = (monton) * 0.006
        time.sleep(2)
        MoverEje3(posMaxInferior) #MoverEje3(-(0.084-f))
        time.sleep(2)
        # dejamos ficha
        DejarItem()
        time.sleep(2)
        # subimos brazo
        MoverEje3(posMaxSuperior)
        time.sleep(2)
            
        
        monton+=1
    