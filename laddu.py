import win32com.client #pip install pywin32
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib
from gpt4all import GPT4All

try:
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
except Exception as e:
    print("Failed to load voice:", e)
    speaker = None

print("Loading GPT4All AI model (may download ~1.8GB if first time)...")
try:
    llm = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")
except Exception as e:
    print("Failed to load AI:", e)
    llm = None

def speak(audio):
    if speaker:
        speaker.Speak(audio)
    else:
        print(f"laddu Output: {audio}")


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am Laddu Sir. Please tell me how may I help you")       

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query


if __name__ == "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            speak("youtube is opened sir")

        elif 'open google' in query:
            webbrowser.open("google.com")
            speak("google is opened sir")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")
            speak("stackoverflow is opened sir")



        elif 'open' in query:
            query = query.replace("open ", "")
            website = query.replace(" ", "")
            if not website.endswith('.com') and not website.endswith('.org') and not website.endswith('.in'):
                website = website + '.com'
            speak(f"Opening {query} sir")
            webbrowser.open(website)


        elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif query != "none":
            if llm:
                speak("Thinking...")
                # Generate a short response suitable for voice
                response = llm.generate(query, max_tokens=60)
                print(f"GPT4All: {response.strip()}")
                speak(response.strip())
            else:
                speak("I am not sure about that, sir.")
