# 🐸 Puzle de las 3 Ranas y los 3 Sapos

Un juego simple y entretenido donde tres ranas deben intercambiar posiciones con tres sapos siguiendo un conjunto de reglas específicas. El objetivo es que las ranas lleguen al lado opuesto de la carretera, mientras los sapos deben moverse hacia el otro extremo.

## Descripción

Este proyecto implementa el famoso puzle de las **3 ranas y los 3 sapos** en Python utilizando `threading`. Cada rana o sapo es un "hilo" que intenta moverse de acuerdo con las reglas del juego. La carretera está representada como una lista de 7 espacios, y el juego finaliza cuando todas las ranas y sapos han intercambiado de posiciones exitosamente.

## Reglas del Juego

1. Las **ranas** (`👉`) solo pueden moverse hacia la derecha.
2. Los **sapos** (`👈`) solo pueden moverse hacia la izquierda.
3. Pueden moverse a un espacio vacío adyacente o saltar sobre una rana o sapo si hay un espacio vacío justo detrás.
4. El objetivo es que las 3 ranas intercambien posiciones con los 3 sapos en el menor número de movimientos posible.

Posición inicial:

[👉, 👉, 👉, -, 👈, 👈, 👈]

Posición objetivo:

[👈, 👈, 👈, -, 👉, 👉, 👉]


## Instalación

Para ejecutar este proyecto en tu máquina local, sigue estos pasos:

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/MatiasGanino/FrogPuzzlePY
2. **Acceder al directorio del proyecto**:
   ```bash
   cd FrogPuzzlePY
3. **Ejecutar el archivo principal**:
    ```bash
   python FrogPuzzle.py
## Uso

El juego empieza automáticamente al ejecutar el script. Verás una representación visual de la carretera y las posiciones de las ranas y sapos. Cada turno muestra el estado de la carretera después de los movimientos.

Al comenzar el juego, verás algo como esto:


👉👉👉-👈👈👈

👉👉-👉👈👈👈

👉👉👈👉-👈👈

...

👈👈👈-👉👉👉

¡El juego ha terminado!