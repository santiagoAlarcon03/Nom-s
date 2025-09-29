import pygame
import math

class VisualizadorArbolAVL:
    """Clase para visualizar gráficamente el árbol AVL de obstáculos"""
    
    def __init__(self, ancho=1000, alto=700):
        self.ancho = ancho
        self.alto = alto
        self.superficie = None
        
        # Colores
        self.BLANCO = (255, 255, 255)
        self.NEGRO = (0, 0, 0)
        self.AZUL = (70, 130, 180)
        self.VERDE = (34, 139, 34)
        self.ROJO = (220, 20, 60)
        self.NARANJA = (255, 140, 0)
        self.MORADO = (138, 43, 226)
        self.GRIS = (128, 128, 128)
        
        # Colores por tipo de obstáculo
        self.colores_obstaculos = {
            'roca': (139, 69, 19),
            'cono': (255, 165, 0),
            'hueco': (64, 64, 64),
            'aceite': (75, 0, 130)
        }
        
        # Configuración de visualización
        self.radio_nodo = 30
        self.espacio_vertical = 80
        self.espacio_horizontal_min = 60
        
        pygame.font.init()
        self.fuente_grande = pygame.font.Font(None, 24)
        self.fuente_pequeña = pygame.font.Font(None, 16)
        self.fuente_titulo = pygame.font.Font(None, 32)
    
    def crear_superficie(self):
        """Crea la superficie para dibujar"""
        self.superficie = pygame.Surface((self.ancho, self.alto))
        return self.superficie
    
    def dibujar_arbol(self, arbol, mostrar_recorrido=None, tipo_recorrido='inorden'):
        """Dibuja el árbol AVL completo"""
        if self.superficie is None:
            self.crear_superficie()
        
        self.superficie.fill(self.BLANCO)
        
        if arbol.esta_vacio():
            self._dibujar_mensaje("Árbol vacío", self.ancho // 2, self.alto // 2)
            return self.superficie
        
        # Calcular posiciones de todos los nodos
        posiciones = self._calcular_posiciones(arbol.raiz)
        
        # Dibujar conexiones primero
        self._dibujar_conexiones(arbol.raiz, posiciones)
        
        # Dibujar nodos
        self._dibujar_nodos(arbol.raiz, posiciones, mostrar_recorrido, tipo_recorrido)
        
        # Dibujar información del árbol
        self._dibujar_info_arbol(arbol)
        
        # Dibujar recorridos si se especifica
        if mostrar_recorrido:
            self._dibujar_recorridos(arbol, tipo_recorrido)
        
        return self.superficie
    
    def _calcular_posiciones(self, raiz):
        """Calcula las posiciones (x, y) de todos los nodos"""
        if raiz is None:
            return {}
        
        posiciones = {}
        
        # Calcular el ancho necesario para el árbol
        ancho_arbol = self._calcular_ancho_arbol(raiz)
        
        # Posición inicial de la raíz
        x_raiz = self.ancho // 2
        y_raiz = 60
        
        self._calcular_posiciones_recursivo(raiz, posiciones, x_raiz, y_raiz, ancho_arbol // 2)
        
        return posiciones
    
    def _calcular_ancho_arbol(self, nodo):
        """Calcula el ancho necesario para dibujar el árbol"""
        if nodo is None:
            return 0
        
        # Contar nodos en el nivel más ancho
        niveles = {}
        self._contar_nodos_por_nivel(nodo, 0, niveles)
        
        max_nodos = max(niveles.values()) if niveles else 1
        return max_nodos * self.espacio_horizontal_min * 2
    
    def _contar_nodos_por_nivel(self, nodo, nivel, niveles):
        """Cuenta los nodos en cada nivel"""
        if nodo is not None:
            niveles[nivel] = niveles.get(nivel, 0) + 1
            self._contar_nodos_por_nivel(nodo.izquierdo, nivel + 1, niveles)
            self._contar_nodos_por_nivel(nodo.derecho, nivel + 1, niveles)
    
    def _calcular_posiciones_recursivo(self, nodo, posiciones, x, y, separacion):
        """Calcula posiciones recursivamente"""
        if nodo is None:
            return
        
        posiciones[nodo] = (x, y)
        
        # Reducir separación para niveles más profundos
        nueva_separacion = max(separacion // 2, self.espacio_horizontal_min)
        
        if nodo.izquierdo:
            self._calcular_posiciones_recursivo(
                nodo.izquierdo, posiciones, 
                x - separacion, y + self.espacio_vertical, nueva_separacion
            )
        
        if nodo.derecho:
            self._calcular_posiciones_recursivo(
                nodo.derecho, posiciones, 
                x + separacion, y + self.espacio_vertical, nueva_separacion
            )
    
    def _dibujar_conexiones(self, nodo, posiciones):
        """Dibuja las líneas que conectan los nodos"""
        if nodo is None or nodo not in posiciones:
            return
        
        x, y = posiciones[nodo]
        
        if nodo.izquierdo and nodo.izquierdo in posiciones:
            x_izq, y_izq = posiciones[nodo.izquierdo]
            pygame.draw.line(self.superficie, self.GRIS, (x, y), (x_izq, y_izq), 2)
            self._dibujar_conexiones(nodo.izquierdo, posiciones)
        
        if nodo.derecho and nodo.derecho in posiciones:
            x_der, y_der = posiciones[nodo.derecho]
            pygame.draw.line(self.superficie, self.GRIS, (x, y), (x_der, y_der), 2)
            self._dibujar_conexiones(nodo.derecho, posiciones)
    
    def _dibujar_nodos(self, nodo, posiciones, mostrar_recorrido, tipo_recorrido):
        """Dibuja todos los nodos del árbol"""
        if nodo is None:
            return
        
        # Obtener orden del recorrido para numeración
        orden_recorrido = {}
        if mostrar_recorrido:
            recorrido = getattr(self, f'_obtener_recorrido_{tipo_recorrido}')(nodo)
            for i, n in enumerate(recorrido):
                orden_recorrido[n] = i + 1
        
        self._dibujar_nodo_individual(nodo, posiciones, orden_recorrido)
        self._dibujar_nodos(nodo.izquierdo, posiciones, mostrar_recorrido, tipo_recorrido)
        self._dibujar_nodos(nodo.derecho, posiciones, mostrar_recorrido, tipo_recorrido)
    
    def _dibujar_nodo_individual(self, nodo, posiciones, orden_recorrido):
        """Dibuja un nodo individual"""
        if nodo not in posiciones:
            return
        
        x, y = posiciones[nodo]
        
        # Color del nodo según tipo de obstáculo
        color_nodo = self.colores_obstaculos.get(nodo.tipo, self.GRIS)
        
        # Dibujar círculo del nodo
        pygame.draw.circle(self.superficie, color_nodo, (int(x), int(y)), self.radio_nodo)
        pygame.draw.circle(self.superficie, self.NEGRO, (int(x), int(y)), self.radio_nodo, 2)
        
        # Dibujar coordenadas
        texto_coords = f"({nodo.x},{nodo.y})"
        superficie_coords = self.fuente_pequeña.render(texto_coords, True, self.BLANCO)
        rect_coords = superficie_coords.get_rect(center=(x, y - 5))
        self.superficie.blit(superficie_coords, rect_coords)
        
        # Dibujar tipo de obstáculo
        superficie_tipo = self.fuente_pequeña.render(nodo.tipo[:4], True, self.BLANCO)
        rect_tipo = superficie_tipo.get_rect(center=(x, y + 8))
        self.superficie.blit(superficie_tipo, rect_tipo)
        
        # Dibujar orden en recorrido si se especifica
        if nodo in orden_recorrido:
            orden = str(orden_recorrido[nodo])
            superficie_orden = self.fuente_pequeña.render(orden, True, self.ROJO)
            rect_orden = superficie_orden.get_rect(center=(x + self.radio_nodo - 5, y - self.radio_nodo + 5))
            pygame.draw.circle(self.superficie, self.BLANCO, rect_orden.center, 8)
            pygame.draw.circle(self.superficie, self.ROJO, rect_orden.center, 8, 1)
            self.superficie.blit(superficie_orden, rect_orden)
        
        # Dibujar altura y factor de balance
        altura_balance = f"h:{nodo.altura} b:{nodo.obtener_factor_balance()}"
        superficie_info = self.fuente_pequeña.render(altura_balance, True, self.NEGRO)
        rect_info = superficie_info.get_rect(center=(x, y + self.radio_nodo + 15))
        self.superficie.blit(superficie_info, rect_info)
    
    def _dibujar_info_arbol(self, arbol):
        """Dibuja información general del árbol"""
        info_y = 10
        
        # Título
        titulo = self.fuente_titulo.render("Árbol AVL de Obstáculos", True, self.NEGRO)
        self.superficie.blit(titulo, (10, info_y))
        info_y += 35
        
        # Información básica
        info_lines = [
            f"Nodos: {arbol.obtener_tamaño()}",
            f"Altura: {arbol.obtener_altura()}",
            f"Estado: {'Balanceado' if arbol.obtener_altura() <= math.log2(arbol.obtener_tamaño() + 1) * 1.44 else 'Revisar'}"
        ]
        
        for line in info_lines:
            superficie_info = self.fuente_pequeña.render(line, True, self.NEGRO)
            self.superficie.blit(superficie_info, (10, info_y))
            info_y += 20
    
    def _dibujar_recorridos(self, arbol, tipo_activo):
        """Dibuja los recorridos del árbol"""
        x_inicio = 10
        y_inicio = self.alto - 180
        
        # Título de recorridos
        titulo_recorridos = self.fuente_grande.render("Recorridos:", True, self.NEGRO)
        self.superficie.blit(titulo_recorridos, (x_inicio, y_inicio))
        y_inicio += 30
        
        tipos_recorrido = ['inorden', 'preorden', 'postorden', 'anchura']
        nombres_recorrido = {
            'inorden': 'En Orden (In)',
            'preorden': 'Pre Orden (Pre)', 
            'postorden': 'Post Orden (Post)',
            'anchura': 'Anchura (BFS)'
        }
        
        for tipo in tipos_recorrido:
            color = self.ROJO if tipo == tipo_activo else self.NEGRO
            recorrido = arbol.obtener_recorrido(tipo)
            
            # Nombre del recorrido
            superficie_nombre = self.fuente_pequeña.render(f"{nombres_recorrido[tipo]}:", True, color)
            self.superficie.blit(superficie_nombre, (x_inicio, y_inicio))
            
            # Secuencia del recorrido
            secuencia = " → ".join([f"({n.x},{n.y})" for n in recorrido])
            if len(secuencia) > 80:  # Truncar si es muy largo
                secuencia = secuencia[:77] + "..."
            
            superficie_secuencia = self.fuente_pequeña.render(secuencia, True, color)
            self.superficie.blit(superficie_secuencia, (x_inicio + 120, y_inicio))
            
            y_inicio += 20
    
    def _obtener_recorrido_inorden(self, nodo):
        """Obtiene recorrido inorden"""
        resultado = []
        if nodo:
            resultado.extend(self._obtener_recorrido_inorden(nodo.izquierdo))
            resultado.append(nodo)
            resultado.extend(self._obtener_recorrido_inorden(nodo.derecho))
        return resultado
    
    def _obtener_recorrido_preorden(self, nodo):
        """Obtiene recorrido preorden"""
        resultado = []
        if nodo:
            resultado.append(nodo)
            resultado.extend(self._obtener_recorrido_preorden(nodo.izquierdo))
            resultado.extend(self._obtener_recorrido_preorden(nodo.derecho))
        return resultado
    
    def _obtener_recorrido_postorden(self, nodo):
        """Obtiene recorrido postorden"""
        resultado = []
        if nodo:
            resultado.extend(self._obtener_recorrido_postorden(nodo.izquierdo))
            resultado.extend(self._obtener_recorrido_postorden(nodo.derecho))
            resultado.append(nodo)
        return resultado
    
    def _obtener_recorrido_anchura(self, nodo):
        """Obtiene recorrido en anchura"""
        if not nodo:
            return []
        
        from collections import deque
        resultado = []
        cola = deque([nodo])
        
        while cola:
            actual = cola.popleft()
            resultado.append(actual)
            
            if actual.izquierdo:
                cola.append(actual.izquierdo)
            if actual.derecho:
                cola.append(actual.derecho)
        
        return resultado
    
    def _dibujar_mensaje(self, mensaje, x, y):
        """Dibuja un mensaje centrado"""
        superficie_mensaje = self.fuente_grande.render(mensaje, True, self.GRIS)
        rect_mensaje = superficie_mensaje.get_rect(center=(x, y))
        self.superficie.blit(superficie_mensaje, rect_mensaje)