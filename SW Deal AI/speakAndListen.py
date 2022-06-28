    # -*- coding: utf-8 -*-

#para escuchar
import speech_recognition as sr

#para hablar
from gtts import gTTS
import os
from playsound import playsound

######################### text to speak
def hablar(mytext):
    language = 'es' #English: en
    filename = "textoo.mp3"
    
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save(filename)
    playsound(filename)
    os.remove(filename) #remove file


######################### speak to text
def escucharJugador():
    r = sr.Recognizer() 
    mic= sr.Microphone()
    
    #print(sr.Microphone.list_microphone_names())
    mic = sr.Microphone(device_index=1)
    
    #escuchamos jugador
    with mic as source:
        try:
            print("Di algo: ")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        except sr.UnknownValueError:
            print("Google Speech Recognition no ha entendido lo que has dicho")
        except sr.RequestError as e:
            print("No se pudieron solicitar los resultados del servicio de reconocimiento de voz de Google; {0}".format(e))
        
    print("Deja de hablar - pasando a texto")
    
    #lo pasamos a texto
    #catala: ca-ES | Espanyol: es-ES | ingles reino unido: en-GB | ingles estados unidos: en-US
    txt =  ""
    try:
        #Esta linea se puede cambiar para usar API de google a lo SM
        txt = r.recognize_google(audio, language="es-ES")
        print("Texto: " + txt) 
    except:
        print("Audio escuchado no contiene palabras")
    
    return txt

