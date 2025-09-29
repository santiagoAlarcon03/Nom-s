import pygame

class Carretera:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.carriles = 3
        self.ancho_carril = ancho // self.carriles
        self.linea_posicion = 0
        self.velocidad_linea = 3
        
    def actualizar(self):
        self.linea_posicion += self.velocidad_linea
        if self.linea_posicion >= 40:
            self.linea_posicion = 0
            
    def dibujar(self, pantalla, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.ancho_carril = ancho // self.carriles
        pantalla.fill((50, 50, 50))
        for i in range(1, self.carriles):
            x = i * self.ancho_carril
            for y in range(-20 + self.linea_posicion, alto + 20, 40):
                pygame.draw.rect(pantalla, (255, 255, 255), (x - 2, y, 4, 20))
        pygame.draw.rect(pantalla, (255, 255, 255), (0, 0, 4, alto))
        pygame.draw.rect(pantalla, (255, 255, 255), (ancho - 4, 0, 4, alto))

    def dibujar_estatica(self, pantalla, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.ancho_carril = ancho // self.carriles
        pantalla.fill((50, 50, 50))
        for i in range(1, self.carriles):
            x = i * self.ancho_carril
            for y in range(0, alto, 40):
                pygame.draw.rect(pantalla, (255, 255, 255), (x - 2, y, 4, 20))
        pygame.draw.rect(pantalla, (255, 255, 255), (0, 0, 4, alto))
        pygame.draw.rect(pantalla, (255, 255, 255), (ancho - 4, 0, 4, alto))
                
    def obtener_carril_centro(self, numero_carril):
        if 0 <= numero_carril < self.carriles:
            return numero_carril * self.ancho_carril + self.ancho_carril // 2
        return self.ancho // 2