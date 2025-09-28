import pygame

class Carrito:
    def __init__(self, x, y):
        """Inicializa el carrito con posición inicial y sistema de energía"""
        self.x = x
        self.y = y
        self.velocidad = 60
        self.ancho = 50
        self.alto = 70
        self.color = (0, 0, 255)
        self.energia_maxima = 100
        self.energia_actual = 100
        
        # Sistema de salto
        self.saltando = False
        self.tiempo_salto = 0
        self.duracion_salto = 800  # milisegundos
        
    def mover_arriba(self):
        """Mueve el carrito hacia arriba (izquierda en coordenadas originales)"""
        self.x -= self.velocidad
        
    def mover_abajo(self):
        """Mueve el carrito hacia abajo (derecha en coordenadas originales)"""
        self.x += self.velocidad
        
    def obtener_rect(self):
        """Retorna el rectángulo de colisión del carrito"""
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)
        
    def reducir_energia(self, cantidad):
        """Reduce la energía del carrito"""
        self.energia_actual = max(0, self.energia_actual - cantidad)
        return self.energia_actual <= 0  # Retorna True si se quedó sin energía
        
    def obtener_porcentaje_energia(self):
        """Retorna el porcentaje de energía actual"""
        return (self.energia_actual / self.energia_maxima) * 100
        
    def saltar(self):
        """Inicia el salto del carrito"""
        if not self.saltando:
            self.saltando = True
            self.tiempo_salto = pygame.time.get_ticks()
            
    def actualizar_salto(self):
        """Actualiza el estado del salto"""
        if self.saltando:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_salto >= self.duracion_salto:
                self.saltando = False
                
    def esta_saltando(self):
        """Retorna True si el carrito está saltando"""
        return self.saltando
        
    def dibujar(self, pantalla, ancho, alto):
        """Dibuja el carrito con forma de carro realista, adaptado al tamaño"""
        escala_x = ancho / 800
        escala_y = alto / 600
        x = int(self.x * escala_x)
        y = int(self.y * escala_y)
        w = int(self.ancho * escala_x)
        h = int(self.alto * escala_y)
        
        self._dibujar_carro(pantalla, x, y, w, h)
        
    def _dibujar_carro(self, pantalla, x, y, w, h):
        
        # Cambiar colores si está saltando
        if self.saltando:
            color_carroceria = (255, 215, 0)  # Dorado brillante
            color_ventanas = (255, 255, 255)  # Blanco brillante
            color_ruedas = (255, 165, 0)      # Naranja
            color_llantas = (255, 140, 0)     # Naranja oscuro
            color_parachoque = (255, 255, 255)  # Blanco
            color_faros = (255, 255, 255)     # Blanco puro
        else:
            color_carroceria = (220, 20, 20)
            color_ventanas = (135, 206, 235)
            color_ruedas = (64, 64, 64)
            color_llantas = (32, 32, 32)
            color_parachoque = (200, 200, 200)
            color_faros = (255, 255, 200)
        
        rueda_radio = min(w, h) // 6
        
        carroceria = pygame.Rect(x + 2, y + rueda_radio, w - 4, h - rueda_radio * 2)
        pygame.draw.rect(pantalla, color_carroceria, carroceria)
        pygame.draw.rect(pantalla, (0, 0, 0), carroceria, 2)
        
        techo_w = int(w * 0.8)
        techo_h = int(h * 0.4)
        techo_x = x + (w - techo_w) // 2
        techo_y = y + rueda_radio + 2
        techo = pygame.Rect(techo_x, techo_y, techo_w, techo_h)
        pygame.draw.rect(pantalla, color_carroceria, techo)
        pygame.draw.rect(pantalla, (0, 0, 0), techo, 1)
        
        ventana_margen = 3
        
        parabrisas = pygame.Rect(techo_x + ventana_margen, techo_y + ventana_margen, 
                                techo_w - ventana_margen * 2, techo_h // 2 - ventana_margen)
        pygame.draw.rect(pantalla, color_ventanas, parabrisas)
        pygame.draw.rect(pantalla, (0, 0, 0), parabrisas, 1)
        
        ventana_trasera = pygame.Rect(techo_x + ventana_margen, 
                                     techo_y + techo_h // 2 + 1, 
                                     techo_w - ventana_margen * 2, 
                                     techo_h // 2 - ventana_margen * 2)
        pygame.draw.rect(pantalla, color_ventanas, ventana_trasera)
        pygame.draw.rect(pantalla, (0, 0, 0), ventana_trasera, 1)
        
        rueda_frontal_pos = (x + w // 6, y + h - rueda_radio - 2)
        rueda_trasera_pos = (x + 5 * w // 6, y + h - rueda_radio - 2)
        
        pygame.draw.circle(pantalla, color_ruedas, rueda_trasera_pos, rueda_radio)
        pygame.draw.circle(pantalla, color_llantas, rueda_trasera_pos, rueda_radio - 2)
        pygame.draw.circle(pantalla, (128, 128, 128), rueda_trasera_pos, rueda_radio // 2)
        
        pygame.draw.circle(pantalla, color_ruedas, rueda_frontal_pos, rueda_radio)
        pygame.draw.circle(pantalla, color_llantas, rueda_frontal_pos, rueda_radio - 2)
        pygame.draw.circle(pantalla, (128, 128, 128), rueda_frontal_pos, rueda_radio // 2)
        
        parachoque_frontal = pygame.Rect(x, y + h - rueda_radio * 2 + 5, w, 6)
        pygame.draw.rect(pantalla, color_parachoque, parachoque_frontal)
        pygame.draw.rect(pantalla, (0, 0, 0), parachoque_frontal, 1)
        
        parachoque_trasero = pygame.Rect(x, y + rueda_radio - 3, w, 6)
        pygame.draw.rect(pantalla, color_parachoque, parachoque_trasero)
        pygame.draw.rect(pantalla, (0, 0, 0), parachoque_trasero, 1)
        
        faro_size = max(3, w // 12)
        faro_izq = (x + 2, y + h - rueda_radio * 2 + 2)
        faro_der = (x + w - 2 - faro_size, y + h - rueda_radio * 2 + 2)
        
        pygame.draw.circle(pantalla, color_faros, faro_izq, faro_size)
        pygame.draw.circle(pantalla, color_faros, faro_der, faro_size)
        pygame.draw.circle(pantalla, (255, 255, 255), faro_izq, faro_size - 1)
        pygame.draw.circle(pantalla, (255, 255, 255), faro_der, faro_size - 1)
        
        luz_trasera_size = max(2, w // 15)
        luz_izq = (x + 2, y + rueda_radio + 2)
        luz_der = (x + w - 2 - luz_trasera_size, y + rueda_radio + 2)
        
        pygame.draw.circle(pantalla, (255, 0, 0), luz_izq, luz_trasera_size)
        pygame.draw.circle(pantalla, (255, 0, 0), luz_der, luz_trasera_size)
        
        pygame.draw.line(pantalla, (0, 0, 0), 
                        (parabrisas.centerx, parabrisas.top), 
                        (parabrisas.centerx, parabrisas.bottom), 1)
        
        manija_izq = (techo_x - 1, techo_y + techo_h // 2)
        manija_der = (techo_x + techo_w + 1, techo_y + techo_h // 2)
        pygame.draw.circle(pantalla, (128, 128, 128), manija_izq, 2)
        pygame.draw.circle(pantalla, (128, 128, 128), manija_der, 2)