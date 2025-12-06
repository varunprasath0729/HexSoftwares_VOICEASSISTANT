import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import pywhatkit
import sys

ASSISTANT_NAME = "assistant"
VOICE_RATE = 150
WIKI_LANG = "en"
EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_email_password"

engine = pyttsx3.init()
engine.setProperty('rate', VOICE_RATE)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning.")
    elif 12 <= hour < 18:
        speak("Good afternoon.")
    else:
        speak("Good evening.")
    speak(f"I am your {ASSISTANT_NAME}. How can I help you?")

def listen_command(timeout=6, phrase_time_limit=6):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return None
    try:
        query = r.recognize_google(audio, language='en-IN')
        print("You:", query)
        return query.lower()
    except:
        return None

def send_email(receiver, subject, body):
    try:
        msg = f"Subject: {subject}\n\n{body}"
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, receiver, msg)
        server.quit()
        return True
    except:
        return False

def open_application(app):
    app = app.lower()
    try:
        if "notepad" in app:
            if sys.platform.startswith('win'): os.system("notepad")
            elif sys.platform == 'darwin': os.system("open -a TextEdit")
            else: os.system("gedit &")
            return True
        if "calculator" in app:
            if sys.platform.startswith('win'): os.system("calc")
            elif sys.platform == 'darwin': os.system("open -a Calculator")
            else: os.system("gnome-calculator &")
            return True
    except:
        return False
    return False

def main_loop():
    greet_user()
    while True:
        query = listen_command()
        if not query:
            speak("Say it again.")
            continue

        if ASSISTANT_NAME in query:
            query = query.replace(ASSISTANT_NAME, "").strip()

        if any(x in query for x in ["exit", "quit", "stop", "bye"]):
            speak("Goodbye.")
            break

        if "time" in query:
            t = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {t}")
            continue

        if "date" in query:
            d = datetime.datetime.now().strftime("%A, %d %B %Y")
            speak(f"Today is {d}")
            continue

        if "wikipedia" in query or "who is" in query or "what is" in query:
            try:
                speak("Searching Wikipedia")
                term = query.replace("wikipedia", "").replace("who is", "").replace("what is", "")
                wikipedia.set_lang(WIKI_LANG)
                result = wikipedia.summary(term, sentences=2)
                speak("According to Wikipedia")
                speak(result)
            except:
                speak("Not found.")
            continue

        if "open youtube" in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
            continue

        if "open google" in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
            continue

        if "stack overflow" in query:
            speak("Opening Stack Overflow")
            webbrowser.open("https://stackoverflow.com")
            continue

        if "play" in query and "youtube" in query:
            speak("Which song?")
            song = listen_command()
            if song:
                speak(f"Playing {song}")
                pywhatkit.playonyt(song)
            continue

        if query.startswith("play "):
            song = query.replace("play", "").strip()
            speak(f"Playing {song}")
            pywhatkit.playonyt(song)
            continue

        if "send email" in query:
            speak("Recipient email?")
            receiver = listen_command()
            if not receiver: continue
            receiver = receiver.replace(" at ", "@").replace(" dot ", ".").replace(" ", "")
            speak("Subject?")
            subject = listen_command() or ""
            speak("Message?")
            body = listen_command() or ""
            speak("Sending email.")
            ok = send_email(receiver, subject, body)
            speak("Email sent." if ok else "Failed.")
            continue

        if "open notepad" in query or "open calculator" in query:
            ok = open_application(query)
            speak("Opened." if ok else "Failed to open.")
            continue

        if "how are you" in query:
            speak("I am fine. How can I help?")
            continue

        speak("Shall I search this on Google?")
        ans = listen_command()
        if ans and ("yes" in ans or "ok" in ans):
            webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        else:
            speak("Okay.")

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        speak("Shutting down.")
