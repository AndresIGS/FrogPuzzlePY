import pygame
import sys
import heapq
import itertools

# Inicializar Pygame
pygame.init()

# --------------------------
# 1. CONSTANTES Y CONFIGURACIÓN
# --------------------------
LONGITUD_CARRETERA = 7
ANCHO_VENTANA = 800
ALTO_VENTANA = 350
TAMANIO_CUADRO = ANCHO_VENTANA // LONGITUD_CARRETERA

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 150, 0)
ROJO = (150, 0, 0)
GRIS = (150, 150, 150)
AZUL = (0, 100, 200)

# Velocidad de animación en ms
velocidad = 500  # Tiempo que dura cada estado de la animación

# Cargar imágenes
try:
    imagen_rana = pygame.image.load("rana.png")
    imagen_rana = pygame.transform.scale(imagen_rana, (TAMANIO_CUADRO - 10, TAMANIO_CUADRO - 10))
    imagen_sapo = pygame.image.load("sapo.webp")
    imagen_sapo = pygame.transform.scale(imagen_sapo, (TAMANIO_CUADRO - 10, TAMANIO_CUADRO - 10))
    fondo = pygame.image.load("fondo.webp")
    fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))
    piedra = pygame.image.load("piedra.png")
    piedra = pygame.transform.scale(piedra, (TAMANIO_CUADRO, TAMANIO_CUADRO))
except pygame.error:
    print("Advertencia: No se encontraron archivos de imagen. Usando colores sustitutos.")
    imagen_rana = pygame.Surface((TAMANIO_CUADRO - 10, TAMANIO_CUADRO - 10)); imagen_rana.fill(VERDE)
    imagen_sapo = pygame.Surface((TAMANIO_CUADRO - 10, TAMANIO_CUADRO - 10)); imagen_sapo.fill(ROJO)
    fondo = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA)); fondo.fill(GRIS)
    piedra = pygame.Surface((TAMANIO_CUADRO, TAMANIO_CUADRO)); piedra.fill(BLANCO)

pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Ranas y Sapos - Solucionador A*")
fuente = pygame.font.Font(None, 30)
reloj = pygame.time.Clock()

# Estados inicial y objetivo
ESTADO_INICIAL = ('rana', 'rana', 'rana', None, 'sapo', 'sapo', 'sapo')
ESTADO_OBJETIVO = ('sapo', 'sapo', 'sapo', None, 'rana', 'rana', 'rana')

contador = itertools.count()

# --------------------------
# 2. FUNCIONES HEURÍSTICAS Y LÓGICA A*
# --------------------------
def funcion_heuristica(tablero_actual):
    try:
        indice_vacio = tablero_actual.index(None)
    except ValueError:
        return float('inf') 
    h = 0
    # Ranas a la izquierda del espacio vacío deben moverse a la derecha
    for i in range(indice_vacio):
        if tablero_actual[i] == 'rana':
            h += 1
    # Sapos a la derecha del espacio vacío deben moverse a la izquierda
    for i in range(indice_vacio + 1, LONGITUD_CARRETERA):
        if tablero_actual[i] == 'sapo':
            h += 1
    return h

def obtener_movimientos_legales(tablero):
    tablero_lista = list(tablero)
    try:
        indice_vacio = tablero_lista.index(None)
    except ValueError:
        return []
    nuevos_estados = []
    
    # Desplazamientos: -2 (salto izq), -1 (paso izq), 1 (paso der), 2 (salto der)
    for desplazamiento in [-2, -1, 1, 2]:
        indice_anfibio = indice_vacio - desplazamiento
        if 0 <= indice_anfibio < LONGITUD_CARRETERA:
            tipo_anfibio = tablero_lista[indice_anfibio]
            
            # 1. Movimiento de Rana (solo a la derecha, desplazamiento > 0)
            if tipo_anfibio == 'rana' and desplazamiento > 0:
                # Caso de salto (2 pasos)
                if desplazamiento == 2:
                    # La pieza saltada debe ser un 'sapo' (regla del juego)
                    if tablero_lista[indice_vacio - 1] != 'sapo': continue
                # Caso de paso (1 paso), sin restricción
                
            # 2. Movimiento de Sapo (solo a la izquierda, desplazamiento < 0)
            elif tipo_anfibio == 'sapo' and desplazamiento < 0:
                # Caso de salto (2 pasos)
                if desplazamiento == -2: # abs(desplazamiento) == 2
                    # La pieza saltada debe ser una 'rana' (regla del juego)
                    if tablero_lista[indice_vacio + 1] != 'rana': continue
                # Caso de paso (1 paso), sin restricción
                
            # Si no es un movimiento legal para ese tipo de anfibio y desplazamiento
            else:
                continue
            
            # Si el movimiento es legal, creamos el nuevo estado
            nuevo_tablero_lista = list(tablero_lista)
            nuevo_tablero_lista[indice_vacio] = tipo_anfibio
            nuevo_tablero_lista[indice_anfibio] = None
            nuevos_estados.append(tuple(nuevo_tablero_lista))
            
    return nuevos_estados

def reconstruir_camino(camino_dict, objetivo):
    secuencia = []
    estado = objetivo
    while estado is not None:
        secuencia.append(estado)
        estado = camino_dict.get(estado)
    return secuencia[::-1]

def resolver_ranas_astar():
    g_costo_inicial = 0
    h_costo_inicial = funcion_heuristica(ESTADO_INICIAL)
    f_costo_inicial = g_costo_inicial + h_costo_inicial
    # (f_costo, g_costo, contador_desempate, estado)
    priority_queue = [(f_costo_inicial, g_costo_inicial, next(contador), ESTADO_INICIAL)]
    costos_g = {ESTADO_INICIAL: g_costo_inicial}
    camino = {ESTADO_INICIAL: None}
    
    while priority_queue:
        f_actual, g_actual, _, estado_actual = heapq.heappop(priority_queue)
        
        if estado_actual == ESTADO_OBJETIVO:
            print(f"Solución encontrada en {g_actual} pasos.")
            return reconstruir_camino(camino, ESTADO_OBJETIVO)
        
        for nuevo_estado in obtener_movimientos_legales(estado_actual):
            nuevo_g = g_actual + 1
            
            if nuevo_estado not in costos_g or nuevo_g < costos_g[nuevo_estado]:
                costos_g[nuevo_estado] = nuevo_g
                h_costo = funcion_heuristica(nuevo_estado)
                nuevo_f = nuevo_g + h_costo
                camino[nuevo_estado] = estado_actual
                # Añadir/Actualizar en la cola de prioridad
                heapq.heappush(priority_queue, (nuevo_f, nuevo_g, next(contador), nuevo_estado))
                
    return None

# --------------------------
# 3. DIBUJO Y VISUALIZACIÓN
# --------------------------
def calcular_costos_estado(tablero):
    g_costo = 0 # No se puede determinar 'g' de un estado fuera del contexto de A*
    h_costo = funcion_heuristica(tablero)
    f_costo = h_costo # Usamos h como un sustituto para la visualización fuera del bucle A*
    return f_costo, g_costo, h_costo

def dibujar_tablero(tablero_actual, paso_actual, total_pasos, f_costo, g_costo, h_costo):
    pantalla.blit(fondo, (0, 0))
    
    # Dibuja las piedras/casillas
    for i in range(LONGITUD_CARRETERA):
        x = i * TAMANIO_CUADRO
        pantalla.blit(piedra, (x, 50))
        
    # Dibuja los anfibios
    offset_x = (TAMANIO_CUADRO - (TAMANIO_CUADRO - 10)) // 2 
    offset_y = 55 # Ajuste vertical para que queden centrados en la piedra
    
    for i, ocupante in enumerate(tablero_actual):
        x_pos = i * TAMANIO_CUADRO + offset_x
        if ocupante == "rana":
            pantalla.blit(imagen_rana, (x_pos, offset_y))
        elif ocupante == "sapo":
            pantalla.blit(imagen_sapo, (x_pos, offset_y))
            
    # Información de A*
    texto_paso = fuente.render(f"Paso {paso_actual}/{total_pasos}", True, NEGRO)
    pantalla.blit(texto_paso, (10, 10))
    # Muestra los costos. Nota: g_costo es la longitud del camino hasta este punto.
    texto_costos = fuente.render(f"Paso: g={g_costo} | Heurística: h={h_costo} | f={f_costo}", True, NEGRO)
    pantalla.blit(texto_costos, (200, 10))
    
    # Dibujar botones
    pygame.draw.rect(pantalla, AZUL, reinicio_btn)
    pygame.draw.rect(pantalla, AZUL, velocidad_btn)
    pygame.draw.rect(pantalla, AZUL, salir_btn)
    
    pantalla.blit(fuente.render("Reiniciar", True, BLANCO), (reinicio_btn.x + 8, reinicio_btn.y + 10))
    pantalla.blit(fuente.render(f"Velocidad: {velocidad//1000}s", True, BLANCO), (velocidad_btn.x + 5, velocidad_btn.y + 10))
    pantalla.blit(fuente.render("Salir", True, BLANCO), (salir_btn.x + 25, salir_btn.y + 10))
    
    pygame.display.flip()

# Botones como rectángulos
reinicio_btn = pygame.Rect(50, 180, 100, 40)
velocidad_btn = pygame.Rect(250, 180, 150, 40)
salir_btn = pygame.Rect(450, 180, 100, 40)

# --------------------------
# 4. BUCLE PRINCIPAL
# --------------------------
def visualizar_solucion():
    global velocidad
    
    # Calcular la solución de A* antes del bucle principal
    solucion = resolver_ranas_astar()
    if not solucion:
        print("Error: No se encontró solución.")
        return 
        
    total_pasos = len(solucion) - 1
    paso_actual = 0
    tiempo_ultimo_paso = pygame.time.get_ticks()
    
    # Variable de estado para controlar si la animación ha terminado
    animacion_terminada = False 
    
    running = True
    while running:
        # Lógica de Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
            # Lógica de clics de ratón
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if reinicio_btn.collidepoint(evento.pos):
                    # Reiniciar la animación y el estado
                    paso_actual = 0
                    tiempo_ultimo_paso = pygame.time.get_ticks()
                    animacion_terminada = False # Reiniciar el estado
                elif velocidad_btn.collidepoint(evento.pos):
                    # Cambiar velocidad
                    velocidades = [2000, 1000, 500, 250, 100] # Opciones de velocidad en ms
                    try:
                        idx = velocidades.index(velocidad)
                        velocidad = velocidades[(idx + 1) % len(velocidades)]
                    except ValueError:
                        velocidad = velocidades[0] # Velocidad predeterminada si la actual no está en la lista
                elif salir_btn.collidepoint(evento.pos):
                    running = False
        
        # Lógica de Animación (Modificada)
        tiempo_actual = pygame.time.get_ticks()
        
        # Solo avanzar el paso si la animación NO ha terminado
        if not animacion_terminada:
            if tiempo_actual - tiempo_ultimo_paso >= velocidad:
                if paso_actual < total_pasos:
                    paso_actual += 1
                    tiempo_ultimo_paso = tiempo_actual
                # Si estamos en el último paso y el tiempo ha pasado, la animación ha terminado
                elif paso_actual == total_pasos: 
                    animacion_terminada = True
                    # No actualizamos tiempo_ultimo_paso para que no vuelva a entrar aquí.
        
        # Dibujar
        if solucion:
            estado_actual_tablero = solucion[min(paso_actual, total_pasos)]
            g_costo_display = min(paso_actual, total_pasos) # g_costo es el índice en la solución
            h_costo_display = funcion_heuristica(estado_actual_tablero)
            f_costo_display = g_costo_display + h_costo_display
            
            dibujar_tablero(estado_actual_tablero, min(paso_actual, total_pasos), total_pasos, 
                            f_costo_display, g_costo_display, h_costo_display)


        # Mensaje al acabar el juego (Activado cuando la animación termina)
        if animacion_terminada: 
            mensaje_final = fuente.render("¡JUEGO TERMINADO! Todas las ranas cruzaron.", True, (255, 0, 0))  # Rojo
            pantalla.blit(mensaje_final, (ANCHO_VENTANA // 2 - mensaje_final.get_width() // 2, ALTO_VENTANA - 50))
            pygame.display.flip() # Asegura que el mensaje se dibuje inmediatamente

        
        # Control de FPS (solo para asegurar que Pygame no consuma CPU innecesariamente)
        reloj.tick(60) 
        
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    visualizar_solucion()