# Lógica de movimiento y colisiones
import pygame
import random
from .carrito import Carrito
from .carretera import Carretera
from .obstaculo import Obstaculo
from estructuras.arbol_avl import ArbolAVL

class Motor:
    def __init__(self):
        """Inicializa el motor del juego"""
        self.ancho_pantalla = 800
        self.alto_pantalla = 600
        # Componentes del juego
        self.carretera = Carretera(self.ancho_pantalla, self.alto_pantalla)
        self.carrito = Carrito(
            self.ancho_pantalla // 2 - 25,  # Centro horizontal
            self.alto_pantalla - 100  # Parte inferior
        )
        # Lista de obstáculos
        self.obstaculos = []
        self.tiempo_ultimo_obstaculo = 0
        self.intervalo_obstaculo = 2000  # milisegundos
        # Árbol AVL para gestionar obstáculos
        self.arbol_obstaculos = ArbolAVL()
        # Puntuación y estado del juego
        self.puntuacion = 0
        self.juego_activo = True
        self.velocidad_juego = 1.0
        
    def manejar_eventos(self, evento):
        """Maneja los eventos del teclado y el redimensionamiento"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                # Verificar límite izquierdo (aparece como arriba en la pantalla rotada)
                if self.carrito.x - self.carrito.velocidad >= 0:
                    self.carrito.mover_arriba()
            elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                # Verificar límite derecho (aparece como abajo en la pantalla rotada)
                if self.carrito.x + self.carrito.ancho + self.carrito.velocidad <= self.ancho_pantalla:
                    self.carrito.mover_abajo()
            elif evento.key == pygame.K_SPACE:
                # Saltar con la barra espaciadora
                self.carrito.saltar()
        elif evento.type == pygame.VIDEORESIZE:
            self.ancho_pantalla = evento.w
            self.alto_pantalla = evento.h
                    
    def generar_obstaculo(self):
        """Genera un nuevo obstáculo en la parte superior"""
        x = random.randint(0, self.ancho_pantalla - 40)
        y = -40  # Aparece arriba de la pantalla
        
        # Tipo de obstáculo aleatorio con diferentes probabilidades
        probabilidades = ["roca", "roca", "cono", "cono", "cono", "hueco", "aceite", "aceite", "aceite"]
        tipo = random.choice(probabilidades)
        
        obstaculo = Obstaculo(x, y, tipo)
        self.obstaculos.append(obstaculo)
        
        # Agregar al árbol AVL (usando posición Y como clave principal)
        clave = f"{obstaculo.y},{obstaculo.x}"  # Usar coordenadas como clave única
        self.arbol_obstaculos.insertar(clave, obstaculo)
        
    def actualizar(self):
        """Actualiza la lógica del juego"""
        if not self.juego_activo:
            return
            
        # Actualizar sistema de salto del carrito
        self.carrito.actualizar_salto()
            
        # Actualizar carretera
        self.carretera.actualizar()
        
        # Generar obstáculos
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_ultimo_obstaculo > self.intervalo_obstaculo:
            self.generar_obstaculo()
            self.tiempo_ultimo_obstaculo = tiempo_actual
            
        # Actualizar obstáculos
        obstaculos_a_eliminar = []
        for obstaculo in self.obstaculos:
            # Mover obstáculo hacia abajo
            obstaculo.mover(self.velocidad_juego)
            
            # Verificar colisiones
            if self.verificar_colision(self.carrito, obstaculo):
                # Si está saltando, no pierde energía y obtiene puntos bonus
                if self.carrito.esta_saltando():
                    # Puntos bonus por saltar sobre el obstáculo
                    self.puntuacion += 15
                else:
                    # Reducir energía del carrito según el tipo de obstáculo
                    danio = obstaculo.obtener_danio_energia()
                    sin_energia = self.carrito.reducir_energia(danio)
                    
                    # Agregar puntos por el obstáculo superado (aunque haya causado daño)
                    self.puntuacion += 5
                    
                    # Terminar juego si se queda sin energía
                    if sin_energia:
                        self.juego_activo = False
                
                # Desactivar obstáculo después de la colisión
                obstaculo.desactivar()
                    
            # Eliminar obstáculos que salieron de la pantalla
            if obstaculo.y > self.alto_pantalla:
                obstaculos_a_eliminar.append(obstaculo)
                self.puntuacion += 1
                
        # Limpiar obstáculos eliminados
        for obstaculo in obstaculos_a_eliminar:
            if obstaculo in self.obstaculos:
                self.obstaculos.remove(obstaculo)
                
        # Aumentar velocidad gradualmente
        self.velocidad_juego += 0.001
        
    def verificar_colision(self, carrito, obstaculo):
        """Verifica si hay colisión entre el carrito y un obstáculo"""
        if not obstaculo.activo:
            return False
            
        rect_carrito = carrito.obtener_rect()
        rect_obstaculo = obstaculo.obtener_rect()
        
        # Colisión más estricta: reducir ligeramente las áreas de colisión para mayor precisión
        rect_carrito_reducido = pygame.Rect(
            rect_carrito.x + 2, 
            rect_carrito.y + 2, 
            rect_carrito.width - 4, 
            rect_carrito.height - 4
        )
        rect_obstaculo_reducido = pygame.Rect(
            rect_obstaculo.x + 2, 
            rect_obstaculo.y + 2, 
            rect_obstaculo.width - 4, 
            rect_obstaculo.height - 4
        )
        
        return rect_carrito_reducido.colliderect(rect_obstaculo_reducido)
        
    def reiniciar_juego(self):
        """Reinicia el juego"""
        self.obstaculos.clear()
        self.arbol_obstaculos = ArbolAVL()
        self.puntuacion = 0
        self.juego_activo = True
        self.velocidad_juego = 1.0
        self.carrito.x = self.ancho_pantalla // 2 - 25
        self.carrito.y = self.alto_pantalla - 100  
        self.carrito.energia_actual = self.carrito.energia_maxima
        # Resetear estado de salto
        self.carrito.saltando = False
        self.carrito.tiempo_salto = 0