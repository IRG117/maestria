import pygame
import random
import matplotlib.pyplot as plt

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, bala, nave, fondo, etc.
jugador = None
bala = None
bala2= None
fondo = None
nave = None
menu = None

# Variables de salto
salto = False
salto_altura = 15  # Velocidad inicial de salto
gravedad = 1
en_suelo = True

#variables de caminar
camina= False
camina_distancia= 15
friccion= 1
atras= True

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False  # Indica si el modo de juego es automático

# Lista para guardar los datos de velocidad, distancia y salto (target)
datos_modelo = []

# Cargar las imágenes
jugador_frames = [
    pygame.image.load('assets/sprites/mono_frame_1.png'),
    pygame.image.load('assets/sprites/mono_frame_2.png'),
    pygame.image.load('assets/sprites/mono_frame_3.png'),
    pygame.image.load('assets/sprites/mono_frame_4.png')
]

bala_img = pygame.image.load('assets/sprites/purple_ball.png')
bala_img2 = pygame.image.load('assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('assets/game/fondo2.png')
nave_img = pygame.image.load('assets/game/ufo.png')
menu_img = pygame.image.load('assets/game/menu.png')

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador y de la bala
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
bala2 = pygame.Rect(w - 745, h - 390, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)  # Tamaño del menú

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10  # Cuántos frames antes de cambiar a la siguiente imagen
frame_count = 0

# Variables para la bala
velocidad_bala = -5  # Velocidad de la bala hacia la izquierda
bala_disparada = False
velocidad_bala2 = 0  # Velocidad de la bala hacia la izquierda
bala_disparada2 = False

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w

# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -3)  # Velocidad aleatoria negativa para la bala
        bala_disparada = True

def disparar_bala2():
    global bala_disparada2, velocidad_bala2
    if not bala_disparada2:
        velocidad_bala2 = random.randint(3, 8)  # Velocidad aleatoria negativa para la bala
        bala_disparada2 = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50  # Reiniciar la posición de la bala
    bala_disparada = False

def reset_bala2():
    global bala2, bala_disparada2
    bala2.y = h - 390  # Reiniciar la posición de la bala
    bala_disparada2 = False

# Función para manejar el salto
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura  # Mover al jugador hacia arriba
        salto_altura -= gravedad  # Aplicar gravedad (reduce la velocidad del salto)

        # Si el jugador llega al suelo, detener el salto
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15  # Restablecer la velocidad de salto
            en_suelo = True



# funcion para manejar el avance
def manejar_caminata():
    global jugador, camina, camina_distancia, friccion, atras

    if camina:
        jugador.x += camina_distancia
        camina_distancia -= friccion

        if jugador.x <= 60:
            jugador.x = 60
            camina = False
            camina_distancia= 15
            atras= True
        


# Función para actualizar el juego
def update():
    global bala, velocidad_bala, current_frame, frame_count, fondo_x1, fondo_x2, bala2, velocidad_bala2

    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

    # Si el primer fondo sale de la pantalla, lo movemos detrás del segundo
    if fondo_x1 <= -w:
        fondo_x1 = w

    # Si el segundo fondo sale de la pantalla, lo movemos detrás del primero
    if fondo_x2 <= -w:
        fondo_x2 = w

    # Dibujar los fondos
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    # Dibujar el jugador con la animación
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))

    # Dibujar la nave
    pantalla.blit(nave_img, (nave.x, nave.y))

    # Mover y dibujar la bala
    if bala_disparada:
        bala.x += velocidad_bala

    if bala_disparada2:
        bala2.y += velocidad_bala2

    # Si la bala sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()
    
    if bala2.y > h:
        reset_bala2()

    pantalla.blit(bala_img, (bala.x, bala.y))
    pantalla.blit(bala_img2, (bala2.x, bala2.y))

    # Colisión entre la bala y el jugador
    if jugador.colliderect(bala):
        print("Colisión detectada!")
        reiniciar_juego()  # Terminar el juego y mostrar el menú

    if jugador.colliderect(bala2):
        print("Colisión detectada!")
        reiniciar_juego()
# Función para guardar datos del modelo en modo manual
def guardar_datos():
    global jugador, bala, velocidad_bala, salto, bala2, camina
    distancia = abs(jugador.x - bala.x)
    salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
    # Guardar velocidad de la bala, distancia al jugador y si saltó o no
    caminata_hecha = 1 if camina else 0
    datos_modelo.append((velocidad_bala, distancia, salto_hecho,caminata_hecha))

# Función para pausar el juego y guardar los datos
def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
    else:
        print("Juego reanudado.")

# Función para mostrar el menú y seleccionar el modo de juego
def mostrar_menu():
    global menu_activo, modo_auto
    pantalla.fill(NEGRO)
    texto = fuente.render("Presiona 'A' para Auto, 'M' para Manual, o 'Q' para Salir", True, BLANCO)
    pantalla.blit(texto, (w // 4, h // 2))
    pygame.display.flip()

    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    modo_auto = True
                    menu_activo = False
                elif evento.key == pygame.K_m:
                    modo_auto = False
                    menu_activo = False
                elif evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()



def graficar_datos():
    if not datos_modelo:
        return  # No hay datos para graficar

    # Convertir los datos en listas separadas
    velocidades, distancias, saltos, caminatas = zip(*datos_modelo)

    # Crear subgráficas
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))

    # Graficar velocidad de la bala
    axs[0, 0].plot(velocidades, label='Velocidad de la bala', color='blue')
    axs[0, 0].set_title('Velocidad de la Bala')
    axs[0, 0].set_xlabel('Iteración')
    axs[0, 0].set_ylabel('Velocidad')
    axs[0, 0].legend()

    # Graficar distancia
    axs[0, 1].plot(distancias, label='Distancia', color='orange')
    axs[0, 1].set_title('Distancia al Jugador')
    axs[0, 1].set_xlabel('Iteración')
    axs[0, 1].set_ylabel('Distancia')
    axs[0, 1].legend()

    # Graficar saltos
    axs[1, 0].plot(saltos, label='Saltó (1 = Sí, 0 = No)', color='green')
    axs[1, 0].set_title('Saltó')
    axs[1, 0].set_xlabel('Iteración')
    axs[1, 0].set_ylabel('Salto')
    axs[1, 0].legend()

    # Graficar caminatas
    axs[1, 1].plot(caminatas, label='Caminó (1 = Sí, 0 = No)', color='red')
    axs[1, 1].set_title('Caminó')
    axs[1, 1].set_xlabel('Iteración')
    axs[1, 1].set_ylabel('Caminata')
    axs[1, 1].legend()

    # Ajustar la distribución de las subgráficas
    plt.tight_layout()
    plt.show()









# Función para reiniciar el juego tras la colisión
def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo, bala2, bala_disparada2, camina
    menu_activo = True  # Activar de nuevo el menú
    jugador.x, jugador.y = 50, h - 100  # Reiniciar posición del jugador
    bala.x = w - 50  # Reiniciar posición de la bala
    bala2.y= h - 390
    nave.x, nave.y = w - 100, h - 100  # Reiniciar posición de la nave
    bala_disparada = False
    bala_disparada2= False
    salto = False
    camina = False
    en_suelo = True
    # Mostrar los datos recopilados hasta el momento
    print("Datos recopilados para el modelo: ", datos_modelo)
    graficar_datos()
    mostrar_menu()  # Mostrar el menú de nuevo para seleccionar modo
    



def main():
    global salto, en_suelo, bala_disparada, bala_disparada2, camina, atras

    reloj = pygame.time.Clock()
    mostrar_menu()  # Mostrar el menú al inicio
    correr = True

    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_d and not pausa:
                    camina=True
                    atras= False
                if evento.key == pygame.K_SPACE and en_suelo and not pausa:  # Detectar la tecla espacio para saltar
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_p:  # Presiona 'p' para pausar el juego
                    pausa_juego()
                if evento.key == pygame.K_q:  # Presiona 'q' para terminar el juego
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

        if not pausa:
            # Modo manual: el jugador controla el salto
            if not modo_auto:
                if salto:
                    manejar_salto()
                if camina:
                    manejar_caminata()
                # Guardar los datos si estamos en modo manual
                guardar_datos()

            # Actualizar el juego
            if not bala_disparada:
                disparar_bala()
            update()

            if not bala_disparada2:
                disparar_bala2()
            update()

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(30)  # Limitar el juego a 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
