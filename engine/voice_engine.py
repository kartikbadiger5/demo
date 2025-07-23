# No relative imports to change
import speech_recognition as sr
import pyttsx3

class VoiceEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 180)

    def listen(self):
        with self.microphone as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
        try:
            return self.recognizer.recognize_google(audio).lower()
        except:
            return ""

    def speak(self, text):
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
