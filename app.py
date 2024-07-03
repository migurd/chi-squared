import eel
import sys

# Agrega la ruta al sistema si es necesario
sys.path.append("..")

# Inicializa eel con la carpeta 'html' donde están los archivos HTML
eel.init("html")

# Define una función expuesta a JavaScript
@eel.expose
def saludo(nombre):
    return f"Hola, {nombre}!"

def start_eel():
    # Lista de navegadores con su modo y ruta (si es necesario)
    browsers = [
        ('chrome', 'C:/Program Files/Google/Chrome/Application/chrome.exe'),  # Chrome
        ('edge', None),  # Edge no necesita una ruta específica
        ('opera', 'C:/Program Files/Opera/launcher.exe'),  # Opera
        ('opera_gx', 'C:/Program Files/Opera GX/launcher.exe')  # Opera GX
    ]

    # Intenta iniciar eel con cada navegador en la lista
    for mode, path in browsers:
        try:
            # Si hay una ruta específica para el navegador, usarla
            if path:
                eel.start("index.html", mode=mode, cmdline_args=['--browser', path], size=(400, 400))
            else:
                eel.start("index.html", mode=mode, size=(400, 400))
            return  # Si se inicia eel con éxito, salir de la función
        except OSError as e:
            # Captura la excepción si no se puede iniciar eel con el navegador actual
            print(f"Error starting eel with {mode}: {e}")

    # Si no se encuentra ningún navegador compatible, imprimir un mensaje de error
    print("No se pudo encontrar ningún navegador compatible.")

if __name__ == "__main__":
    # Llama a la función para iniciar eel
    start_eel()
