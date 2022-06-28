# -*- coding: utf-8 -*-

from Variables_Main import *

import torch

import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv2
#import math
import sympy as sp
from sympy import *
import pandas as pd

import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

renombrarColoresYolo={
    'Black Chip': "negro", 
    'Red Chip'  : "rojo" , 
    'Green Chip': "verde", 
    'Blue Chip' : "azul" , 
    'White Chip': "blanco" 
}

def obtenerImagen():
    cam = cv2.VideoCapture(cam_port,cv2.CAP_DSHOW)
    cont =0
    while(True):
        result, image = cam.read()
        #cv2.imshow('frame',image)
        if cont == 3: #cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cont+=1
        
    #cam.release()
    #cv2.destroyAllWindows()
    img_Robot = 0
    if result:
        print("imge.shape: ", image.shape)
        imge=np.array(image,dtype=np.uint8)
        imge.resize(imge.shape)

        img_Robot = cv2.cvtColor(imge,cv2.COLOR_BGR2RGB)
        alpha = 1.1 # Contrast control (1.0-3.0)
        beta = 30 # Brightness control (0-100)
        #img_Robot =  0.59 * img_Robot + 100
        img_Robot = cv2.convertScaleAbs(img_Robot, alpha=alpha, beta=beta)
        return img_Robot
    
    else:
        print("No image detected. Please! try again")
        return 0

def valorObjetos(imageArea):
    model = torch.hub.load('C:/Users/jiaye/Documents/UNI/4R CURSO S2/TFG/SOFTWARE/yolov5-master'
                           ,'custom'
                           , path='C:/Users/jiaye/Documents/UNI/4R CURSO S2/TFG/SOFTWARE//best.pt'
                           , source='local')  # local repo    

    # Inference
    results = model(imageArea)
    # si no hay resultados
    if (len(results.xyxy[0].size()) == 0) :
        print( "YOLO: no se han reconocido objetos" )
        return 0
    # si hay resultados
    
    # mostramos objetos detectados 
    results.show()
    #plt.figure(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k')
    #plt.imshow(results.show())
    
    print("------YOLO results ------------------")
    print( (results.pandas().xyxy[0]) )
    print("------results ------------------")
    #          xmin        ymin        xmax        ymax  confidence  class      name
    # 0   76.567413   65.968002  323.587097  367.914581    0.948060     39  A Spades
    # to acces: .iloc[0]['name']

    # convertimos pandas data en un un diccionario
    dicResultados = (results.pandas().xyxy[0]).to_dict('index')
    
    listaResultados = []

    for clave in dicResultados.keys():                      
        nombreObjeto = dicResultados[clave]["name"]
        # si los objetos detectados son fichas, renombramos ("Green chip" => "verde")
        if nombreObjeto in renombrarColoresYolo.keys():
            dicResultados[clave]["name"] = renombrarColoresYolo[nombreObjeto]
        
        # return [nombre y posicion centro ]
        cx = (dicResultados[clave]["xmax"] + dicResultados[clave]["xmin"])/2
        cy = (dicResultados[clave]["ymax"] + dicResultados[clave]["ymin"])/2
        listaResultados.append([dicResultados[clave]["name"], cx,cy])

        
    print("Num objetos obtenidos: ",len(listaResultados))

    print("------YOLO results ------------------")
    
    return listaResultados  #["azul",640,480]

