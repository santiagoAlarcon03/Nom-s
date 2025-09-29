import pygame
import sys

class GUI:
    def __init__(self):
        """Inicializa la interfaz gráfica para movimiento horizontal"""
        self.ancho_pantalla = 900  
        self.alto_pantalla = 600  
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
            motor.carretera.dibujar_estatica(superficie_juego, alto, ancho)  # Usar método estático
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
            self.mostrar_velocidad_carrito(motor.velocidad_carrito_x)
            self.mostrar_carril_actual(motor.carril_actual, motor.total_carriles)
            self.mostrar_energia(motor.carrito)
            self.mostrar_indicadores_carriles(motor)
            self.mostrar_controles_arbol(motor)
            
            # Mostrar árbol AVL si está activado
            if motor.mostrar_arbol:
                self.mostrar_arbol_avl(motor)
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
        """Muestra la velocidad actual del juego"""
        texto = self.fuente_pequeña.render(f"Velocidad Juego: {velocidad:.1f}x", 
                                         True, self.BLANCO)
        self.pantalla.blit(texto, (10, 50))
        
    def mostrar_velocidad_carrito(self, velocidad_carrito):
        """Muestra la velocidad del carrito"""
        texto = self.fuente_pequeña.render(f"Velocidad Carrito: {velocidad_carrito:.1f}px/s", 
                                         True, self.BLANCO)
        self.pantalla.blit(texto, (10, 70))
        
    def mostrar_carril_actual(self, carril_actual, total_carriles):
        """Muestra el carril actual del carrito"""
        nombres_carriles = ["Izquierdo", "Central", "Derecho"]
        nombre_carril = nombres_carriles[carril_actual] if carril_actual < len(nombres_carriles) else f"Carril {carril_actual + 1}"
        
        texto = self.fuente_pequeña.render(f"Carril: {nombre_carril} ({carril_actual + 1}/{total_carriles})", 
                                         True, self.BLANCO)
        self.pantalla.blit(texto, (10, 90))
        
    def mostrar_energia(self, carrito):
        """Muestra la barra de energía del carrito"""
        barra_x = 10
        barra_y = 120  # Ajustar posición Y para dar espacio a la información de carril
        barra_ancho = 200
        barra_alto = 20
        
        # Calcular porcentaje de energía
        porcentaje = carrito.obtener_porcentaje_energia()
        ancho_energia = int((porcentaje / 100) * barra_ancho)

        if porcentaje > 70:
            color_energia = (0, 255, 0)  # Verde
        elif porcentaje > 40:
            color_energia = (255, 255, 0)  # Amarillo
        elif porcentaje > 20:
            color_energia = (255, 165, 0)  # Naranja
        else:
            color_energia = (255, 0, 0)  # Rojo
            
        pygame.draw.rect(self.pantalla, (64, 64, 64), 
                        (barra_x, barra_y, barra_ancho, barra_alto))
        
        if ancho_energia > 0:
            pygame.draw.rect(self.pantalla, color_energia, 
                            (barra_x, barra_y, ancho_energia, barra_alto))

        pygame.draw.rect(self.pantalla, self.BLANCO, 
                        (barra_x, barra_y, barra_ancho, barra_alto), 2)
        
        texto_energia = self.fuente_pequeña.render(f"Energía: {carrito.energia_actual}/{carrito.energia_maxima}", 
                                                  True, self.BLANCO)
        self.pantalla.blit(texto_energia, (barra_x + barra_ancho + 10, barra_y))
        
    def mostrar_indicadores_carriles(self, motor):
        """Muestra indicadores visuales de los carriles"""
        ancho, alto = self.get_size()
        
        # Posición de los indicadores en la parte derecha de la pantalla
        pos_x = ancho - 80
        pos_y_base = alto // 2 - 50
        
        # Colores
        AMARILLO = (255, 255, 0)
        GRIS = (100, 100, 100)
        
        # Dibujar indicador para cada carril
        for i in range(motor.total_carriles):
            pos_y = pos_y_base + (i * 40)
            color = AMARILLO if i == motor.carril_actual else GRIS
            
            # Círculo indicador
            pygame.draw.circle(self.pantalla, color, (pos_x, pos_y), 12)
            pygame.draw.circle(self.pantalla, self.BLANCO, (pos_x, pos_y), 12, 2)
            
            # Etiqueta del carril
            nombres = ["I", "C", "D"]  # Izquierdo, Central, Derecho
            texto = self.fuente_pequeña.render(nombres[i] if i < len(nombres) else str(i+1), 
                                             True, self.NEGRO if i == motor.carril_actual else self.BLANCO)
            rect_texto = texto.get_rect(center=(pos_x, pos_y))
            self.pantalla.blit(texto, rect_texto)
        
        # Instrucciones de control
        texto_controles = self.fuente_pequeña.render("↑/↓ o W/S: Cambiar carril", True, GRIS)
        self.pantalla.blit(texto_controles, (pos_x - 100, pos_y_base + 120))
        
    def mostrar_controles_arbol(self, motor):
        """Muestra los controles para el árbol AVL"""
        ancho, alto = self.get_size()
        x_base = 10
        y_base = alto - 120
        
        controles = [
            "T: Mostrar/Ocultar Árbol AVL",
            f"Recorrido actual: {motor.tipo_recorrido_actual.upper()}",
            "1:InOrden 2:PreOrden 3:PostOrden 4:Anchura"
        ]
        
        for i, control in enumerate(controles):
            color = self.VERDE if i == 1 else self.AZUL
            texto = self.fuente_pequeña.render(control, True, color)
            self.pantalla.blit(texto, (x_base, y_base + i * 20))
    
    def mostrar_arbol_avl(self, motor):
        """Muestra el árbol AVL en una ventana superpuesta"""
        superficie_arbol = motor.obtener_superficie_arbol()
        if superficie_arbol:
            # Crear overlay semi-transparente
            ancho, alto = self.get_size()
            overlay = pygame.Surface((ancho, alto))
            overlay.set_alpha(230) 
            overlay.fill((0, 0, 0))
            self.pantalla.blit(overlay, (0, 0))
            
            # Mostrar el árbol centrado
            arbol_rect = superficie_arbol.get_rect()
            arbol_rect.center = (ancho // 2, alto // 2)
            self.pantalla.blit(superficie_arbol, arbol_rect)
            
            # Mostrar instrucciones para cerrar
            instruccion = "Presiona T para ocultar el árbol AVL"
            texto_instruccion = self.fuente_mediana.render(instruccion, True, self.BLANCO)
            texto_rect = texto_instruccion.get_rect(center=(ancho // 2, alto - 30))
            self.pantalla.blit(texto_instruccion, texto_rect)
        
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