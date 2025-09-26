# Clase Carrito
import pygame

class Carrito:
    def __init__(self, x, y):
        """Inicializa el carrito con posición inicial"""
        self.x = x
        self.y = y
        self.velocidad = 20
        self.ancho = 50  # Ligeramente más pequeño para colisión más precisa
        self.alto = 70   # Ligeramente más pequeño para colisión más precisa
        self.color = (0, 0, 255)  # Azul para distinguir mejor
        
    def mover_arriba(self):
        """Mueve el carrito hacia arriba (izquierda en coordenadas originales)"""
        self.x -= self.velocidad
        
    def mover_abajo(self):
        """Mueve el carrito hacia abajo (derecha en coordenadas originales)"""
        self.x += self.velocidad
        
    def obtener_rect(self):
        """Retorna el rectángulo de colisión del carrito"""
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)
        
    def dibujar(self, pantalla, ancho, alto):
        """Dibuja el carrito en la pantalla, adaptado al tamaño"""
        escala_x = ancho / 800
        escala_y = alto / 600
        x = int(self.x * escala_x)
        y = int(self.y * escala_y)
        w = int(self.ancho * escala_x)
        h = int(self.alto * escala_y)
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(pantalla, self.color, rect)
        
        # Agregar borde negro para mejor visibilidad
        pygame.draw.rect(pantalla, (0, 0, 0), rect, 2)