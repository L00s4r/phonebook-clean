from gtts import gTTS
import pygame
import os

def speak(text, lang='ru'):
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save("temp_speech.mp3")
    
    pygame.mixer.init()
    pygame.mixer.music.load("temp_speech.mp3")
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        continue
    
    os.remove("temp_speech.mp3")  # Удаляем временный файл

speak("Привет. как дела?")