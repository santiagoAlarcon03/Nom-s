import pygame
import sys

class GUI:
    def __init__(self):
        """Inicializa la interfaz gráfica para movimiento horizontal"""
        self.ancho_pantalla = 800  # Más ancho para movimiento horizontal
        self.alto_pantalla = 600   # Menos alto para movimiento horizontal
        self.pantalla = pygame.display.set_mode(
            (self.ancho_pantalla, self.alto_pantalla), pygame.RESIZABLE
        )
        pygame.display.set_caption("Carrito Horizontal - Árbol AVL")
        

        pygame.font.init()
        self.fuente_grande = pygame.font.Font(None, 48)
        self.fuente_mediana = pygame.font.Font(None, 36)
        self.fuente_pequeña = pygame.font.Font(None, 24)
        
 
        self.BLANCO = (255, 255, 255)
        self.NEGRO = (0, 0, 0)
        self.ROJO = (255, 0, 0)
        self.VERDE = (0, 255, 0)
        self.AZUL = (0, 0, 255)

    def get_size(self):
        """Devuelve el tamaño actual de la ventana"""
        return self.pantalla.get_size()
        
    def renderizar(self, motor):
        """Renderiza todos los elementos del juego"""
        # Obtener tamaño actual de ventana
        ancho, alto = self.get_size()
        motor.ancho_pantalla = ancho
        motor.alto_pantalla = alto
        # Crear superficie rotada para cambiar orientación visual
        superficie_juego = pygame.Surface((alto, ancho))  # Intercambiar dimensiones
        
        if motor.juego_activo:
            # Dibujar en superficie temporal con coordenadas originales
            motor.carretera.dibujar(superficie_juego, alto, ancho)
            motor.carrito.dibujar(superficie_juego, alto, ancho)
            for obstaculo in motor.obstaculos:
                obstaculo.dibujar(superficie_juego, alto, ancho)
        else:
            superficie_juego.fill(self.NEGRO)
            
        # Rotar la superficie 90 grados en sentido horario y escalar
        superficie_rotada = pygame.transform.rotate(superficie_juego, -90)
        superficie_escalada = pygame.transform.scale(superficie_rotada, (ancho, alto))
        
        # Dibujar la superficie rotada en la pantalla principal
        self.pantalla.fill(self.NEGRO)
        self.pantalla.blit(superficie_escalada, (0, 0))
        
        if motor.juego_activo:
            # Mostrar información en la pantalla rotada
            self.mostrar_puntuacion(motor.puntuacion)
            self.mostrar_velocidad(motor.velocidad_juego)
            self.mostrar_energia(motor.carrito)
        else:
            # Pantalla de game over
            self.mostrar_game_over(motor.puntuacion)
            
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
        
    def mostrar_energia(self, carrito):
        """Muestra la barra de energía del carrito"""
        # Posición y dimensiones de la barra
        barra_x = 10
        barra_y = 80
        barra_ancho = 200
        barra_alto = 20
        
        # Calcular porcentaje de energía
        porcentaje = carrito.obtener_porcentaje_energia()
        ancho_energia = int((porcentaje / 100) * barra_ancho)
        
        # Color de la barra según el nivel de energía
        if porcentaje > 70:
            color_energia = (0, 255, 0)  # Verde
        elif porcentaje > 40:
            color_energia = (255, 255, 0)  # Amarillo
        elif porcentaje > 20:
            color_energia = (255, 165, 0)  # Naranja
        else:
            color_energia = (255, 0, 0)  # Rojo
            
        # Dibujar fondo de la barra
        pygame.draw.rect(self.pantalla, (64, 64, 64), 
                        (barra_x, barra_y, barra_ancho, barra_alto))
        
        # Dibujar energía actual
        if ancho_energia > 0:
            pygame.draw.rect(self.pantalla, color_energia, 
                            (barra_x, barra_y, ancho_energia, barra_alto))
        
        # Dibujar borde
        pygame.draw.rect(self.pantalla, self.BLANCO, 
                        (barra_x, barra_y, barra_ancho, barra_alto), 2)
        
        # Texto de energía
        texto_energia = self.fuente_pequeña.render(f"Energía: {carrito.energia_actual}/{carrito.energia_maxima}", 
                                                  True, self.BLANCO)
        self.pantalla.blit(texto_energia, (barra_x + barra_ancho + 10, barra_y))
        
    def mostrar_game_over(self, puntuacion_final):
        """Muestra la pantalla de game over"""

        overlay = pygame.Surface((self.ancho_pantalla, self.alto_pantalla))
        overlay.set_alpha(128)
        overlay.fill(self.NEGRO)
        self.pantalla.blit(overlay, (0, 0))
        
  
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
            "El carrito se mueve automáticamente hacia la derecha",
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