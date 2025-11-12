# ===================================================================================================
#   Comprueba la conectividad de una IPv4 mediante ping y obtiene su MAC
#
#   - Input: IPv4 en la misma red local (LAN)
#   - Output: Direccion Mac
#
#   By: Gonzalo Blanco
# ===================================================================================================

from sys import argv, exit, stdout
from time import sleep
from subprocess import run, check_output, DEVNULL
from threading import Thread
import platform
from re import compile


def get_param() -> str | None:
    """
    Obtiene la IP dada por terminal, gestiona y controla los posibles errores.

    Returns:
        int: IPv4 comprabada
    Raises:
        Exception: Lanza un tipo de error generico, en formato: "[ERROR] <error interpretado>".
    """

    msg = "[ERROR]: La IP debe de estar separada por '.', tener 4 octetos entre [0, 255]"

    try:
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
    except Exception as error:
        print(error)
        exit(1)

    return argv[1]

# Parte extra dicha por el profesor
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
        try:
            result = run(['ping', target], stdout=DEVNULL, stderr=DEVNULL)
            result_dict["returncode"] = result.returncode
        except Exception as error:
            print("[ERROR]: No se ha podido ejecutar el comando ping")
            exit(1)

    # HILO
    ping_thread = Thread(target=run_ping_subprocess, args=(ip,))
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

        sleep(0.5)  # Espera 0.1s para la animacion de espera
        stdout.flush()  # Fuerza la actualización inmediate del buffer por medio del flush()

    return result_dict


def ping(ip: str) -> str:
    """
    Envia paquetes a la IPv4 dada, si es 0 ha sido recibida

    Args:
        ip (str): IPv4 comprabada
    Returns:
        str: "Exito" si recibe los paquetes, "Fracaso" si no los recibe
    """
    system = platform.system().lower()

    # Si queremos hacer una espera, debemos usar subprocesos, por lo tanto, el cuerpo es el mismo. Sin embargo,
    # voy a dejar la estructura por si en un futuro se quiere modificar algo especifico y para que se entienda de forma didactica
    if "linux" in system:
        msg = "Exito" if ping_subprocess(ip).get("returncode") == 0 else "Fracaso"
    elif "windows" in system or "darwin" in system:
        msg = "Exito" if ping_subprocess(ip).get("returncode") == 0 else "Fracaso"

    print(f"\rProceso completado\n", end="")

    return msg


# Funcion extraida de ChatGPT para parsear MACs con el resultado de `arp -a <ip>`. No sabia como hacerlo, usa una expresion compleja de RegeEx
def parse_mac_from_text(text: str) -> str | None:
    """
    Parsea la MAC de un texto dado usando expresiones regulares.

    Args:
        text (str): Texto de la mac de un texto.
    Returns:
        str | None: MAC en formato estandarizado o None si no se encuentra.
    """
    MAC_RE = compile(r'([0-9A-Fa-f]{2}(?:[:\-][0-9A-Fa-f]{2}){5})')

    m = MAC_RE.search(text)
    if not m:
        return None

    mac = m.group(1).lower().replace("-", ":")
    return mac


def get_mac_from_system(ip: str) -> str | None:
    """
    Intenta obtener la MAC consultando comandos del sistema operativo (Windows, Linux o MacOS).

    Args:
        ip (str): IP objetivo.
    Returns:
        str | None: MAC en formato estandarizado o None si no se encuentra.
    """

    # Usamos `subprocess` en vez de `os.system` porque segun la propia documentacion es mas recomendable, ademas de que ya lo hemos usado para la practica ping
    # https://docs.python.org/3.13/library/os.html#os.system

    system = platform.system().lower()

    # Linux | MacOS: `arp -n <ip>`
    if "linux" in system or "darwin" in system:
        try:
            # Usamos `subprocess.check_output` para capturar la salida del comando ya que es una simplificacion de `subprocess.run` con `run(..., check=True, stdout=PIPE).stdout`
            # Debido a que queremos capturar la salida del comando para parsearla con la funcion `parse_mac_from_text` que la he tomado de ChatGPT como he comentado mas arriba
            # https://docs.python.org/3.13/library/subprocess.html#subprocess.check_output
            output = check_output(["arp", "-n", ip], stderr=DEVNULL, universal_newlines=True)
            mac = parse_mac_from_text(output)
            return mac
        except Exception as error:
            print("[ERROR]: No se ha podido obtener la MAC")
            exit(1)

    # Windows: `arp -a <ip>`
    if "windows" in system:
        try:
            output = check_output(["arp", "-a", ip], stderr=DEVNULL, universal_newlines=True)
            mac = parse_mac_from_text(output)
            return mac
        except Exception as error:
            print("[ERROR]: No se ha podido obtener la MAC")
            exit(1)
    return None


if __name__ == "__main__":
    try:
        ip = get_param()
        ping(ip)
        mac = get_mac_from_system(ip)
        if not mac is None:
            print(mac)
        else:
            print("No se ha podido obtener la MAC")
    except KeyboardInterrupt as error:
        print("\nSalida forzada por usuario")