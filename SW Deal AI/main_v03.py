# -*- coding: utf-8 -*-

# =============================================================================
#                               IMPORTS 
# =============================================================================
# imports geenrales
import random
from functools import partial
import sys 
# modulo de reconocimiento de voz
import speakAndListen as sl
# modulo de cambio
from Modulo_Cambio_Fichas import *
# modulo cinematica inversa
from Modulo_Cinematica_Inversa import *
# modulo de la mano del jugador (cartas y combos)
from Modulo_Mano_Jugador import *
# variabless Compartidas
from Variables_Main import *

# =============================================================================
#                        VARIABLES GLOBALES MAIN
# =============================================================================
global nJug; nJug = 1
global dealer; dealer = 1

# =============================================================================
#                               UTILS MAIN
# =============================================================================

def num_players(n):
    global nJug; nJug = n
    global endBucle; endBucle = True
    
def num_dealer(n):
    global nJug;
    global dealer; 
    if n == 0:
        n = random.randint(1, nJug)
        dealer = n
    if n > nJug:
        error_num_players()
    else:
         dealer = n
        #global endBucle; endBucle = True
    
def error_num_players():
    sl.hablar("Numero de jugadores incorrecto")
    #sl.hablar("Han de haber entre 1 y 4 jugadores")

switch_players = {
    "dos" : partial(num_players, 2),
    "tres" : partial(num_players, 3),
    "cuatro" : partial(num_players, 4),
    "cinco" : partial(num_players, 5),
}

def switch_dealer(txt): 
    num = -1
    if txt =="uno" : num = 1
    elif txt =="dos" : num = 2
    elif txt =="tres" : num = 3
    elif txt =="cuatro" : num = 4
    elif txt =="cinco" : num = 5
    elif txt =="aleatorio" : num = 0
    if num != -1:
        num_dealer(num)
    else: error_num_players()

def condWildRonda(listaHanJugado): 
    for x in listaHanJugado:
        if x == False:
            return False
    return True

def main_cambio(modo,actual_j):
    sl.hablar("Coloca tus fichas de cambio ")
    time.sleep(4)
    valor_fichas, posicion= recogerFichasMonton(areas5jug[actual_j-1])  
    if valor_fichas!=0: 
        l_cambio = cambiar_fichas_greedy(valor_fichas,modo) #modo 0 o 1                   
        dar_Cambio(l_cambio, posicion) 
        time.sleep(6)
    else: 
        print("Error Nsolve")
        sl.hablar("Error Nsolve")
        
def finalizar_poker():
    sl.hablar("POKER FINALIZADO")
    print("----POKER FINALIZADO----")
    sys.exit()
    
# =============================================================================
#                               MAIN
# =============================================================================

def main():
    global nJug;
    global dealer; 
    sl.hablar("Buenos dias")
    opciones_jug = ["tres","cuatro","cinco"]
    opciones_del = ["uno","dos","tres","cuatro","cinco","aleatorio"]
    
    # determinar num. jugadores 'nJug'
    txt = 0
    sl.hablar("Numero de jugadores?")
    while txt not in opciones_jug:
        txt = sl.escucharJugador()
        switch_players.get(txt, error_num_players)()
        
    # determinar dealer
    sl.hablar("Quien será el díler?")
    txt = 0
    while txt not in opciones_del:
        txt = sl.escucharJugador()
    switch_dealer(txt)  
    
    # obtener posciciones de los jugadores 
    pos_j = posicionJugadores(nJug); 
    
    # colocar brazo en posicon de inicio
    Standby()

    
    # determinar ciegas
    ciega_pequeña = 10
    ciega_grande = 2*ciega_pequeña

    # inicializar lista de posibles dealers i su iterador
    dealers_p = [x for x in range(1,nJug+1)]
    d_it = dealer-1

    # inicializar mano, ganador de partida y las posibles ordenes a acatar
    MANO = 0
    ganadorP = False
    opciones = ["paso","voy","me retiro","subo","check","lo veo"
                ,"siguiente", "cambio a la alta","cambio a la baja"
                ,"abandono", "retiro", "finalizar juego"
               ]
    opciones_info = [ "ronda actual","mano actual","dealer actual"
                     ,"hola dealer", "quién es la ciega grande"
                     ,"turno actual","apuesta máxima"
                     ,"cantidad ciega pequeña" ,"cantidad ciega grande"
                    ]
    # determinar cantidades de pujas
    opciones_subir = [ str(5*x) for x in range(1,101)] # numeros multiples de 5

    sl.hablar( "La ciega pequeña es de "+str(ciega_pequeña) +" i la grande de "+str(ciega_grande) )
    
    # =============================================================================
    #                       BUCLE ENORME  DE MANOS 
    # =============================================================================
    while ( MANO < 3 and ganadorP == False ):
        # actualizar CIEGAS cada 4 RONDAS 
        if MANO%4 == 0 and MANO != 0:
            ciega_pequeña = ciega_grande
            ciega_grande = 2*ciega_pequeña
            sl.hablar("Se han actualizado las ciegas")
            sl.hablar("La ciega pequeña es de"+str(ciega_pequeña)+" i la grande de"+str(ciega_grande))

        # información de partida    
        print("DP:", dealers_p)
        sl.hablar("MANO " +str(MANO))
        print("MANO: ",MANO,"-------------------------")
        
        # inicializar RONDA
        Ronda= 0
        
        players_p = dealers_p.copy() 
        #players_p= [2,3]
        sl.hablar("El dÍler es el jugador" +str(dealer))
        
        # INICIO ---------    
        txt =0; next_j = 0

        # ----------- DETERMINAR QUIEN EMPIEZA ----- el +3 del de la pos del dealer o el +1 de la pos del dealer
        dealer_index = dealers_p.index(dealer)
        
        jugador_empieza_r0 = -1
        pos_cg = -1
        if len(dealers_p) == 2: # si solo hay 2 jugadores
            jugador_empieza_r0 = dealers_p[1]
            if dealer_index == 1:
                jugador_empieza_r0 = dealers_p[0]
            pos_cg = dealer_index # La ciega grande es el propio Dealer
        else:                  
            pos = dealer_index +3 
            if  pos >= len(dealers_p): # +1 ciega peque, +2 ciega grande, empieza +3
                pos = pos - len(dealers_p) 
    
            jugador_empieza_r0 = dealers_p[pos]
                
            #--------ciega grande -1 pos de  next_j o +2 pos del Dealer NO HACER CASO
            pos_cg = pos-1 
            if pos -1 < 0:
                pos_cg = len(dealers_p)-1
        #--------
        jugador_izquierda=-1
        if dealer_index +1 == len(dealers_p):
            jugador_izquierda = dealers_p[0]
        else:
            jugador_izquierda = dealers_p[dealer_index +1]
        ji_ind =dealer_index #jug izquierda index inicial 
        next_j = jugador_empieza_r0
        ganadorR = False
        
        # =============================================================================
        #                       BUCLE DE RONDAS 
        # =============================================================================
        
        apuesta_max_jug = ciega_grande
        while( Ronda < 4 and ganadorR == False ): 
            
            sl.hablar("RONDA  " +str(Ronda))
            print("RONDA: ",Ronda,"--------------")
            if Ronda != 0:  next_j = jugador_izquierda #jugador izuiqerda de dealer o si ha abandonado este, el siguiente
            it = players_p.index(next_j) 
            ha_jugado = [False for x in range(1,len(players_p)+1)]
            #--------
            
            # control de rondas
            if Ronda == 0:#a = 0
                sl.hablar(" el jugador " +str(dealers_p[pos_cg])+ " es la ciega grande")
                sl.hablar("Preparando tablero, no obstaculicen la zona de juego")
                
                # ---REPARTICION DE CARTAS M0 ---------      
                for p in players_p:                   
                    sl.hablar('DANDO CARTA A JUGADOR '+str(p))
                    darCartaJugador(pos_j[p-1][0],pos_j[p-1][1], pos_j[p-1][2])
                Standby()   

    
            elif Ronda == 1: 
                sl.hablar("Atencion!, Colocando cartas centrales")
                Colocar3CartasCentrales(); 
                Standby()
            elif Ronda == 2: 
                sl.hablar("Atencion!, Colocando carta 4")
                quemarCarta();Colocar4CartaCentral(); Standby()
            elif Ronda == 3: 
                sl.hablar("Atencion!, Colocando carta 5")
                quemarCarta();Colocar5CartaCentral(); Standby()
            
            sl.hablar("empieza el jugador " +str(next_j))

            # =============================================================================
            #                       BUCLE de 1 RONDA
            # =============================================================================
            
            while condWildRonda(ha_jugado) == False:   #txt != "siguiente": # dentro de 1 mano
                txt = 0
                sl.hablar("Turno del jugador " +str(next_j))
                actual_j = next_j
                print("- ...........")
                print("- TURNO DEL JUGADOR: ",actual_j)
                actual_j_pos = it #-1 por la pos de la lista
                print("actual_j_pos: ", actual_j_pos)
                
 
                while txt not in opciones:
                    txt = input('option: ')#sl.escucharJugador()
                #--- Informacion de Juego ---
                    if txt in opciones_info:
                        info = "none"
                        if txt == "mano actual":
                            info = MANO
                        elif txt == "quién es la ciega grande":
                            info = dealers_p[pos_cg]
                        elif txt == "ronda actual":
                            info = Ronda
                        elif txt == "turno actual":
                            info = actual_j
                        elif txt == "dealer actual":
                            info = dealer
                        elif txt == "apuesta máxima":
                            info = apuesta_max_jug
                        elif txt == "cantidad ciega pequeña":
                            info = ciega_pequeña
                        elif txt == "cantidad ciega grande":
                            info = ciega_grande
                        print("info:" , info)
                        
                        if txt == "hola dealer":
                            sl.hablar("Hola amigo")
                        else:
                            sl.hablar("La respuesta es "+str(info))
                                           
                #---- Cambios ---
                if txt == "cambio a la baja" or txt == "cambio a la alta" :
                    modo = 0
                    if txt == "cambio a la alta": modo = 1
                    main_cambio(modo,actual_j)
                    time.sleep(1); Standby()
                    txt = 0
                    while txt not in opciones:
                        txt = sl.escucharJugador()
                        
                # --- SUBIR APUESTA ---    
                if txt == "subo":
                    sl.hablar("Cuanto subes?")
                    print("Cuanto subes?")
                    while txt not in opciones_subir:
                        txt = input('option: ')# sl.escucharJugador()
                    ha_jugado = [False for x in range(1,len(players_p)+1)] # Reseteamos FALSE a todos
                    apuesta_max_jug = apuesta_max_jug + int(txt)

                #--- RETIRO o ABANDONO ---
                se_ha_retirado = False
                if txt == "me retiro" or txt == "abandono" :
                    #-- Caso retiro, se aplica tambien si se abandona  ----  
                    se_ha_retirado = True
                    players_p.remove(actual_j)
                    ha_jugado.pop(actual_j_pos)
                    print("len: ",len(players_p))
                    if it == len(players_p):
                        next_j = players_p[0]
                        it=0
                    else:
                        next_j = players_p[it]
                    if 1 == len(players_p):
                        sl.hablar("EL GANADOR de la MANO es el jugador "+str(players_p[0]))
                        ganadorR = True
                        break
                    
                    #-- Caso abandono ----    
                    if txt == "abandono":
                        dealers_p.remove(actual_j)

                        if 1 == len(dealers_p):
                            sl.hablar("Ganador del POKER es el jugador "+str(players_p[0]))
                            finalizar_poker()
                            
                    #-- Si abandona el jugador de la izquierda se actualiza jugIz i index
                    if actual_j == jugador_izquierda:
                        if ji_ind +1 == len(players_p):
                            jugador_izquierda = players_p[0]
                        else:
                            jugador_izquierda = players_p[ji_ind +1]
                        ji_ind = players_p.index(jugador_izquierda)
                        
                else:
                    haJugado = True
                    while (haJugado == True):
                
                        if it == len(players_p)-1:  #Actualizar posiciones
                            next_j = players_p[0]
                            it=0
                        else:
                            it+=1
                            next_j = players_p[it]
                            
                        haJugado = ha_jugado[next_j-1]
                    

                # --- FINALIZAR JUEGO ---
                if txt == "finalizar juego":
                    finalizar_poker()
                    
                print("Opcion Jugador: ",txt)
                if se_ha_retirado == False:
                    if txt != "paso":
                        ha_jugado[actual_j_pos] = True
                print("PP:",players_p)
                print("HJ:",ha_jugado)
                time.sleep(1)
                
            if Ronda ==3: #Ronda Final
                sl.hablar("Jugadores, muestren sus cartas ")
                time.sleep(30) # -9.0006e+01   Gamma
                ganador, combo_ganador = decirGanador(players_p,3) #modulo VC+ Algoritmo combinaciones (Jofre)
                sl.hablar("EL GANADOR es el jugador "+str(ganador))
                print("Ganador de Mano:", ganador )
                sl.hablar("EL COMBO GANADOR ES "+str(combo_ganador))
                sl.hablar("Jugador "+str(ganador)+" recoge tus ganacias")
                sl.hablar("Fin de MANO, Recojan las cartas de la mesa")
                time.sleep(6)
                
            Ronda+=1     
        
        if d_it == len(dealers_p)-1:
            dealer = dealers_p[0]
            d_it=0
        else:
            d_it+=1
            dealer = dealers_p[d_it]
        
            
        MANO+=1
    sl.hablar("POKER FINALIZADO")
    print("----POKER FINALIZADO----")
   
    
if __name__ == "__main__":
    main()