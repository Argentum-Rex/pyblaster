# IMPORTACION DE LIBRERIAS
import math
import pygame
import sys
import os
import pygame.sprite
import random

# INICIALIZACION DE MODULOS (PYGAME, MIXER)
pygame.init()
pygame.mixer.init()

# VARIABLES DE CONTROL
clock = pygame.time.Clock()  # se utiliza para definir la velocidad de los cuadros por segundo
fuente_titulo = pygame.font.Font('Minecraftia.ttf', 80)  # Tipo de fuente y tamaño para el titulo
fuente_creditos = pygame.font.Font('Minecraftia.ttf', 36)  # Tipo de fuente y tamaño para los créditos
fuente_pausa = pygame.font.Font('Minecraftia.ttf', 60) # Tipo de fuente y tamaño para el menu de pausa


# VARIABLES DIMENSIONES VENTANA
anchoP = 1152
altoP = 648

# VENTANA Y NOMBRE
pygame.display.set_caption("PyBlaster")  # nombre de la ventana
pantalla = pygame.display.set_mode((anchoP, altoP))  # creación de la ventana en las medidas especificadas anteriormente

# IMAGEN DE FONDO
fondo1 = pygame.image.load('BG.png')  # carga de imágenes a utilizar en variables

# VARIABLE DE MOVIMIENTO DE FONDO 
mov_fondo = 0  # variable para fusionar imagen con imagen generando la ilusión de movimiento

# CALCULO DE CUADROS DE IMAGEN 
tiles = math.ceil(anchoP / fondo1.get_width()) + 1  # cálculo para determinar los cuadros por segundo de la imagen de fondo (para animar)

# CARGA DE MÚSICA Y EFECTOS DE SONIDO
pygame.mixer.music.load('Track1.mp3') # Carga el primer archivo de música
pygame.mixer.music.queue('Track2.mp3') # Pone el cola el segundo archivo de musica
pygame.mixer.music.play() # Reproduce la musica
pygame.mixer.music.set_volume(0.2) # Establece el volumen de los archivos a reproducirse
sonido_laser = pygame.mixer.Sound('laser_player.mp3')  # Carga el archivo de sonido para los disparos láser
sonido_laser.set_volume(0.5) # Establece el volumen del sonido de disparo laser


# CLASE PARA EL SPRITE DE LA NAVE
class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('PlayerShip.png').convert_alpha()  # Carga del sprite
        self.rect = self.image.get_rect()  # Obtiene el rectángulo de la imagen
        self.rect.center = (anchoP // 2, altoP // 2)  # Posición inicial del sprite

    def update(self, keys):
        # Movimiento del sprite con WASD o flechitas
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= 10
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += 10
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= 10
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += 10
            
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > anchoP:
            self.rect.right = anchoP
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > altoP:
            self.rect.bottom = altoP    

# CLASE PARA EL LASER (MOVIMIENTO HORIZONTAL)
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('laser_player.png').convert_alpha()  # Carga del sprite del láser
        self.rect = self.image.get_rect()
        self.rect.centerx = x  # Posición inicial del láser (coincide con la nave)
        self.rect.centery = y  # La posición `y` es la misma que la nave

    def update(self):
        # Movimiento del láser hacia la derecha (horizontal)
        self.rect.x += 15
        # Eliminar el láser si sale de la pantalla
        if self.rect.left > anchoP:
            self.kill()

# INSTANCIA DEL SPRITE DE LA NAVE
sprite1 = Nave()

# AGRUPACION DE SPRITES
sprites = pygame.sprite.Group()
lasers = pygame.sprite.Group()  # Grupo para los láseres
sprites.add(sprite1)

# VARIABLE PARA CONTROLAR LA PAUSA
pausado = False

# Clase modificada para usar imágenes en los botones
class Boton:
    def __init__(self, imagen_normal, imagen_hover, x, y):
        # Cargar imágenes para el estado normal y activo (hover)
        self.imagen_normal = pygame.image.load(imagen_normal).convert_alpha()
        self.imagen_hover = pygame.image.load(imagen_hover).convert_alpha()
        self.rect = self.imagen_normal.get_rect()  # Obtener el rectángulo de la imagen
        self.rect.topleft = (x, y)  # Establecer la posición del botón

    def dibujar(self, pantalla):
        # Deteccion del mouse, para mostrar la imagen correcta (boton inactivo y activo)
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pantalla.blit(self.imagen_hover, self.rect.topleft)  # Dibuja la imagen activa (hover)
        else:
            pantalla.blit(self.imagen_normal, self.rect.topleft)  # Dibuja la imagen normal

    def es_clic(self, evento):
        # Verificacion de click
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return True
        return False

# Función para mostrar la pantalla de inicio
def pantalla_inicio():
    # Crear botones con imágenes personalizadas
    boton_jugar = Boton('Play_BTN_96px.png', 'Play_BTN_ACTIVE_96px.png', anchoP // 2 - 50, altoP // 2 - 115)
    boton_creditos = Boton('Info_BTN_96px.png', 'Info_BTN_ACTIVE_96px.png', anchoP // 2 - 50, altoP // 2)
    boton_salir = Boton('Close_BTN_96px.png', 'Close_BTN_ACTIVE_96px.png', anchoP // 2 - 50, altoP // 2 + 115)

    mostrando_inicio = True
    while mostrando_inicio:
        # Capturar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Verificar si los botones fueron clickeados
            if boton_jugar.es_clic(event):
                mostrando_inicio = False  # Iniciar el juego
            if boton_creditos.es_clic(event):
                mostrar_creditos()  # Mostrar los créditos
            if boton_salir.es_clic(event):
                pygame.quit()
                sys.exit()  # Salir del juego

        # Dibujar la pantalla de inicio
        pantalla.fill((0, 0, 0))  # Opcional: Establecer un fondo negro o cualquier color
        boton_jugar.dibujar(pantalla)
        boton_creditos.dibujar(pantalla)
        boton_salir.dibujar(pantalla)

        # Mostrar el título del juego
        titulo = fuente_titulo.render("PyBlaster", True, (255, 255, 255))
        pantalla.blit(titulo, (anchoP // 2 - titulo.get_width() // 2, 75))

        # Actualizar la pantalla
        pygame.display.update()


# Función para mostrar los créditos
def mostrar_creditos():
    mostrando_creditos = True
    while mostrando_creditos:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Volver al menú con Escape
                    mostrando_creditos = False

        # Crear una superficie semitransparente para la opacidad
        fade_credits = pygame.Surface((anchoP, altoP), pygame.SRCALPHA)  # Superficie con soporte de alfa
        fade_credits.fill((0, 0, 0, 8))  # Negro con un valor alfa de 150 (ajusta el último valor para más o menos opacidad)
        pantalla.blit(fade_credits, (0, 0))  # Dibujar la capa opaca sobre el fondo        
        
        # Lista de líneas de texto
        lineas_creditos = [
            ".:: Desarrollado por [REDACTED] ::.",
            ".:: Recursos obtenidos de ITCH.IO y OpenGameArt ::.",
            ".:: ¡Gracias por jugar PyBlaster! ::."
        ]
        
        # Dibujar cada línea con un espaciado entre ellas
        for i, linea in enumerate(lineas_creditos):
            texto_creditos = fuente_creditos.render(linea, True, (255, 255, 255))
            pantalla.blit(texto_creditos, (anchoP // 2 - texto_creditos.get_width() // 2, altoP // 2 - 100 + i * 100))

        # Actualizar pantalla
        pygame.display.update()

# Llamar a la pantalla de inicio antes de entrar al bucle principal del juego
pantalla_inicio()


# LOOP PRINCIPAL
running = True
while running:
    
    # SENTENCIA 'FOR' PARA CERRAR PROGRAMA 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            # Tecla de pausa (Esc)
            if event.key == pygame.K_ESCAPE:
                pausado = not pausado  # Alterna entre pausado y no pausado
                
                if pausado:
                    pygame.mixer.music.pause()  # Pausa la música
                    
                else:
                    pygame.mixer.music.unpause()  # Reanuda la música            
            
            # Tecla para disparar (barra espaciadora o letra K)
            if event.key == pygame.K_SPACE or event.key == pygame.K_k and not pausado:
                
                # Crear un nuevo láser en la posición actual de la nave
                nuevo_laser = Laser(sprite1.rect.right, sprite1.rect.centery)
                lasers.add(nuevo_laser)
                
                # Reproducir el sonido del láser
                sonido_laser.play()                

    # Si no está pausado, el juego sigue normal
    if not pausado:
        # VELOCIDAD DEL RELOJ DE CUADROS POR SEGUNDO 
        clock.tick(24)

        # MOVIMIENTO TECLAS
        keys = pygame.key.get_pressed()
        sprite1.update(keys)

        # ANEXAR IMAGEN CON IMAGEN
        i = 0
        while i < tiles:
            pantalla.blit(fondo1, (fondo1.get_width()*i + mov_fondo, 0))
            i += 1

        # ACTUALIZAR Y DIBUJAR SPRITES
        lasers.update()  # Actualiza la posición de los láseres
        sprites.draw(pantalla)
        lasers.draw(pantalla)

        # FRAME DE MOVIMIENTO
        mov_fondo -= 3

        # RESET DEL FRAME DE MOVIMIENTO
        if abs(mov_fondo) > fondo1.get_width():
            mov_fondo = 0

    else:
        # Si el juego está pausado, atenuar la pantalla
        fade_pause = pygame.Surface((anchoP, altoP)) # dibuja un rectangulo
        fade_pause.fill((75, 75, 75)) # rellena el rectangulo de negro
        fade_pause.set_alpha(8) # establece el nivel de transparencia
        pantalla.blit(fade_pause, (0, 0)) # superpone el rectangulo encima del previo (pantalla de juego)

        # Mostrar el texto de "En Pausa"
        texto_pausa = fuente_pausa.render("EN PAUSA", True, (255, 255, 255))
        pantalla.blit(texto_pausa, (anchoP // 2 - texto_pausa.get_width() // 2, altoP // 2 - texto_pausa.get_height() // 2))

    # REFRESCO DE PANTALLA
    pygame.display.update()

# SALIR DEL PROGRAMA
pygame.quit()