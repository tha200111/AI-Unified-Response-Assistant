import sounddevice as sd
import speech_recognition as sr
import scipy.io.wavfile as wav
import pyttsx3
import datetime
import webbrowser
import wikipedia
import os
import time


# ================= VOICE ENGINE =================

engine = pyttsx3.init()

engine.setProperty("rate", 150)


def speak(text):

    print("Assistant:", text)

    engine.say(text)

    engine.runAndWait()



# ================= FIND MICROPHONE =================

def get_microphone():

    devices = sd.query_devices()

    for index, device in enumerate(devices):

        name = device["name"].lower()


        if "microphone" in name or "mic" in name:

            print("Using microphone:", device["name"])

            return index


    print("No microphone found")

    return None



# ================= LISTEN =================

def listen():

    fs = 16000
    seconds = 5


    print("\nListening...")


    try:


        mic = get_microphone()


        if mic is None:

            speak("No microphone detected")

            return ""



        recording = sd.rec(

            int(seconds * fs),

            samplerate=fs,

            channels=1,

            dtype="int16",

            device=mic

        )


        sd.wait()



        wav.write(

            "voice.wav",

            fs,

            recording

        )



        recognizer = sr.Recognizer()



        with sr.AudioFile("voice.wav") as source:


            audio = recognizer.record(source)



        command = recognizer.recognize_google(audio)


        print("You:", command)


        return command.lower()



    except sr.UnknownValueError:


        print("Could not understand")


        return ""



    except sr.RequestError:


        print("Internet connection error")


        return ""



    except Exception as e:


        print("Microphone error:", e)


        return ""





# ================= COMMANDS =================


def assistant():


    speak(
        "Hello Tharun, I am your AI assistant"
    )


    while True:


        command = listen()



        if command == "":

            continue




        # TIME

        if "time" in command:


            current_time = datetime.datetime.now().strftime(
                "%I:%M %p"
            )


            speak(
                "The time is " + current_time
            )




        # OPEN GOOGLE

        elif "open google" in command:


            speak(
                "Opening Google"
            )


            webbrowser.open(
                "https://google.com"
            )




        # SEARCH

        elif "search" in command:


            speak(
                "What should I search?"
            )


            query = listen()


            if query:


                webbrowser.open(

                    "https://www.google.com/search?q=" + query

                )





        # WIKIPEDIA

        elif "wikipedia" in command:


            topic = command.replace(
                "wikipedia",
                ""
            )


            try:


                result = wikipedia.summary(

                    topic,

                    sentences=2

                )


                speak(result)



            except:


                speak(
                    "I could not find information"
                )





        # OPEN NOTEPAD

        elif "open notepad" in command:


            speak(
                "Opening Notepad"
            )


            os.system(
                "notepad"
            )





        # EXIT

        elif "exit" in command or "stop" in command:


            speak(
                "Goodbye"
            )


            break





# ================= START =================


assistant()
