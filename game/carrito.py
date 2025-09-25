# Clase Carrito
import pygame

class Carrito:
    def __init__(self, x, y):
        """Inicializa el carrito con posición inicial"""
        self.x = x
        self.y = y
        self.velocidad = 5
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
        
    def dibujar(self, pantalla):
        """Dibuja el carrito en la pantalla"""
        rect = self.obtener_rect()
        pygame.draw.rect(pantalla, self.color, rect)