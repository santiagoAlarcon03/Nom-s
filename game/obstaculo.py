import pygame

class Obstaculo:
    def __init__(self, x, y, tipo="roca"):
        """Inicializa un obstáculo con tipo específico y daño de energía"""
        self.x = x
        self.y = y
        self.ancho = 40
        self.alto = 40
        self.tipo = tipo
        self.activo = True

        self.propiedades_tipos = {
            "roca": {
                "color": (139, 69, 19),  
                "danio_energia": 25,       
                "descripcion": "Roca grande"
            },
            "cono": {
                "color": (255, 165, 0),    
                "danio_energia": 15,       
                "descripcion": "Cono de tráfico"
            },
            "hueco": {
                "color": (64, 64, 64),   
                "danio_energia": 30,       
                "descripcion": "Hueco en la carretera"
            },
            "aceite": {
                "color": (75, 0, 130),    
                "danio_energia": 10,       
            "descripcion": "Mancha de aceite"
            }
        }
        
        # Establecer propiedades del obstáculo
        if tipo in self.propiedades_tipos:
            self.color = self.propiedades_tipos[tipo]["color"]
            self.danio_energia = self.propiedades_tipos[tipo]["danio_energia"]
            self.descripcion = self.propiedades_tipos[tipo]["descripcion"]
        else:
            self.color = (128, 128, 128)
            self.danio_energia = 20
            self.descripcion = "Obstáculo desconocido"
    
    def mover(self, velocidad):
        """Mueve el obstáculo hacia abajo"""
        self.y += velocidad * 2  # Velocidad de caída
            
    def obtener_rect(self):
        """Retorna el rectángulo de colisión preciso del obstáculo"""
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)
        
    def obtener_danio_energia(self):
        """Retorna el daño de energía que causa este obstáculo"""
        return self.danio_energia
        
    def dibujar(self, pantalla, ancho, alto):
        """Dibuja el obstáculo según su tipo en la pantalla"""
        if self.activo:
            # Escalar para ventana responsiva
            escala_x = ancho / 800
            escala_y = alto / 600
            
            x = int(self.x * escala_x)
            y = int(self.y * escala_y)
            w = int(self.ancho * escala_x)
            h = int(self.alto * escala_y)
            
            rect = pygame.Rect(x, y, w, h)
            
            if self.tipo == "roca":
                # Dibujar como círculo irregular (roca)
                pygame.draw.ellipse(pantalla, self.color, rect)
                pygame.draw.ellipse(pantalla, (0, 0, 0), rect, 2)
                # Pequeñas marcas para textura
                center_x, center_y = rect.center
                pygame.draw.circle(pantalla, (100, 50, 0), (center_x-5, center_y-3), 3)
                pygame.draw.circle(pantalla, (100, 50, 0), (center_x+3, center_y+4), 2)
                
            elif self.tipo == "cono":     
                pygame.draw.rect(pantalla, self.color, rect)
                pygame.draw.polygon(pantalla, (255, 255, 255), [
                    (x + w//2, y + 5), 
                    (x + 5, y + h - 5),
                    (x + w - 5, y + h - 5) 
                ])
                pygame.draw.rect(pantalla, (0, 0, 0), rect, 2)
                
            elif self.tipo == "hueco":
                pygame.draw.ellipse(pantalla, self.color, rect)
                pygame.draw.ellipse(pantalla, (0, 0, 0), rect, 3)
                inner_rect = pygame.Rect(x+5, y+5, w-10, h-10)
                pygame.draw.ellipse(pantalla, (32, 32, 32), inner_rect)
                
            elif self.tipo == "aceite":
                pygame.draw.ellipse(pantalla, self.color, rect)
                center_x, center_y = rect.center
                pygame.draw.circle(pantalla, (138, 43, 226), (center_x-3, center_y-2), w//6)
                pygame.draw.circle(pantalla, (255, 255, 255), (center_x+2, center_y+1), w//8)
                pygame.draw.ellipse(pantalla, (0, 0, 0), rect, 1)
                
            else:
                pygame.draw.rect(pantalla, self.color, rect)
                pygame.draw.rect(pantalla, (0, 0, 0), rect, 2)
        
    def esta_fuera_de_pantalla(self, alto_pantalla):
        """Verifica si el obstáculo ha salido de la pantalla"""
        return self.y > alto_pantalla
    
    def desactivar(self):
        """Desactiva el obstáculo"""
        self.activo = False