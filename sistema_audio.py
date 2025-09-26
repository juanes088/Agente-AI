import speech_recognition as sr
import pyttsx3

# Configuracion inicial del reconocedor de voz
r = sr.Recognizer()
r.energy_threshold = 4000

def configurar_voz(engine):
    # Busca una voz en espanol o usa la predeterminada
    voices = engine.getProperty('voices')
    voz_espanola = None
    for voice in voices:
        if any(palabra in voice.name.lower() for palabra in ['spanish', 'es', 'maria', 'espanol']):
            voz_espanola = voice.id
            break
    if voz_espanola:
        engine.setProperty('voice', voz_espanola)
    else:
        engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 160)
    engine.setProperty('volume', 0.9)

def hablar(texto, communicator):
    # Convierte texto a voz y maneja el estado de hablando
    try:
        communicator.speaking_changed.emit(True)
        engine = pyttsx3.init()
        configurar_voz(engine)
        engine.say(texto)
        engine.runAndWait()
        communicator.speaking_changed.emit(False)
        return True
    except:
        communicator.speaking_changed.emit(False)
        return False

def escuchar():
    # Escucha el microfono y devuelve el comando en texto
    try:
        with sr.Microphone() as source:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        comando = r.recognize_google(audio, language='es-ES').lower()
        print(f"👤: {comando}")
        return comando
    except:
        return ""