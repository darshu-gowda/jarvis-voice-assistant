import pyttsx3
import speech_recognition as sr
import eel
import time
import datetime
import requests
import wikipedia
import webbrowser
import sys
from engine.config import ASSISTANT_NAME
from bs4 import BeautifulSoup
def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source,10,6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
       
    except Exception as e:
        return ""
    
    return query.lower()



@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "on google" in query:
            from engine.features import opengoogle
            opengoogle(query)

        
        # date and time features    
        
        elif "the date" in query:
            query = query.replace(ASSISTANT_NAME, "")
            currentDate = datetime.datetime.now().strftime("%Y-%m-%d")
            speak(f"Sir, today's date is {currentDate}")
        elif "the time" in query:
            query = query.replace(ASSISTANT_NAME, "")
            strTime = datetime.datetime.now().strftime("%H:%M")
            speak(f"Sir, the time is {strTime}")
        elif "the date and time" in query:
            query = query.replace(ASSISTANT_NAME, "")
            currentDateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            speak(f"Sir, the date and time is {currentDateTime}")
       
       
        # about jarvis and about creater
        elif "who are you" in query or "tell me about youself" in query or "your details" in query:
            query = query.replace(ASSISTANT_NAME, "")
            who_are_you = "I am jarvis, an A I based computer program, but i can help you in providing information ,providing weather updates,making phone call,sending message,web searching and lot things !"
            print(who_are_you)
            speak(who_are_you)

        elif 'who make you' in query or 'who made you' in query or 'who created you' in query or 'who develop you' in query:
            query = query.replace(ASSISTANT_NAME, "")
            speak(f"For your information darshan gowda and harish reddy a Created me !")

        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            flag = "H"
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "send message" in query:
                    flag = 'message'
                    speak("what message to send")
                    query = takecommand()
                    
                elif "phone call" in query:
                    flag = 'call'
                else:
                    flag = 'video call'
                    
                whatsApp(contact_no, query, flag, name)

        elif 'wikipedia' in query:
            speak("searching in wikipedia....")
            try:
                query=query.replace("wikipedia","")
                results = wikipedia.summary(query, sentences=3)
                speak("According to Wikipedia,")
                print(results)
                speak(results)
            except:
                speak("No results found..")
                print("No results found.")

        elif "temperature" in query:
            query = query.replace(ASSISTANT_NAME, "")
            search = "temperature in kolar"
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text,"html.parser")
            temp = data.find("div", class_ = "BNeawe").text
            speak(f"current{search} is {temp}")
        
        elif "where is" in query or "locate" in query:
            query = query.replace(ASSISTANT_NAME, "")
            query = query.replace("where is","locate", "")
            location = query
            speak("User asked to Locate")
            speak(location)
            webbrowser.open("https://www.google.nl/maps/place/"+ location + "")
 
        elif 'hi' in query or 'hello' in query or 'jarvis' in query:
            query = query.replace(ASSISTANT_NAME, "")
            speak("hello sir, how can i help you today")  
        elif "what's your name" in query or "your name is" in query or "your name" in query or "what's your good name " in query:
            query = query.replace(ASSISTANT_NAME, "")
            speak("My name: jarvis. My mission: To assist you.")           
        elif "i am fine" in query:
            query = query.replace(ASSISTANT_NAME, "")
            speak("that's great, sir")
        elif "how are you" in query:
            query = query.replace(ASSISTANT_NAME, "")
            speak("Perfect, sir")
        elif "what are you doing" in query:
            query = query.replace(ASSISTANT_NAME, "")
            speak("sir, i am gathering information")
        elif "where are you" in query:
            query = query.replace(ASSISTANT_NAME, "")
            speak("i am A I based computer program, sir")  
        elif "thank you" in query:
            query = query.replace(ASSISTANT_NAME, "")
            speak("you are welcome, sir")   

        else:
            from engine.features import chatBot
            chatBot(query)
    except:
        print("error")
    
    eel.ShowHood()