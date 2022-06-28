# -*- coding: utf-8 -*-
#areas para cambio de fichas
areas5jug=[[300, 410, 710, 850], #710 mod, de 680     
           [190, 281, 600, 740], #281 mod, de 300
           [160, 260, 420, 600],
           [200, 300, 320, 415], #200 mod, de 210
           [280, 410, 210, 300]]

#VARIABLES CONSTANTES:
global blanco; blanco = 0
global negro; negro = 1
global rojo; rojo = 2
global verde; verde = 3
global azul; azul = 4
global rotationCentro
global posFichas

cam_port = 0 # modulo de VC en teoria es 1 para la webcam externa
cmTablero = 50 # modulo de cambio: recoger monton

#VARIABLES GLOBALES:
    
#rotationCentro = [90, 82.5, 68, 49, 28.35]
rotationCentro = [90, 82.5, 65, 43.45, 21]
#-- cartas
global cartasTotales
cartasTotales = 19
global cartasReveladas
cartasReveladas = 0
global cartasQuemadas
cartasQuemadas=0

#-- fichas
global fichasTotales_Banco, fichasTotales_Jug
#fichasTotales_Banco = {blanco: 8, negro: 8, rojo: 8, verde: 8, azul: 8}
fichasTotales_Jug = {blanco: 3, negro: 3, rojo: 3, verde: 3, azul: 3}
fichasTotales_Banco={
    "blanco" : 8,
    "negro"  : 8,
    "rojo"   : 8,
    "verde"  : 8,
    "azul"   : 8,
}
valorFichas={
    "blanco" : 5,
    "negro"  : 100,
    "rojo"   : 50,
    "verde"  : 25,
    "azul"   : 10,
}

# POSICIONES DE OBJETOS EN MESA Y STANDBY
posMaxInferior = 12
posMaxSuperior = 20 # seria 25 en vd

posStandby = { #    x = -0.0895 y = 0.0 z = 0.2
    'x' : 20,#0,    
    'y' : -20,#10,
    'z' : posMaxSuperior,
    'angulo4' : 90
}

posFichas = {
    "blanco" : {'x' : -40,    'y' : 0.0},
    "negro"  : {'x' : -27.7,  'y' : 0.0},
    "rojo"   : {'x' : -33.95, 'y' : 0.0},
    "verde"  : {'x' : -21.45, 'y' : 0.0},
    "azul"   : {'x' : -15.2,  'y' : 0.0},
}

posBaraja = { #(0.275, 0.05, -0.12, 90)
    'x' : 20,    
    'y' : 10,
    'z' : 13, #posMaxInferior,
    'angulo4' : 90
}

posFlipeador={ #(0.383, 0.082, -0.12, 90)
    'x' : 38.3,    
    'y' : 8.2,
    'z' : posMaxInferior,
    'angulo4' : 0
}

posBandeja={ #(0.275, -0.018, -0.12, 90)
    'x' : 27.5,    
    'y' : 1.8,
    'z' : posMaxInferior,
    'angulo4' : 0
}

posCartasQuemadas={ # x = 0.1565 y = 0.05, ang4 = 90
    'x' : 15.65,    
    'y' : 5,
    'z' : posMaxInferior,
    'angulo4' : 0
}


