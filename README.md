# Comprobacion de IP y MAC (Python) — README

> CLI que dada una IPv4 por terminal en formato: py mac.py <IPv4>, realiza un `ping` comprobando si la direccion IPv4 es correcta,
> apuntando a la direccion dada ocultando cualquier output ya sea, `stdout` o `stderr`. Despues devuelve su dirrecion fisica, es decir,
> la MAC asociada a la IPv4 dada en caso de que la IPv4 exista y este en la misma red local (LAN).

---

## 1) Descripción del módulo

Este proyecto implementa un `ping` y devuelve su direccion MAC a una direccion IPv4
- El comando sigue el siguiente formato: `py mac.py <IPv4>`
- La IP debe de cumplir que sea 4 octetos entre 0 y 255 cada uno separado por puntos.
- La IP debe de existir y estar en la misma red local (LAN) para devolver su MAC.
---

## 2) Requisitos

- **Python 3.10 o superior**.
- **Sin dependencias externas obligatorias.**
- Si en algún momento se añaden librerías, se listarán en el archivo **`dependecias.txt`**

---

## 3) Instalación de Python

### 3.1 Linux

#### Debian/Ubuntu (y derivados)
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
python3 --version
python3 -m pip --version
```

#### Fedora
```bash
sudo dnf install -y python3 python3-pip python3-virtualenv
python3 --version
python3 -m pip --version
```

#### Arch/Manjaro
```bash
sudo pacman -S --needed python python-pip
python --version
python -m pip --version
```

> **Entorno virtual (opcional recomendado)**
```bash
python3 -m venv .venv
# Activar:
# Linux/macOS:
source .venv/bin/activate
# (Salir: 'deactivate')
```

### 3.2 Windows

#### Opción A — Microsoft Store
1. Abrir **Microsoft Store**, buscar **Python 3.x** (Python Software Foundation).
2. Instalar y verificar:
```powershell
py --version
py -m pip --version
```

#### Opción B — Instalador oficial
1. Descargar desde **https://www.python.org/downloads/** el instalador de Python 3.x.
2. **Marcar** “**Add Python to PATH**” durante la instalación.
3. Verificar:
```powershell
py --version
py -m pip --version
```

> **Entorno virtual (opcional)**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
# (Salir: 'deactivate')
```

---

## 4) Ejecución del módulo

### Sintaxis general
```bash
python mac.py <IPv4>
```
- `mac.py` archivo `.py` donde esta el codigo
- `IP` dirección en formato IPv4

> En Windows puedes usar `py` en lugar de `python`.
> En Linux, si conviven varias versiones, usa `python3`.

### Casos de prueba

```bash
# Linux/macOS
python mac.py 192.168.1.1
```
Salida esperada:
```
Las salidas depende si las direcciones IP existen o no y estan en la misma red local, es decir, la red LAN

Caso de ejemplo:
Proceso completado
94:6a:b0:1d:54:b5
```

## 6) Mensajes de error y códigos de salida


- **Ping a IPv4 incorrecta** ->
  - Mensaje: `Fracaso` →
- **Tipo de dato**, **rango numerico**, **numero de octetos** ->
  - Mensaje: `[ERROR]: La IP debe de estar separada por '.', tener 4 octetos entre [0, 255]`
- **Formato en terminal incorrecto** ->
  - Mensaje: `[ERROR]: Formato incorrecto`
- **Ejecutar comando** ->
- Mensaje: `[ERROR]: No se ha podido ejecutar el comando ping` | `[ERROR]: No se ha podido obtener la MAC`
---

## 7) Problemas frecuentes (FAQ)

- **“python: command not found” / “py no se reconoce”** → Instala Python o ajusta el **PATH** (ver sección 3).
- **“pip no se reconoce”** → Usa `python -m pip` (o `py -m pip` en Windows).

---

## 8) Comentarios

La funcion `parse_mac_from_text()` esta extraida de ChatGPT y adaptada a las necesidades del proyecto debido a que no encontraba
la forma de hacerlo ya que usa expresion compleja de RegeEx. Por otro lado, se usa `subprocess` para ejecutar comandos del sistema operativo por comodidad.
Todo esta explicado en el codigo fuente `mac.py`. Por ultimo, he dejado la parte de la animacion a la hora de esperar como en la practica Ping.