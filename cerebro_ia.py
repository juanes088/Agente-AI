import requests
import json
import webbrowser
from sistema_audio import hablar
from config import GROQ_API_KEY

# Configuraciones de la IA
MODO_IA = "groq"
MODO_ROBERTO = False

def consultar_roberto(pregunta):
    # Consulta la IA de Groq con la pregunta dada
    if MODO_IA == "groq" and GROQ_API_KEY != "AQUI_TU_KEY":
        try:
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "messages": [
                    {
                        "role": "system", 
                        "content": "Eres Roberto, un asistente amigable. Responde en espanol brevemente."
                    },
                    {
                        "role": "user", 
                        "content": str(pregunta)
                    }
                ],
                "model": "llama-3.1-8b-instant",
                "max_tokens": 500,
                "temperature": 0.5
            }
            
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions", 
                headers=headers, 
                json=data, 
                timeout=25
            )
            
            if response.status_code == 200:
                result = response.json()
                respuesta = result['choices'][0]['message']['content']
                return respuesta.strip()
            else:
                return "Error de conexion con la IA"
                
        except Exception as e:
            return "Error tecnico inesperado"
    
    return "IA no disponible ahora"

def procesar_comando(comando, communicator):
    # Procesa comandos de voz y decide la accion
    global MODO_ROBERTO
    
    if "quiero hablar roberto" in comando:
        MODO_ROBERTO = True
        hablar("Hola, soy Roberto. ¿De que quieres hablar?", communicator)
        return True
    
    if "chao roberto" in comando:
        MODO_ROBERTO = False
        hablar("Chao, vuelvo a ser tu asistente normal", communicator)
        return True
    
    if MODO_ROBERTO:
        print("🧠 Roberto esta pensando...")
        respuesta = consultar_roberto(comando)
        if respuesta:
            print(f"👾 Roberto: {respuesta}")
            hablar(respuesta, communicator)
            return True
        else:
            hablar("No pude entenderte", communicator)
            return True
    
    palabras = comando.split()
    
    if "busca" in palabras or "buscar" in palabras:
        idx = palabras.index("busca") if "busca" in palabras else palabras.index("buscar")
        if idx + 1 < len(palabras):
            busqueda = " ".join(palabras[idx+1:])
            url = f"https://www.google.com/search?q={busqueda}"
            webbrowser.open(url)
            hablar(f"Buscando {busqueda}", communicator)
            return True
        else:
            hablar("¿Que quieres buscar?", communicator)
            return True
    
    if any(frase in comando for frase in ["abre chrome", "abre navegador"]):
        from controlador_web import abrir_chrome
        return abrir_chrome(communicator)
    
    if any(frase in comando for frase in ["cierra chrome", "cierra todo", "cierra navegador"]):
        from controlador_web import cerrar_chrome
        return cerrar_chrome(communicator)
    
    if "abre" in palabras:
        idx = palabras.index("abre")
        if idx + 1 < len(palabras):
            sitio = " ".join(palabras[idx+1:])
            if "chrome" not in sitio.lower():
                from controlador_web import adivinar_url
                return adivinar_url(sitio, communicator)
            else:
                from controlador_web import abrir_chrome
                return abrir_chrome(communicator)
    
    return False

def modo_roberto_on():
    # Activa el modo conversacion
    global MODO_ROBERTO
    MODO_ROBERTO = True

def modo_roberto_off():
    # Desactiva el modo conversacion
    global MODO_ROBERTO
    MODO_ROBERTO = False