# Clase Obstáculo - Sistema de tipos con drenaje de energía
import pygame

class Obstaculo:
    def __init__(self, x, y, tipo="normal"):
        """Inicializa un obstáculo cuadrado"""
        self.x = x
        self.y = y
        self.ancho = 40
        self.alto = 40
        self.tipo = tipo
        self.activo = True
        
        # Definir colores según el tipo
        if tipo == "normal":
            self.color = (255, 0, 0)  # Rojo para obstáculos normales
        elif tipo == "especial":
            self.color = (0, 255, 0)  # Verde para obstáculos especiales (puntos)
        else:
            self.color = (128, 128, 128)  # Gris por defecto
    
    def mover(self, velocidad):
        """Mueve el obstáculo hacia abajo"""
        self.y += velocidad * 2  # Velocidad de caída
            
    def obtener_rect(self):
        """Retorna el rectángulo de colisión preciso del obstáculo"""
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)
        
    def dibujar(self, pantalla, ancho, alto):
        """Dibuja el obstáculo cuadrado en la pantalla"""
        if self.activo:
            # Escalar para ventana responsiva
            escala_x = ancho / 800
            escala_y = alto / 600
            
            x = int(self.x * escala_x)
            y = int(self.y * escala_y)
            w = int(self.ancho * escala_x)
            h = int(self.alto * escala_y)
            
            # Dibujar obstáculo como cuadrado sólido
            rect = pygame.Rect(x, y, w, h)
            pygame.draw.rect(pantalla, self.color, rect)
            pygame.draw.rect(pantalla, (0, 0, 0), rect, 2)
            
            # Efecto especial para obstáculos especiales
            if self.tipo == "especial":
                # Dibujar una estrella o símbolo especial
                center_x = x + w // 2
                center_y = y + h // 2
                pygame.draw.circle(pantalla, (255, 255, 0), (center_x, center_y), w // 4)
        
    def esta_fuera_de_pantalla(self, alto_pantalla):
        """Verifica si el obstáculo ha salido de la pantalla"""
        return self.y > alto_pantalla
    
    def desactivar(self):
        """Desactiva el obstáculo"""
        self.activo = False