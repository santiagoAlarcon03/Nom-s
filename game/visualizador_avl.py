import pygame
import math

class VisualizadorArbolAVL:
    def __init__(self, ancho=1000, alto=700):
        self.ancho = ancho
        self.alto = alto
        self.superficie = None
        self.animacion_activa = False
        self.paso_actual = 0
        self.nodos_recorrido = []
        self.tipo_recorrido_animacion = 'inorden'
        self.tiempo_ultimo_paso = 0
        self.intervalo_animacion = 1000
        self.nodos_visitados = []
        self.nodo_actual = None
        self.modo_eliminacion = False
        self.mensaje_eliminacion = ""
        self.tiempo_mensaje = 0
        self.BLANCO = (255, 255, 255)
        self.NEGRO = (0, 0, 0)
        self.AZUL = (70, 130, 180)
        self.VERDE = (34, 139, 34)
        self.ROJO = (220, 20, 60)
        self.NARANJA = (255, 140, 0)
        self.MORADO = (138, 43, 226)
        self.GRIS = (128, 128, 128)
        self.AMARILLO = (255, 255, 0)
        self.VERDE_CLARO = (144, 238, 144)
        self.colores_obstaculos = {'roca': (139, 69, 19), 'cono': (255, 165, 0), 'hueco': (64, 64, 64), 'aceite': (75, 0, 130)}
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
        
        # Actualizar animación si está activa
        if self.animacion_activa:
            self.actualizar_animacion()
        
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
        
        # Dibujar información de animación si está activa
        if self.animacion_activa:
            self._dibujar_info_animacion()
        
        # Dibujar mensaje de eliminación si existe
        self._dibujar_mensaje_eliminacion()
        
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
        
        # Determinar color según estado de animación
        if self.animacion_activa:
            if nodo == self.nodo_actual:
                # Nodo actual en animación - amarillo brillante
                color_nodo = self.AMARILLO
                borde_color = self.ROJO
                borde_grosor = 4
            elif nodo in self.nodos_visitados:
                # Nodo ya visitado - verde claro
                color_nodo = self.VERDE_CLARO
                borde_color = self.VERDE
                borde_grosor = 3
            else:
                # Nodo no visitado - color original más apagado
                color_original = self.colores_obstaculos.get(nodo.tipo, self.GRIS)
                color_nodo = tuple(c // 2 + 64 for c in color_original)  # Más apagado
                borde_color = self.GRIS
                borde_grosor = 2
        else:
            # Color normal del nodo según tipo de obstáculo
            color_nodo = self.colores_obstaculos.get(nodo.tipo, self.GRIS)
            borde_color = self.NEGRO
            borde_grosor = 2
        
        # Dibujar círculo del nodo
        pygame.draw.circle(self.superficie, color_nodo, (int(x), int(y)), self.radio_nodo)
        pygame.draw.circle(self.superficie, borde_color, (int(x), int(y)), self.radio_nodo, borde_grosor)
        
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
    
    def iniciar_animacion(self, arbol, tipo_recorrido):
        """Inicia la animación de un recorrido específico"""
        if arbol.esta_vacio():
            return
        
        self.animacion_activa = True
        self.paso_actual = 0
        self.tipo_recorrido_animacion = tipo_recorrido
        self.tiempo_ultimo_paso = pygame.time.get_ticks()
        self.nodos_visitados = []
        self.nodo_actual = None
        
        # Obtener secuencia del recorrido
        recorrido_completo = arbol.obtener_recorrido(tipo_recorrido)
        self.nodos_recorrido = recorrido_completo.copy()
        
        print(f"\n🎬 INICIANDO ANIMACIÓN: {tipo_recorrido.upper()}")
        print(f"Pasos totales: {len(self.nodos_recorrido)}")
    
    def detener_animacion(self):
        """Detiene la animación actual"""
        self.animacion_activa = False
        self.paso_actual = 0
        self.nodos_visitados = []
        self.nodo_actual = None
        print("⏹️ Animación detenida")
    
    def actualizar_animacion(self):
        """Actualiza el estado de la animación"""
        if not self.animacion_activa or not self.nodos_recorrido:
            return
        
        tiempo_actual = pygame.time.get_ticks()
        
        # Verificar si es tiempo del siguiente paso
        if tiempo_actual - self.tiempo_ultimo_paso >= self.intervalo_animacion:
            if self.paso_actual < len(self.nodos_recorrido):
                # Mover nodo anterior a visitados
                if self.nodo_actual is not None:
                    self.nodos_visitados.append(self.nodo_actual)
                
                # Obtener siguiente nodo
                self.nodo_actual = self.nodos_recorrido[self.paso_actual]
                self.paso_actual += 1
                self.tiempo_ultimo_paso = tiempo_actual
                
                # Imprimir paso actual
                print(f"Paso {self.paso_actual}: Visitando nodo ({self.nodo_actual.x},{self.nodo_actual.y}) - {self.nodo_actual.tipo}")
                
            else:
                # Animación completa
                if self.nodo_actual is not None:
                    self.nodos_visitados.append(self.nodo_actual)
                    self.nodo_actual = None
                
                print(f"✅ Animación {self.tipo_recorrido_animacion.upper()} completada!")
                self.animacion_activa = False
    
    def cambiar_velocidad_animacion(self, velocidad):
        """Cambia la velocidad de la animación"""
        velocidades = {
            'lenta': 2000,
            'normal': 1000,
            'rapida': 500,
            'muy_rapida': 250
        }
        self.intervalo_animacion = velocidades.get(velocidad, 1000)
        print(f"⚡ Velocidad de animación cambiada a: {velocidad}")
    
    def esta_animando(self):
        """Verifica si hay una animación en curso"""
        return self.animacion_activa
    
    def activar_modo_eliminacion(self):
        """Activa el modo de eliminación de nodos"""
        self.modo_eliminacion = True
        self.nodo_a_eliminar = None
        self.mensaje_eliminacion = "Haz clic en un nodo para eliminarlo"
        self.tiempo_mensaje = pygame.time.get_ticks()
        print(" Modo eliminación activado - Haz clic en un nodo para eliminarlo")
    
    def desactivar_modo_eliminacion(self):
        """Desactiva el modo de eliminación de nodos"""
        self.modo_eliminacion = False
        self.nodo_a_eliminar = None
        self.mensaje_eliminacion = ""
        print("❌ Modo eliminación desactivado")
    
    def manejar_click_eliminacion(self, pos_mouse, arbol):
        """Maneja el click del mouse en modo eliminación"""
        if not self.modo_eliminacion:
            return False
        
        # Calcular posiciones de todos los nodos
        posiciones = self._calcular_posiciones(arbol.raiz)
        
        # Verificar si se hizo clic en algún nodo (usar radio más grande para facilitar selección)
        radio_seleccion = 50  # Radio más grande para facilitar la selección
        for nodo, (x, y) in posiciones.items():
            distancia = math.sqrt((pos_mouse[0] - x)**2 + (pos_mouse[1] - y)**2)
            if distancia <= radio_seleccion:
                # Nodo encontrado, proceder con eliminación
                return self.eliminar_nodo_seleccionado(nodo, arbol)
        
        return False
    
    def eliminar_nodo_seleccionado(self, nodo, arbol):
        """Elimina el nodo seleccionado del árbol"""
        try:
            # Información del nodo a eliminar
            coord_x = nodo.x
            coord_y = nodo.y
            tipo = nodo.tipo
            
            print(f"🗑️ Eliminando nodo: ({coord_x},{coord_y}) - {tipo}")
            
            # Eliminar del árbol AVL
            exito = arbol.eliminar_nodo(coord_x, coord_y)
            
            if exito:
                self.mensaje_eliminacion = f"✅ Nodo ({coord_x},{coord_y})-{tipo} eliminado"
                print(f"✅ Nodo ({coord_x},{coord_y}) - {tipo} eliminado exitosamente")
                print(f"📊 Estadísticas actualizadas - Nodos: {arbol.obtener_tamaño()}, Altura: {arbol.obtener_altura()}")
            else:
                self.mensaje_eliminacion = f"❌ Error al eliminar nodo ({coord_x},{coord_y})-{tipo}"
                print(f"❌ Error al eliminar nodo ({coord_x},{coord_y}) - {tipo}")
            
            self.tiempo_mensaje = pygame.time.get_ticks()
            self.desactivar_modo_eliminacion()
            return exito
            
        except Exception as e:
            self.mensaje_eliminacion = f"❌ Error: {str(e)}"
            self.tiempo_mensaje = pygame.time.get_ticks()
            print(f"❌ Error al eliminar nodo: {e}")
            self.desactivar_modo_eliminacion()
            return False
    
    def _dibujar_info_animacion(self):
        """Dibuja información sobre la animación en curso"""
        if not self.animacion_activa:
            return
        
        # Posición para la información de animación
        x_info = self.ancho - 300
        y_info = 10
        
        # Fondo semitransparente
        pygame.draw.rect(self.superficie, (240, 240, 240), (x_info - 10, y_info - 5, 290, 120))
        pygame.draw.rect(self.superficie, self.NEGRO, (x_info - 10, y_info - 5, 290, 120), 2)
        
        # Título de animación
        titulo = f"🎬 ANIMACIÓN: {self.tipo_recorrido_animacion.upper()}"
        superficie_titulo = self.fuente_grande.render(titulo, True, self.ROJO)
        self.superficie.blit(superficie_titulo, (x_info, y_info))
        y_info += 25
        
        # Progreso
        progreso = f"Paso: {self.paso_actual} / {len(self.nodos_recorrido)}"
        superficie_progreso = self.fuente_pequeña.render(progreso, True, self.NEGRO)
        self.superficie.blit(superficie_progreso, (x_info, y_info))
        y_info += 20
        
        # Nodo actual
        if self.nodo_actual:
            nodo_info = f"Actual: ({self.nodo_actual.x},{self.nodo_actual.y}) - {self.nodo_actual.tipo}"
            superficie_nodo = self.fuente_pequeña.render(nodo_info, True, self.NARANJA)
            self.superficie.blit(superficie_nodo, (x_info, y_info))
        y_info += 20
        
        # Leyenda de colores
        leyenda = [
            ("🟡 Nodo actual", self.AMARILLO),
            ("🟢 Visitado", self.VERDE_CLARO),
            ("⚪ Por visitar", self.GRIS)
        ]
        
        for texto, color in leyenda:
            superficie_leyenda = self.fuente_pequeña.render(texto, True, self.NEGRO)
            self.superficie.blit(superficie_leyenda, (x_info, y_info))
            y_info += 15
    
    def _dibujar_mensaje_eliminacion(self):
        """Dibuja mensajes de eliminación y modo eliminación"""
        if not hasattr(self, 'superficie') or self.superficie is None:
            return
            
        # Mostrar mensaje de eliminación si existe
        if self.mensaje_eliminacion and pygame.time.get_ticks() - self.tiempo_mensaje < 3000:  # 3 segundos
            mensaje_x = 10
            mensaje_y = self.alto - 90
            superficie_mensaje = self.fuente_pequeña.render(self.mensaje_eliminacion, True, self.ROJO if "❌" in self.mensaje_eliminacion else self.VERDE)
            self.superficie.blit(superficie_mensaje, (mensaje_x, mensaje_y))
        
        # Mostrar instrucciones en modo eliminación
        if self.modo_eliminacion:
            instruccion_x = 10
            instruccion_y = self.alto - 60
            superficie_instruccion = self.fuente_pequeña.render("�️ MODO ELIMINACIÓN: Haz clic en un nodo para eliminarlo (ESC para cancelar)", True, self.ROJO)
            self.superficie.blit(superficie_instruccion, (instruccion_x, instruccion_y))
    
