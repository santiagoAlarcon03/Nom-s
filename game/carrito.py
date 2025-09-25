# Clase Carrito
import pygame

class Carrito:
    def __init__(self, x, y):
        """Inicializa el carrito con posición inicial"""
        self.x = x
        self.y = y
        self.velocidad = 20
        self.ancho = 40
        self.alto = 60
        self.color = (255, 0, 0)  # Rojo
        
    def mover_izquierda(self):
        """Mueve el carrito hacia la izquierda"""
        self.x -= self.velocidad
        
    def mover_derecha(self):
        """Mueve el carrito hacia la derecha"""
        self.x += self.velocidad
        
    def obtener_rect(self):
        """Retorna el rectángulo de colisión del carrito"""
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)
        
    def dibujar(self, pantalla, ancho, alto):
        """Dibuja el carrito en la pantalla, adaptado al tamaño"""
        # Escalar posición y tamaño
        escala_x = ancho / 600
        escala_y = alto / 800
        x = int(self.x * escala_x)
        y = int(self.y * escala_y)
        w = int(self.ancho * escala_x)
        h = int(self.alto * escala_y)
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(pantalla, self.color, rect)