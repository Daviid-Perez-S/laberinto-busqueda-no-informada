# Laberinto con algoritmo de búsqueda no informada Depth First Search (DSF)


## Creación del entorno virtual

Antes de iniciar, debemos de crear un entorno virtual para los paquetes que se instalarán en nuestro proyecto. Se creará un entorno virtual usando **venv** ☝🏻.

P.D. se asume que ya tienes instalado en tu sistema 👀:

- python3
- pip3

Para el caso de Linux (que es el S.O. recomendado por exelencia y el usado en este proyecto), las instrucciones en la terminal (**bash**) son las siguientes:

1. Debemos de instalar venv con python3

    ```bash
    sudo apt update
    sudo apt upgrade
    sudo apt install python3-venv
    ```

2. Ahora debemos crear nuestro entorno virtual dentro de nuestro proyecto (lo llamaremos **env**)

    ```bash
    python3 -m venv env
    ```

3. Por último activamos el entorno virtual recién creado

    ```bash
    source env/bin/activate
    ```

## Instalación de las dependencias del proyecto

Una vez activado el entorno virtual se deben de instalar desde cero las dependecias.
Para instalar las dependencias del proyecto ejecuta el siguiente comando:

```bash
pip3 install -r requirements.txt
```

NOTA 1: Si le instalas otras dependencias al proyecto, no te olvides de guardarlas en el archivo de requerimientos :D ---> (requirements.txt). Usa el comando:

```bash
pip3 freeze > requirements.txt
```

## Instalar pygraphviz

Como esta dependecia es algo *especial*, hagamos lo siguiente.
Instala pygraphviz con el siguiente comando:

```bash
pip3 install pygraphviz
```

Si te da un error al instalarlo, instalalo mejor usando mejor apt:

```bash
sudo apt install graphviz
```

Eso debería funcionar... sino pues ya fue, ya ni le continues al resto de este README  :v

## Ejecutar el programa

```bash
python arbol.py
```

Generará una imagen llamada "arbol.png" en el directorio raíz.

## Desactivar el entorno virtual

Para desactivar el entorno virtual que anteriormente activamos, basta con que ejecutemos el siguiente comando:

```bash
deactivate
```
