import pytesseract as tess
import cv2
from tkinter import *
import pyttsx3
import numpy as np
import  speech_recognition as sr
from time import sleep , strftime
import time
from multiprocessing.connection import Listener
from click import command
import pywhatkit
from bs4 import BeautifulSoup
import requests
import python_weather
import asyncio
import datetime
from translate import Translator
from utils import *
from matplotlib import pyplot as plt



def Glass_Speak(audio_string):
    engine = pyttsx3.init()
    engine.setProperty('rate', 178)
    voices = engine.getProperty('voices')   
    engine.setProperty('voice', voices[0].id)
    engine.say(audio_string)
    engine.runAndWait()

def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        voice_data = ''
        try :
            voice_data = r.recognize_google(audio, language='fr')
            print(voice_data)
        except sr.UnknownValueError:
            Glass_Speak("")
        except sr.RequestError :
            Glass_Speak("désolé,            verifie ton connection internet")
        return voice_data

def takePic2(voice_data):
    #time.sleep(1)
    thres = 0.5 # Threshold to detect object
    nms_threshold = 0.2 #(0.1 to 1) 1 means no suppress , 0.1 means high suppress 

    cam = cv2.VideoCapture(0)
    cv2.namedWindow('Python Webcam')
    img_counter = 0
    while True :
        ret,frame = cam.read()
        if not ret:
            print ("failed to grab frame")
            break
        cv2.imshow('test',frame)
        k = cv2.waitKey(1)
        if 'détecter les objets' in voice_data or 'déteter' in voice_data or "money" in voice_data or "argent" in voice_data:
            img_name = "open_frame.png"
            img=cv2.imwrite(img_name,frame)
            print("screenshot_taken")
            break

    
        
    cam.release ()
    cv2.destroyAllWindows()

def PicTaking(voice_data):
    Glass_Speak('Prenez le papier et relâchez vos bras')
    #time.sleep(5)
    cam = cv2.VideoCapture(0)
    cv2.namedWindow('Python Webcam')
    img_counter = 0
    while True :
        ret,frame = cam.read()
        if not ret:
            break
        cv2.imshow('test',frame)
        k = cv2.waitKey(1)

        if 'lire' in voice_data:
            img_name = "open_frame.png"
            pic=cv2.imwrite(img_name,frame)
            print("screenshot_taken")
            break

    cam.release ()
    cv2.destroyAllWindows()


def search():
    
    def getdata(url):
        r = requests.get(url)
        return r.text

    search= record_audio()
    url = str("https://fr.wikipedia.org/wiki/"+search)
    htmldata = getdata(url)
    soup = BeautifulSoup(htmldata, 'html.parser')
    data = ''
    for data in soup.find_all("p"):
        print(data.get_text())
        TextToSpeech(data.get_text())


def PicToText():
    
    img = cv2.imread('open_frame.png')
    #cv2.imshow('Simple image',img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    text = tess.image_to_string(img)
    print(text)
    return (text)

def TextToSpeech(text) :
    if text != '':
        
        engine = pyttsx3.init()
        engine.setProperty('rate', 190)
        voices = engine.getProperty('voices')   
        engine.setProperty('voice', voices[0].id)
        engine.say(text)
        engine.runAndWait()


def greeting():
    Glass_Speak("Bonjour,           comment puis-je vous aider ?")

def respond(voice_data):
    if 'lire' in voice_data or 'lire lire' in voice_data :
        Glass_Speak('lire')
        PicTaking(voice_data)
        text = PicToText()
        TextToSpeech(text)
    if 'détecter les objets' in voice_data or 'détecter' in voice_data or 'détecter les objets détecter les objets' in voice_data :
        Glass_Speak('detect les objets')
        takePic2(voice_data)
        tab = detectionObject()
        Glass_Speak ("devont vous il y a,        " + listToString(tab))
    if 'play music' in voice_data or 'musique' in voice_data or 'music' in voice_data or 'play musique' in voice_data:
        Glass_Speak('play music')
        play_music()
    if 'sortie' in voice_data or 'fermer' in voice_data:
        Glass_Speak('sortie')
        Glass_Speak('sil vous plaît restez en sécurité, au revoir')
        exit()
    if 'chercher' in voice_data or 'cherche' in voice_data or 'chercher chercher' in voice_data or 'cherher chercher chercher' in voice_data :
        Glass_Speak('chercher')
        TextToSpeech('sur quoi voulez-vous rechercher')
        search()
    if 'météo maintenant' in voice_data or 'météo maintenant météo maintenant' in voice_data :
        Glass_Speak('météo')
        weather_Now ()
    if 'météo demain' in voice_data : 
        Glass_Speak('météo demain')
        weatherTommorow()
    if "quelle heure est-il" in voice_data:
        time()
    if "quelle est le date de aujourd'hui" in voice_data or "date d'aujourd'hui" in voice_data :
        date()
    if 'merci' in voice_data:
        Glass_Speak("j'ai fais rien")
    if 'quelle est votre nom' in voice_data or 'quelle est ton nom' in voice_data or "comment tu t'appelles" in voice_data or "nom" in voice_data :
        Glass_Speak("je m'appelle Mirou")
    if 'monnaie' in voice_data or 'argent' in voice_data:
        Glass_Speak("detect l'argent")
        takePic2(voice_data)
        money()
    else:
        Glass_Speak('je ne peux pas te comprendre, Veuillez réessayer')        

def time():
    x = datetime.datetime.now()
    Glass_Speak("maintenant c'est" +strftime("%H")+"et"+strftime("%M")+"minutes")

def date():
    x = datetime.datetime.now()
    
    day_names = ["","first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth","eleventh","twelfth","thirteenth","fourteenth","fifteenth","sixteenth","seventeenth","nineteenth","twenty","twenty-one","twenty-second","twenty-third","twenty-fourth","twenty-fifth","twenty-sixth","twenty-seventh","twenty-eighth","twenty-ninth","thirtieth","thirty-first"]
    a=int(x.strftime("%d"))
    b="today is the "+day_names[a]+" of "+x.strftime("%B")+x.strftime("%Y")
    translator= Translator(from_lang="english",to_lang="french")
    trans = translator.translate(b)
    print (trans)
    Glass_Speak(trans)



def detectionObject():
    classNames = []
    with open('coco.names','r') as f:
        classNames = f.read().splitlines()
    print(classNames)

    weightsPath = "frozen_inference_graph.pb"
    configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"

    model = cv2.dnn_DetectionModel(weightsPath,configPath)
    model.setInputSize(320,320)
    model.setInputScale(1.0/ 127.5)
    model.setInputMean((127.5, 127.5, 127.5))
    model.setInputSwapRB(True)

    img = cv2.imread('open_frame.png')

    classIndex, confidece, bbox = model.detect(img,confThreshold = 0.5)

    print (classIndex)
    arr = classIndex.tolist()
    tab = []
    #print(len(classIndex))
    font_scale = 3
    font = cv2.FONT_HERSHEY_PLAIN
    for ClassInd, conf, boxes in zip(classIndex.flatten(),confidece.flatten(), bbox):
        tab.append(str(arr.count(ClassInd)) +" "+ str(classNames[ClassInd-1])+ " ")
    tab = list(dict.fromkeys(tab))
    print (tab)
    return tab

def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str1

def play_music():
   
    def talk(command):
        engine=pyttsx3.init()
        voice=engine.getProperty('voices')
        engine.setProperty('voices',voice[1].id)
        engine.say("playing"+command)
        engine.runAndWait()
 

    def takecommand():
        print("listening")
        Listener = sr.Recognizer()
        mic = sr.Microphone(device_index=2)
        try :
            with mic as source:

                voice=Listener.listen(source)
                command=Listener.recognize_google(voice)
                song=command.replace('play','')
                talk(song)
                pywhatkit.playonyt(song)    
            

        except:
            pass
    takecommand()

def weather_Now (): 
    async def getweather():
        # declare the client. format defaults to the metric system (celcius, km/h, etc.)
        client = python_weather.Client(format=python_weather.IMPERIAL)

        # fetch a weather forecast from a city
        weather = await client.find("Tunis")
        tab = {}
        i=0
        # returns the current day's forecast temperature (int)
        translator= Translator(from_lang="english",to_lang="french")
        trans = translator.translate(str(weather.current.sky_text))
        a="le météo maintenant est "+trans
        b="c'est "+str(int((weather.current.temperature-32)*5/9))+"degré celsius"
        Glass_Speak(a)
        Glass_Speak(b)
        await client.close()
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getweather())


def weatherTommorow () :
    async def getweather():
        # declare the client. format defaults to the metric system (celcius, km/h, etc.)
        client = python_weather.Client(format=python_weather.IMPERIAL)

        # fetch a weather forecast from a city
        weather = await client.find("Tunis")
        tab = {}
        i=0
     # returns the current day's forecast temperature (int)
        for forecast in weather.forecasts:
            tab [i]=( forecast.sky_text, int((forecast.temperature-32)*5/9))
            i+=1
        translator= Translator(from_lang="english",to_lang="french")
        trans = translator.translate(str(tab[1]))
    
        Glass_Speak("la météo de demain est"+trans +"degré celsius")
        await client.close()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getweather())   

def money():
    max_val = 8
    max_pt = -1
    max_kp = 0
    orb = cv2.ORB_create()
    test_img = read_img('open_frame.png')
    original = resize_img(test_img, 0.4)
    display('original', original)
    (kp1, des1) = orb.detectAndCompute(test_img, None)
    training_set = ['files/5.jpg', 'files/5b.jpg', 'files/10-1.jpg', 'files/10.jpg','files/10b_1.jpg', 'files/10b.jpg', 'files/20_1.jpg', 'files/20.jpg','files/20b_1.jpg', 'files/20b.jpg', 'files/50.jpg', 'files/50b.jpg','files/20-2.jpg','files/10 (2).jpg', 'files/10 (3).jpg', 'files/10 (4).jpg', 'files/10 (5).jpg','files/10 (6).jpg', 'files/10 (7).jpg', 'files/10 (8).jpg', 'files/10 (9).jpg','files/10 (10).jpg', 'files/10 (11).jpg', 'files/10 (11).jpg', 'files/10 (12).jpg','files/10 (13).jpg', 'files/10 (14).jpg', 'files/10 (15).jpg', 'files/10 (16).jpg','files/10 (17).jpg', 'files/10 (18).jpg', 'files/10 (19).jpg', 'files/20 (2).jpg','files/20 (3).jpg', 'files/20 (4).jpg', 'files/20 (5).jpg', 'files/20 (6).jpg','files/20 (7).jpg','files/20 (8).jpg', 'files/20 (9).jpg', 'files/20 (10).jpg', 'files/20 (11).jpg','files/20 (12).jpg']

    for i in range(0, len(training_set)):
        # train image
        train_img = cv2.imread(training_set[i])

        (kp2, des2) = orb.detectAndCompute(train_img, None)

        # brute force matcher
        bf = cv2.BFMatcher()
        all_matches = bf.knnMatch(des1, des2, k=2)

        good = []
        # give an arbitrary number -> 0.789
        # if good -> append to list of good matches
        for (m, n) in all_matches:
            if m.distance < 0.789 * n.distance:
                good.append([m])

        if len(good) > max_val:
            max_val = len(good)
            max_pt = i
            max_kp = kp2

        print(i, ' ', training_set[i], ' ', len(good))
    if max_val != 8:
        print(training_set[max_pt])
        print('good matches ', max_val)

        train_img = cv2.imread(training_set[max_pt])
        img3 = cv2.drawMatchesKnn(test_img, kp1, train_img, max_kp, good, 4)
        
        note = str(training_set[max_pt])[6:-4]
        print('\nDetected denomination: Rs. ', note)
            
        if '20' in note :
            Glass_Speak ('vous aver 20 dinar')
        if '10' in note :
            Glass_Speak ('vous aver 10 dinar')
        if '5' in note :
            Glass_Speak ('vous aver 5 dinar')
    else:
	    Glass_Speak("j'ai rien vu, Veuillez réessayer")

#time.sleep(1)
greeting()
while (1):
    voice_data = record_audio()
    respond(voice_data)