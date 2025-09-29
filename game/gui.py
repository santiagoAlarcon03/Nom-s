import pygame

class GUI:
    def __init__(self):
        self.ancho_pantalla = 900
        self.alto_pantalla = 600
        self.pantalla = pygame.display.set_mode((self.ancho_pantalla, self.alto_pantalla), pygame.RESIZABLE)
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
        self.NARANJA = (255, 140, 0)

    def get_size(self):
        return self.pantalla.get_size()
        
    def renderizar(self, motor):
        ancho, alto = self.get_size()
        motor.ancho_pantalla = ancho
        motor.alto_pantalla = alto
        superficie_juego = pygame.Surface((alto, ancho))
        
        if motor.juego_activo:
            motor.carretera.dibujar_estatica(superficie_juego, alto, ancho)
            motor.carrito.dibujar(superficie_juego, alto, ancho)
            for obstaculo in motor.obstaculos:
                obstaculo.dibujar(superficie_juego, alto, ancho)
        else:
            superficie_juego.fill(self.NEGRO)
            
        superficie_rotada = pygame.transform.rotate(superficie_juego, -90)
        superficie_escalada = pygame.transform.scale(superficie_rotada, (ancho, alto))
        self.pantalla.fill(self.NEGRO)
        self.pantalla.blit(superficie_escalada, (0, 0))
        
        if motor.juego_activo:
            self.mostrar_velocidad(motor.velocidad_juego)
            self.mostrar_velocidad_carrito(motor.velocidad_carrito_x)
            self.mostrar_energia(motor.carrito)
            self.mostrar_controles_arbol(motor)
            if motor.mostrar_arbol:
                self.mostrar_arbol_avl(motor)
        else:
            self.mostrar_game_over()
        pygame.display.flip()
     
    def mostrar_velocidad(self, velocidad):
        texto = self.fuente_pequeña.render(f"Velocidad Juego: {velocidad:.1f}x", True, self.BLANCO)
        self.pantalla.blit(texto, (10, 10))
        
    def mostrar_velocidad_carrito(self, velocidad_carrito):
        texto = self.fuente_pequeña.render(f"Velocidad Carrito: {velocidad_carrito:.1f}px/s", True, self.BLANCO)
        self.pantalla.blit(texto, (10, 30))
        
    def mostrar_energia(self, carrito):
        barra_x, barra_y, barra_ancho, barra_alto = 10, 50, 200, 20
        porcentaje = carrito.obtener_porcentaje_energia()
        ancho_energia = int((porcentaje / 100) * barra_ancho)
        if porcentaje > 70:
            color_energia = (0, 255, 0)
        elif porcentaje > 40:
            color_energia = (255, 255, 0)
        elif porcentaje > 20:
            color_energia = (255, 165, 0)
        else:
            color_energia = (255, 0, 0)
        pygame.draw.rect(self.pantalla, (64, 64, 64), (barra_x, barra_y, barra_ancho, barra_alto))
        if ancho_energia > 0:
            pygame.draw.rect(self.pantalla, color_energia, (barra_x, barra_y, ancho_energia, barra_alto))
        pygame.draw.rect(self.pantalla, self.BLANCO, (barra_x, barra_y, barra_ancho, barra_alto), 2)
        texto_energia = self.fuente_pequeña.render(f"Energía: {carrito.energia_actual}/{carrito.energia_maxima}", True, self.BLANCO)
        self.pantalla.blit(texto_energia, (barra_x + barra_ancho + 10, barra_y))
        
    def mostrar_controles_arbol(self, motor):
        ancho, alto = self.get_size()
        x_base, y_base = 10, alto - 180
        animacion_activa = motor.visualizador_avl.esta_animando()
        controles = [
            "T: Mostrar/Ocultar Árbol AVL",
            f"Recorrido actual: {motor.tipo_recorrido_actual.upper()}",
            "1:InOrden 2:PreOrden 3:PostOrden 4:Anchura",
            "ANIMACIONES:",
            "Q: Iniciar animación recorrido" if not animacion_activa else "🎬 Animación en curso...",
            "E: Detener animación",
            "- : Lento  0: Normal  + : Rápido",
            "ELIMINACIÓN:",
            "5: Modo eliminación" if not motor.visualizador_avl.modo_eliminacion else "🗑️ MODO ELIMINACIÓN ACTIVO",
            "ESC: Cancelar eliminación" if motor.visualizador_avl.modo_eliminacion else ""
        ]
        for i, control in enumerate(controles):
            if control == "":
                continue
            elif i == 1:
                color = self.VERDE
            elif i == 3:
                color = self.NARANJA
            elif i == 4 and animacion_activa:
                color = self.ROJO
            elif i == 7:
                color = self.ROJO
            elif i == 8 and motor.visualizador_avl.modo_eliminacion:
                color = self.ROJO
            elif i == 9:
                color = self.ROJO
            else:
                color = self.AZUL
            texto = self.fuente_pequeña.render(control, True, color)
            self.pantalla.blit(texto, (x_base, y_base + i * 20))
    
    def mostrar_arbol_avl(self, motor):
        superficie_arbol = motor.obtener_superficie_arbol()
        if superficie_arbol:
            ancho, alto = self.get_size()
            overlay = pygame.Surface((ancho, alto))
            overlay.set_alpha(230)
            overlay.fill((0, 0, 0))
            self.pantalla.blit(overlay, (0, 0))
            arbol_rect = superficie_arbol.get_rect()
            arbol_rect.center = (ancho // 2, alto // 2)
            self.pantalla.blit(superficie_arbol, arbol_rect)
            instruccion = "Presiona T para ocultar el árbol AVL"
            texto_instruccion = self.fuente_mediana.render(instruccion, True, self.BLANCO)
            texto_rect = texto_instruccion.get_rect(center=(ancho // 2, alto - 30))
            self.pantalla.blit(texto_instruccion, texto_rect)
        
    def mostrar_game_over(self):
        overlay = pygame.Surface((self.ancho_pantalla, self.alto_pantalla))
        overlay.set_alpha(128)
        overlay.fill(self.NEGRO)
        self.pantalla.blit(overlay, (0, 0))
        texto_game_over = self.fuente_grande.render("GAME OVER", True, self.ROJO)
        rect_game_over = texto_game_over.get_rect(center=(self.ancho_pantalla//2, self.alto_pantalla//2 - 25))
        self.pantalla.blit(texto_game_over, rect_game_over)
        texto_reiniciar = self.fuente_pequeña.render("Presiona R para reiniciar o ESC para salir", True, self.VERDE)
        rect_reiniciar = texto_reiniciar.get_rect(center=(self.ancho_pantalla//2, self.alto_pantalla//2 + 25))
        self.pantalla.blit(texto_reiniciar, rect_reiniciar)