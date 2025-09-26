import webbrowser
import subprocess
import platform
import os
import re
from sistema_audio import hablar

def abrir_chrome(communicator):
    # Abre Chrome segun el sistema operativo
    sistema = platform.system()
    try:
        if sistema == "Windows":
            subprocess.run(["chrome"], shell=True, check=True)
        elif sistema == "Darwin":
            subprocess.run(["open", "-a", "Google Chrome"], check=True)
        else:
            subprocess.run(["google-chrome"], check=True)
        hablar("Chrome abierto", communicator)
        return True
    except:
        pass
    
    # Fallback para Windows
    if sistema == "Windows":
        rutas_chrome = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        for ruta in rutas_chrome:
            if os.path.exists(ruta):
                os.startfile(ruta)
                hablar("Chrome abierto", communicator)
                return True
    
    # Ultimo recurso: abre navegador predeterminado
    webbrowser.open("https://www.google.com")
    hablar("Navegador abierto", communicator)
    return True

def cerrar_chrome(communicator):
    # Cierra Chrome segun el sistema operativo
    try:
        sistema = platform.system()
        if sistema == "Windows":
            subprocess.run(['taskkill', '/f', '/im', 'chrome.exe'], shell=True)
        elif sistema == "Darwin":
            subprocess.run(["pkill", "Google Chrome"])
        else:
            subprocess.run(["pkill", "chrome"])
        hablar("Chrome cerrado", communicator)
        return True
    except:
        hablar("No pude cerrar Chrome", communicator)
        return False

def adivinar_url(sitio, communicator):
    # Convierte un nombre de sitio en una URL probable
    sitio_limpio = re.sub(r'[^\w\s-]', '', sitio).strip().lower()
    sitio_sin_espacios = re.sub(r'[-\s]+', '', sitio_limpio)
    
    dominios = [
        f"https://www.{sitio_sin_espacios}.com",
        f"https://www.{sitio_sin_espacios}.com.co",
        f"https://www.{sitio_sin_espacios}.org",
        f"https://{sitio_sin_espacios}.com"
    ]
    
    url_principal = dominios[0]
    webbrowser.open(url_principal)
    hablar(f"Abriendo {sitio}", communicator)
    return True