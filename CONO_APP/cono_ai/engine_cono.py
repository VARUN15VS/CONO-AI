import pyttsx3
import speech_recognition as sr

count = 0

def increase_count():
    global count
    count +=1 

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 174)
    engine.say(text)
    engine.runAndWait()
    
def command():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 6)
    try:
        print("Recognizing...")
        command = r.recognize_google(audio, language = 'en-in')
        print(command)
    except Exception as e:
        return ""
    
    return command.lower()

def listen_for_audio():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Listening for keyword...")

    # Continuously listen for audio input
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source, phrase_time_limit=3)  # Listen with a time limit
    
    try:
        # Recognize the audio using Google Speech Recognition
        text = recognizer.recognize_google(audio)
        print("Heard:", text)  # Print the recognized text (for debugging)
        return text
    except sr.UnknownValueError:
        # If speech was unintelligible
        print("Could not understand audio")
        return ""
    except sr.RequestError:
        # If there's an issue with the API
        print("Could not request results; check network connection")
        return ""

#text = command()
    
#speak(text)