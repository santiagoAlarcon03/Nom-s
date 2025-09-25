# Clase Obstáculo
import pygame
import random

class Obstaculo:
    def __init__(self, x, y, tipo="normal"):
        """Inicializa un obstáculo"""
        self.x = x
        self.y = y
        self.velocidad = 3
        self.ancho = 35
        self.alto = 50
        self.tipo = tipo
        self.activo = True
        
        # Definir colores según el tipo
        if tipo == "normal":
            self.color = (0, 0, 255)  # Azul
        elif tipo == "especial":
            self.color = (255, 255, 0)  # Amarillo
        else:
            self.color = (128, 128, 128)  # Gris
            
    def actualizar(self):
        """Actualiza la posición del obstáculo"""
        if self.activo:
            self.y += self.velocidad
            
    def obtener_rect(self):
        """Retorna el rectángulo de colisión del obstáculo"""
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)
        
    def dibujar(self, pantalla):
        """Dibuja el obstáculo en la pantalla"""
        if self.activo:
            rect = self.obtener_rect()
            pygame.draw.rect(pantalla, self.color, rect)
            # Borde negro
            pygame.draw.rect(pantalla, (0, 0, 0), rect, 2)
            
    def esta_fuera_de_pantalla(self, alto_pantalla):
        """Verifica si el obstáculo ha salido de la pantalla"""
        return self.y > alto_pantalla
        
    def desactivar(self):
        """Desactiva el obstáculo"""
        self.activo = False