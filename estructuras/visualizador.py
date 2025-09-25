# Dibujar el árbol
import pygame
import math

class VisualizadorAVL:
    def __init__(self, ancho=800, alto=600):
        """Inicializa el visualizador del árbol AVL"""
        self.ancho = ancho
        self.alto = alto
        self.pantalla = None
        self.fuente = None
        
        # Colores
        self.BLANCO = (255, 255, 255)
        self.NEGRO = (0, 0, 0)
        self.AZUL = (0, 100, 255)
        self.VERDE = (0, 200, 0)
        self.ROJO = (255, 0, 0)
        self.GRIS = (128, 128, 128)
        
        # Configuración de dibujo
        self.radio_nodo = 25
        self.espaciado_horizontal = 80
        self.espaciado_vertical = 60
        
    def inicializar_pygame(self):
        """Inicializa pygame para la visualización"""
        if self.pantalla is None:
            pygame.init()
            self.pantalla = pygame.display.set_mode((self.ancho, self.alto))
            pygame.display.set_caption("Visualizador Árbol AVL")
            pygame.font.init()
            self.fuente = pygame.font.Font(None, 24)
            
    def dibujar_arbol(self, arbol):
        """Dibuja el árbol AVL completo"""
        if not arbol or arbol.esta_vacio():
            return
            
        self.inicializar_pygame()
        self.pantalla.fill(self.BLANCO)
        
        # Calcular posiciones de los nodos
        posiciones = {}
        self._calcular_posiciones(arbol.raiz, posiciones, 
                                self.ancho // 2, 50, self.ancho // 4)
        
        # Dibujar conexiones primero
        self._dibujar_conexiones(arbol.raiz, posiciones)
        
        # Dibujar nodos encima
        self._dibujar_nodos(arbol.raiz, posiciones)
        
        pygame.display.flip()
        
    def _calcular_posiciones(self, nodo, posiciones, x, y, separacion):
        """Calcula las posiciones de todos los nodos"""
        if nodo is None:
            return
            
        posiciones[nodo] = (x, y)
        
        # Calcular posiciones de los hijos
        nueva_separacion = separacion // 2
        if nodo.izquierdo:
            self._calcular_posiciones(nodo.izquierdo, posiciones,
                                    x - separacion, y + self.espaciado_vertical,
                                    nueva_separacion)
                                    
        if nodo.derecho:
            self._calcular_posiciones(nodo.derecho, posiciones,
                                    x + separacion, y + self.espaciado_vertical,
                                    nueva_separacion)
                                    
    def _dibujar_conexiones(self, nodo, posiciones):
        """Dibuja las líneas que conectan los nodos"""
        if nodo is None:
            return
            
        x, y = posiciones[nodo]
        
        # Dibujar línea al hijo izquierdo
        if nodo.izquierdo:
            x_izq, y_izq = posiciones[nodo.izquierdo]
            pygame.draw.line(self.pantalla, self.GRIS, (x, y), (x_izq, y_izq), 2)
            self._dibujar_conexiones(nodo.izquierdo, posiciones)
            
        # Dibujar línea al hijo derecho
        if nodo.derecho:
            x_der, y_der = posiciones[nodo.derecho]
            pygame.draw.line(self.pantalla, self.GRIS, (x, y), (x_der, y_der), 2)
            self._dibujar_conexiones(nodo.derecho, posiciones)
            
    def _dibujar_nodos(self, nodo, posiciones):
        """Dibuja todos los nodos del árbol"""
        if nodo is None:
            return
            
        x, y = posiciones[nodo]
        
        # Determinar color del nodo según su factor de balance
        factor_balance = nodo.obtener_factor_balance()
        if abs(factor_balance) > 1:
            color_nodo = self.ROJO  # Nodo desbalanceado
        elif factor_balance == 0:
            color_nodo = self.VERDE  # Nodo perfectamente balanceado
        else:
            color_nodo = self.AZUL   # Nodo balanceado
            
        # Dibujar círculo del nodo
        pygame.draw.circle(self.pantalla, color_nodo, (int(x), int(y)), self.radio_nodo)
        pygame.draw.circle(self.pantalla, self.NEGRO, (int(x), int(y)), self.radio_nodo, 2)
        
        # Dibujar texto con la clave
        texto = self.fuente.render(str(nodo.clave), True, self.BLANCO)
        rect_texto = texto.get_rect(center=(int(x), int(y)))
        self.pantalla.blit(texto, rect_texto)
        
        # Dibujar altura del nodo (pequeño)
        altura_texto = pygame.font.Font(None, 16).render(f"h:{nodo.altura}", True, self.NEGRO)
        self.pantalla.blit(altura_texto, (int(x) - 10, int(y) + self.radio_nodo + 5))
        
        # Dibujar factor de balance
        balance_texto = pygame.font.Font(None, 16).render(f"b:{factor_balance}", True, self.NEGRO)
        self.pantalla.blit(balance_texto, (int(x) - 10, int(y) + self.radio_nodo + 20))
        
        # Recursivamente dibujar hijos
        self._dibujar_nodos(nodo.izquierdo, posiciones)
        self._dibujar_nodos(nodo.derecho, posiciones)
        
    def mostrar_estadisticas(self, arbol):
        """Muestra estadísticas del árbol en la pantalla"""
        if arbol.esta_vacio():
            stats_text = [
                "Árbol vacío",
                "Tamaño: 0",
                "Altura: 0"
            ]
        else:
            stats_text = [
                f"Tamaño: {arbol.obtener_tamaño()}",
                f"Altura: {arbol.obtener_altura()}",
                f"Balanceado: {'Sí' if self._es_balanceado(arbol.raiz) else 'No'}"
            ]
            
        y_offset = 10
        for texto in stats_text:
            superficie = self.fuente.render(texto, True, self.NEGRO)
            self.pantalla.blit(superficie, (10, y_offset))
            y_offset += 25
            
    def _es_balanceado(self, nodo):
        """Verifica si el árbol está balanceado"""
        if nodo is None:
            return True
            
        factor_balance = nodo.obtener_factor_balance()
        if abs(factor_balance) > 1:
            return False
            
        return (self._es_balanceado(nodo.izquierdo) and 
                self._es_balanceado(nodo.derecho))
                
    def esperar_evento(self):
        """Espera eventos de pygame"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False
        return True
        
    def cerrar(self):
        """Cierra la ventana de visualización"""
        if self.pantalla:
            pygame.quit()
            
    def guardar_imagen(self, nombre_archivo):
        """Guarda la visualización actual como imagen"""
        if self.pantalla:
            pygame.image.save(self.pantalla, nombre_archivo)