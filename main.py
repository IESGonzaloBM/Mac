# ===================================================================================================
#   Sumador de 2 numeros binarios
#
#   - Input: Dos numeros binarios
#   - Output: Suma y/o resta de los numeros binarios
#
#   By: Gonzalo Blanco
# ===================================================================================================
import os
from sys import argv, exit, stdout
import time
import subprocess
import threading


def get_param() -> str | None:
    """
    Obtiene la IP dada por terminal, gestiona y controla los posibles errores.

    Returns:
        int: IPv4 comprabada
    Raises:
        Exception: Lanza un tipo de error generico, en formato: "[ERROR] <error interpretado>".
    """

    msg = "[ERROR]: La IP debe de estar separada por '.', tener 4 octetos entre [0, 255]"

    if len(argv) != 2:
        raise Exception("[ERROR]: Formato incorrecto")

    try:
        ip_octetos = argv[1].split(".")
        ip_octetos = [int(octeto) for octeto in ip_octetos]
    except Exception:
        raise Exception(msg)

    if len(ip_octetos) != 4:
        raise Exception(msg)
    elif any(not 0 <= octeto <= 255 for octeto in ip_octetos):
        raise Exception(msg)

    # Hacer sin ceros a la izquierda por octeto

    # ip_octetos = argv[1].split(".")
    # [int(octeto) for octeto in ip_octetos 0 <= int(octeto) <= 255 and len(ip_octetos) == 4]

    return argv[1]


def ping_subprocess(ip: str) -> dict[str, int]:
    result_dict: dict[str, int] = {} # Definimos un diccionario para poder acceder comodamente

    def run_ping_subprocess(target):
        """
        Función que ejecuta el comando ping y oculta su salida. Y asigna el resultado a un diccionario

        Args:
            target (str): Target IP adress
        """

        # Ocultamos la salida (stdout) y salido por error (stderr) redirigiendo a DEVNULL lo que seria "> null"
        # Tambien se lo podriamos pasar mediante `args` pero de esta forma se puede ejecutar en ambos OS
        result = subprocess.run(['ping', target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        result_dict["returncode"] = result.returncode

    # HILO
    ping_thread = threading.Thread(target=run_ping_subprocess, args=(ip,))
    ping_thread.start()

    # ANIMACION
    spinner = "/-\\|"
    i = 0
    while ping_thread.is_alive():

        # print(f'\rVerificando {spinner[i % len(spinner)]} {ip}', end='')

        if i != 4:
            print(f"\rVerificando{"." * i}", end="")
            i += 1
        else:
            print(f"\rVerificando   ", end="")
            i = 0

        time.sleep(0.5)  # Espera 0.1s para la animacion de espera
        stdout.flush()  # Fuerza la actualización inmediate del buffer por medio del flush()

    return result_dict

def command(ip: str) -> str:
    """
    Envia paquetes a la IPv4 dada, si es 0 ha sido recibida

    Args:
        ip (str): IPv4 comprabada
    Returns:
        str: "Exito" si recibe los paquetes, "Fracaso" si no los recibe
    """

    if os.name == "posix":
        msg = "Exito" if ping_subprocess(ip).get("returncode") == 0 else "Fracaso"
    elif os.name == "nt":
        msg = "Exito" if ping_subprocess(ip).get("returncode") == 0 else "Fracaso"
    else:
        raise Exception("[ERROR]: Sistema operativo desconocido")

    print(" Proceso completado")

    return msg

def mac():
    pass

if __name__ == "__main__":
    try:
        ip = get_param()
        result = command(ip)
        print(result)
    except Exception as error:
        print(error)
        exit(1)
    except KeyboardInterrupt as error:
        print("\nSalida forzada por usuario")