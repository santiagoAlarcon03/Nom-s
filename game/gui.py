# Interfaz gráfica (pygame)
import pygame
import sys

class GUI:
    def __init__(self):
        """Inicializa la interfaz gráfica"""
        self.ancho_pantalla = 600
        self.alto_pantalla = 800
        self.pantalla = pygame.display.set_mode((self.ancho_pantalla, self.alto_pantalla))
        pygame.display.set_caption("Juego de Carros - Árbol AVL")
        
        # Fuentes
        pygame.font.init()
        self.fuente_grande = pygame.font.Font(None, 48)
        self.fuente_mediana = pygame.font.Font(None, 36)
        self.fuente_pequeña = pygame.font.Font(None, 24)
        
        # Colores
        self.BLANCO = (255, 255, 255)
        self.NEGRO = (0, 0, 0)
        self.ROJO = (255, 0, 0)
        self.VERDE = (0, 255, 0)
        self.AZUL = (0, 0, 255)
        
    def renderizar(self, motor):
        """Renderiza todos los elementos del juego"""
        # Limpiar pantalla
        self.pantalla.fill(self.NEGRO)
        
        if motor.juego_activo:
            # Dibujar carretera
            motor.carretera.dibujar(self.pantalla)
            
            # Dibujar carrito
            motor.carrito.dibujar(self.pantalla)
            
            # Dibujar obstáculos
            for obstaculo in motor.obstaculos:
                obstaculo.dibujar(self.pantalla)
                
            # Mostrar puntuación
            self.mostrar_puntuacion(motor.puntuacion)
            
            # Mostrar velocidad
            self.mostrar_velocidad(motor.velocidad_juego)
            
        else:
            # Pantalla de game over
            self.mostrar_game_over(motor.puntuacion)
            
        # Actualizar pantalla
        pygame.display.flip()
        
    def mostrar_puntuacion(self, puntuacion):
        """Muestra la puntuación en pantalla"""
        texto = self.fuente_mediana.render(f"Puntuación: {puntuacion}", 
                                         True, self.BLANCO)
        self.pantalla.blit(texto, (10, 10))
        
    def mostrar_velocidad(self, velocidad):
        """Muestra la velocidad actual"""
        texto = self.fuente_pequeña.render(f"Velocidad: {velocidad:.1f}x", 
                                         True, self.BLANCO)
        self.pantalla.blit(texto, (10, 50))
        
    def mostrar_game_over(self, puntuacion_final):
        """Muestra la pantalla de game over"""
        # Fondo semi-transparente
        overlay = pygame.Surface((self.ancho_pantalla, self.alto_pantalla))
        overlay.set_alpha(128)
        overlay.fill(self.NEGRO)
        self.pantalla.blit(overlay, (0, 0))
        
        # Texto de Game Over
        texto_game_over = self.fuente_grande.render("GAME OVER", True, self.ROJO)
        rect_game_over = texto_game_over.get_rect(center=(self.ancho_pantalla//2, 
                                                         self.alto_pantalla//2 - 50))
        self.pantalla.blit(texto_game_over, rect_game_over)
        
        # Puntuación final
        texto_puntuacion = self.fuente_mediana.render(f"Puntuación Final: {puntuacion_final}", 
                                                    True, self.BLANCO)
        rect_puntuacion = texto_puntuacion.get_rect(center=(self.ancho_pantalla//2, 
                                                           self.alto_pantalla//2))
        self.pantalla.blit(texto_puntuacion, rect_puntuacion)
        
        # Instrucciones para reiniciar
        texto_reiniciar = self.fuente_pequeña.render("Presiona R para reiniciar o ESC para salir", 
                                                   True, self.VERDE)
        rect_reiniciar = texto_reiniciar.get_rect(center=(self.ancho_pantalla//2, 
                                                        self.alto_pantalla//2 + 50))
        self.pantalla.blit(texto_reiniciar, rect_reiniciar)
        
    def mostrar_menu_principal(self):
        """Muestra el menú principal"""
        self.pantalla.fill(self.NEGRO)
        
        # Título
        titulo = self.fuente_grande.render("JUEGO DE CARROS", True, self.BLANCO)
        rect_titulo = titulo.get_rect(center=(self.ancho_pantalla//2, 200))
        self.pantalla.blit(titulo, rect_titulo)
        
        # Subtítulo
        subtitulo = self.fuente_mediana.render("Con Árbol AVL", True, self.VERDE)
        rect_subtitulo = subtitulo.get_rect(center=(self.ancho_pantalla//2, 250))
        self.pantalla.blit(subtitulo, rect_subtitulo)
        
        # Instrucciones
        instrucciones = [
            "Usa las flechas o A/D para moverte",
            "Evita los obstáculos azules",
            "Recoge los obstáculos amarillos",
            "Presiona ESPACIO para comenzar"
        ]
        
        y_offset = 350
        for instruccion in instrucciones:
            texto = self.fuente_pequeña.render(instruccion, True, self.BLANCO)
            rect = texto.get_rect(center=(self.ancho_pantalla//2, y_offset))
            self.pantalla.blit(texto, rect)
            y_offset += 30
            
        pygame.display.flip()