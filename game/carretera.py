# Clase Carretera
import pygame
import random

class Carretera:
    def __init__(self, ancho, alto):
        """Inicializa la carretera"""
        self.ancho = ancho
        self.alto = alto
        self.carriles = 3
        self.ancho_carril = ancho // self.carriles
        self.linea_posicion = 0
        self.velocidad_linea = 3
        
    def actualizar(self):
        """Actualiza la posición de las líneas de la carretera"""
        self.linea_posicion += self.velocidad_linea
        if self.linea_posicion >= 40:  # Espaciado entre líneas
            self.linea_posicion = 0
            
    def dibujar(self, pantalla, ancho, alto):
        """Dibuja la carretera con líneas divisorias, adaptada al tamaño"""
        self.ancho = ancho
        self.alto = alto
        self.ancho_carril = ancho // self.carriles
        pantalla.fill((50, 50, 50))  # Gris oscuro
        for i in range(1, self.carriles):
            x = i * self.ancho_carril
            for y in range(-20 + self.linea_posicion, alto + 20, 40):
                pygame.draw.rect(pantalla, (255, 255, 255), (x - 2, y, 4, 20))
                
    def obtener_carril_centro(self, numero_carril):
        """Retorna la posición X del centro de un carril específico"""
        if 0 <= numero_carril < self.carriles:
            return numero_carril * self.ancho_carril + self.ancho_carril // 2
        return self.ancho // 2