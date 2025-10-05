import time
import random
import threading

LONGITUD_CARRETERA = 7

# Clase que representa una rana como hilo
class Anfibio(threading.Thread):
    def __init__(self, nombre, posicion_inicial, carretera):
        threading.Thread.__init__(self)  # Inicializar la clase base Thread
        self.nombre = nombre
        self.posicion = posicion_inicial
        self.carretera = carretera
        self.lock = threading.Lock()  # Agregar un lock para evitar que 2 anfibios se muevan al mismo lugar
    
    def run(self):
        while True:
            with self.lock:  # Proteger todo el bloque de verificación y movimiento
                # Priorizar movimiento de ranas y sapos específicos
                if self.nombre == "🐶":
                    if self.puede_avanzar():
                        self.posicion += 1  # Se mueve hacia adelante
                    elif self.puede_saltar():
                        self.posicion += 2  # Salta sobre el sapo
                    elif self.puede_retroceder():
                        # tirar dado de 0 a 2
                        dado = random.randint(0, 2)
                        # si dado es 0 no hace nada y sale, si es 1 o 2 retrocede
                        if dado > 0:
                            self.posicion -= 1  # Retrocede uno

                elif self.nombre == "🐱":
                    if self.puede_retroceder():
                        self.posicion -= 1  # Se mueve hacia atrás
                    elif self.puede_saltar():
                        self.posicion -= 2  # Salta sobre la rana
                    elif self.puede_avanzar():
                        # tirar dado de 0 a 2
                        dado = random.randint(0, 2)
                        # si dado es 0 no hace nada y sale, si es 1 o 2 avanza
                        if dado > 0:
                            self.posicion += 1  # Avanza uno
            
            self.carretera.mostrar_pista()
            time.sleep(0.5)
            
            # Verificar si el juego debe finalizar
            if (all(rana.posicion >= 4 for rana in self.carretera.ranas if rana.nombre == "🐶") and
                all(rana.posicion <= 2 for rana in self.carretera.ranas if rana.nombre == "🐱")):
                print("¡El juego ha terminado!")
                break
                
    def puede_avanzar(self):
        # Verificar si puede moverse hacia adelante
        return self.posicion < LONGITUD_CARRETERA - 1 and self.carretera.pista[self.posicion + 1] == " _ "

    def puede_retroceder(self):
        # Verificar si puede moverse hacia atrás
        return self.posicion > 0 and self.carretera.pista[self.posicion - 1] == " _ "

    def puede_saltar(self):
        # Verificar si puede saltar (hay un espacio vacío dos posiciones adelante o atrás)
        if self.nombre == "🐶":
            return (self.posicion < LONGITUD_CARRETERA - 2 and 
                    self.carretera.pista[self.posicion + 1] == "🐱" and 
                    self.carretera.pista[self.posicion + 2] == " _ ")
        else:  # Sapo
            return (self.posicion > 1 and 
                    self.carretera.pista[self.posicion - 1] == "🐶" and 
                    self.carretera.pista[self.posicion - 2] == " _ ")

# Clase que representa la carretera
class Pista:
    def __init__(self):
        self.pista = [" _ "] * LONGITUD_CARRETERA
        self.ranas = []
        self.lock = threading.Lock()  # Agregar un lock para evitar colisiones al mostrar la pista
    
    def agregar_rana(self, rana):
        self.ranas.append(rana)
    
    def iniciar(self):
        # Mostrar la pista inicial antes de que comiencen los movimientos
        self.mostrar_pista()

        for rana in self.ranas:
            rana.start()  # Iniciar cada hilo (cada rana)
        
        for rana in self.ranas:
            rana.join()  # Esperar a que todos los hilos terminen
    
    def mostrar_pista(self):
        with self.lock:  # Proteger la salida con un lock para evitar conflictos entre hilos
            #Limpiar consola
            print("\033c", end="")
            
            # Limpiar la pista
            self.pista = [" _ "] * LONGITUD_CARRETERA
            
            # Colocar las ranas en sus respectivas posiciones
            for rana in self.ranas:
                if 0 <= rana.posicion < LONGITUD_CARRETERA:
                    self.pista[rana.posicion] = rana.nombre
            
            # Mostrar la pista
            print("".join(self.pista))
            print("")  # Espacio extra para claridad visual

# Crear la carretera y las ranas
pista = Pista()

# Crear ranas (se mueven hacia la derecha)
for i in range(3):
    pista.agregar_rana(Anfibio("🐶", i, pista))  # Ranas en posiciones 0, 1, 2

# Crear sapos (se mueven hacia la izquierda)
for i in range(3):
    pista.agregar_rana(Anfibio("🐱", LONGITUD_CARRETERA - 1 - i, pista))  # Sapos en posiciones 4, 5, 6

# Iniciar el juego, primero las ranas y sapos en posiciones extremas
pista.iniciar()
