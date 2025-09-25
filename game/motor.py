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
        self.ancho_pantalla = 600
        self.alto_pantalla = 800
        
        # Componentes del juego
        self.carretera = Carretera(self.ancho_pantalla, self.alto_pantalla)
        self.carrito = Carrito(
            self.carretera.obtener_carril_centro(1) - 20,  # Carril central
            self.alto_pantalla - 100
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
        """Maneja los eventos del teclado"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                if self.carrito.x > 0:
                    self.carrito.mover_izquierda()
            elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                if self.carrito.x < self.ancho_pantalla - self.carrito.ancho:
                    self.carrito.mover_derecha()
                    
    def generar_obstaculo(self):
        """Genera un nuevo obstáculo en un carril aleatorio"""
        carril = random.randint(0, self.carretera.carriles - 1)
        x = self.carretera.obtener_carril_centro(carril) - 17  # Centrar obstáculo
        
        # Tipo de obstáculo aleatorio
        tipo = random.choice(["normal", "normal", "normal", "especial"])
        
        obstaculo = Obstaculo(x, -50, tipo)
        self.obstaculos.append(obstaculo)
        
        # Agregar al árbol AVL (usando posición Y como clave)
        self.arbol_obstaculos.insertar(obstaculo.y, obstaculo)
        
    def actualizar(self):
        """Actualiza la lógica del juego"""
        if not self.juego_activo:
            return
            
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
            obstaculo.actualizar()
            
            # Verificar colisiones
            if self.verificar_colision(self.carrito, obstaculo):
                if obstaculo.tipo == "normal":
                    self.juego_activo = False
                elif obstaculo.tipo == "especial":
                    self.puntuacion += 10
                    obstaculo.desactivar()
                    
            # Eliminar obstáculos fuera de pantalla
            if obstaculo.esta_fuera_de_pantalla(self.alto_pantalla):
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
        
        return rect_carrito.colliderect(rect_obstaculo)
        
    def reiniciar_juego(self):
        """Reinicia el juego"""
        self.obstaculos.clear()
        self.arbol_obstaculos = ArbolAVL()
        self.puntuacion = 0
        self.juego_activo = True
        self.velocidad_juego = 1.0
        self.carrito.x = self.carretera.obtener_carril_centro(1) - 20
        self.carrito.y = self.alto_pantalla - 100