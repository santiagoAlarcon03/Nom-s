# Lógica de movimiento y colisiones
import pygame
import random
import json
import os
from .carrito import Carrito
from .carretera import Carretera
from .obstaculo import Obstaculo
from .visualizador_avl import VisualizadorArbolAVL
from estructuras.arbol_avl_obstaculos import ArbolAVLObstaculos

class Motor:
    def __init__(self):
        """Inicializa el motor del juego"""
        self.ancho_pantalla = 800
        self.alto_pantalla = 600
        # Componentes del juego
        self.carretera = Carretera(self.ancho_pantalla, self.alto_pantalla)
        self.carrito = Carrito(
            self.ancho_pantalla // 2 - 25,  # Centro horizontal (controla carril)
            self.alto_pantalla - 50  # Parte inferior (se moverá automáticamente hacia arriba)
        )
        # Lista de obstáculos
        self.obstaculos = []
        self.obstaculos_predefinidos = []  # Obstáculos cargados desde JSON
        # Árbol AVL para gestionar obstáculos
        self.arbol_obstaculos = ArbolAVLObstaculos()
        
        # Visualizador del árbol AVL
        self.visualizador_avl = VisualizadorArbolAVL()
        self.mostrar_arbol = False
        self.tipo_recorrido_actual = 'inorden'
        # Puntuación y estado del juego
        self.puntuacion = 0
        self.juego_activo = True
        self.velocidad_juego = 1.0
        
        # Sistema de movimiento automático del carrito
        self.velocidad_carrito_x = 2.0  # Velocidad de movimiento horizontal automático
        
        # Sistema de carriles
        self.carril_actual = 1  # Carril central (0=izquierdo, 1=central, 2=derecho)
        self.total_carriles = 3
        self.posiciones_carriles = []  # Se calculará dinámicamente según el ancho de pantalla
        self.cargar_obstaculos_json()
        
    def manejar_eventos(self, evento):
        """Maneja los eventos del teclado y el redimensionamiento"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                # Cambiar al carril izquierdo
                if self.carril_actual > 0:
                    self.carril_actual -= 1
                    self.actualizar_posicion_carril()
            elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                # Cambiar al carril derecho
                if self.carril_actual < self.total_carriles - 1:
                    self.carril_actual += 1
                    self.actualizar_posicion_carril()
            elif evento.key == pygame.K_SPACE:
                # Saltar con la barra espaciadora
                self.carrito.saltar()
            elif evento.key == pygame.K_t:
                # Mostrar/ocultar árbol AVL
                self.mostrar_arbol = not self.mostrar_arbol
            elif evento.key == pygame.K_1:
                self.tipo_recorrido_actual = 'inorden'
            elif evento.key == pygame.K_2:
                self.tipo_recorrido_actual = 'preorden'
            elif evento.key == pygame.K_3:
                self.tipo_recorrido_actual = 'postorden'
            elif evento.key == pygame.K_4:
                self.tipo_recorrido_actual = 'anchura'
            elif evento.key == pygame.K_r and not self.juego_activo:
                # Reiniciar juego
                self.reiniciar_juego()
            elif evento.key == pygame.K_ESCAPE:
                # Salir del juego
                return False
        elif evento.type == pygame.VIDEORESIZE:
            self.ancho_pantalla = evento.w
            self.alto_pantalla = evento.h
            self.calcular_posiciones_carriles()  # Recalcular carriles al redimensionar
                    
    def cargar_obstaculos_json(self):
        """Carga obstáculos predefinidos exactamente desde el archivo JSON"""
        try:
            ruta_json = os.path.join(os.path.dirname(__file__), "..", "obstaculos.json")
            with open(ruta_json, 'r', encoding='utf-8') as archivo:
                datos_obstaculos = json.load(archivo)
                
            self.obstaculos_predefinidos = []
            self.arbol_obstaculos = ArbolAVLObstaculos()
            
            for obs_data in datos_obstaculos:
                # Usar coordenadas exactas del JSON sin modificaciones
                self.crear_obstaculo_en_posicion(obs_data["x"], obs_data["y"], obs_data["tipo"])
            
            # Imprimir recorridos después de cargar todos los obstáculos
            self.imprimir_recorridos()
                
        except FileNotFoundError:
            print("Archivo obstaculos.json no encontrado. No se cargarán obstáculos.")
        except json.JSONDecodeError:
            print("Error al leer obstaculos.json. Formato JSON inválido.")
        except Exception as e:
            print(f"Error al cargar obstáculos: {e}")
        

                
    def crear_obstaculo_en_posicion(self, distancia, carril, tipo):
        """Crea un obstáculo en la posición especificada"""
        # Calcular posición X basada en el carril
        ancho_carril = self.ancho_pantalla // self.total_carriles
        pos_x = (carril * ancho_carril) + (ancho_carril // 2) - 20  # Centrar en carril
        
        # La posición Y: convertir distancia a coordenadas de pantalla
        pos_y = (self.alto_pantalla - 50) - distancia
        
        # Crear obstáculo con coordenadas originales del JSON
        obstaculo = Obstaculo(pos_x, pos_y, tipo)
        # Agregar las coordenadas originales como propiedades adicionales
        obstaculo.x_original = distancia  # Coordenada X original del JSON
        obstaculo.y_original = carril     # Coordenada Y original del JSON (carril)
        
        self.obstaculos_predefinidos.append(obstaculo)
        
        # Insertar en el árbol AVL usando las coordenadas originales del JSON
        if self.arbol_obstaculos.insertar_obstaculo(obstaculo):
            print(f"Obstáculo insertado en AVL: ({distancia}, {carril}) - {tipo}")
        else:
            print(f"Error: Obstáculo duplicado en ({distancia}, {carril})")
            # Remover de la lista si no se pudo insertar
            self.obstaculos_predefinidos.remove(obstaculo)
        
    def actualizar(self):
        """Actualiza la lógica del juego"""
        if not self.juego_activo:
            return
            
        # Calcular posiciones de carriles si es necesario
        if not self.posiciones_carriles:
            self.calcular_posiciones_carriles()
            self.actualizar_posicion_carril()
        
        # Actualizar sistema de salto del carrito
        self.carrito.actualizar_salto()
        
        # Mover carrito automáticamente en el eje Y (que aparece horizontal en pantalla rotada)
        self.carrito.y -= self.velocidad_carrito_x
        
        # Si el carrito sale por arriba, vuelve a aparecer por abajo
        if self.carrito.y < -self.carrito.alto:
            self.carrito.y = self.alto_pantalla
            
        # La carretera ahora es estática (no se actualiza)
        
        # Actualizar lista de obstáculos visibles (los que están cerca del carrito)
        self.actualizar_obstaculos_visibles()
        
        # Verificar colisiones con obstáculos predefinidos
        for obstaculo in self.obstaculos:
            if self.verificar_colision(self.carrito, obstaculo):
                # Si está saltando, no pierde energía y obtiene puntos bonus
                if self.carrito.esta_saltando():
                    # Puntos bonus por saltar sobre el obstáculo
                    self.puntuacion += 15
                else:
                    # Reducir energía del carrito según el tipo de obstáculo
                    danio = obstaculo.obtener_danio_energia()
                    sin_energia = self.carrito.reducir_energia(danio)
                    
                    # Agregar puntos por el obstáculo superado (aunque haya causado daño)
                    self.puntuacion += 5
                    
                    # Terminar juego si se queda sin energía
                    if sin_energia:
                        self.juego_activo = False
                
                # Desactivar obstáculo después de la colisión
                obstaculo.desactivar()
        
        # Aumentar puntuación por distancia recorrida
        self.puntuacion += 0.1
                
        # Aumentar velocidad gradualmente
        self.velocidad_juego += 0.001
        self.velocidad_carrito_x += 0.001  # También aumentar velocidad del carrito
        
    def verificar_colision(self, carrito, obstaculo):
        """Verifica si hay colisión entre el carrito y un obstáculo"""
        if not obstaculo.activo:
            return False
            
        rect_carrito = carrito.obtener_rect()
        rect_obstaculo = obstaculo.obtener_rect()
        
        # Colisión más estricta: reducir ligeramente las áreas de colisión para mayor precisión
        rect_carrito_reducido = pygame.Rect(
            rect_carrito.x + 2, 
            rect_carrito.y + 2, 
            rect_carrito.width - 4, 
            rect_carrito.height - 4
        )
        rect_obstaculo_reducido = pygame.Rect(
            rect_obstaculo.x + 2, 
            rect_obstaculo.y + 2, 
            rect_obstaculo.width - 4, 
            rect_obstaculo.height - 4
        )
        
        return rect_carrito_reducido.colliderect(rect_obstaculo_reducido)
    
    def calcular_posiciones_carriles(self):
        """Calcula las posiciones X de cada carril"""
        ancho_carril = self.ancho_pantalla // self.total_carriles
        self.posiciones_carriles = []
        for i in range(self.total_carriles):
            # Centrar el carrito en cada carril
            posicion_x = (i * ancho_carril) + (ancho_carril // 2) - (self.carrito.ancho // 2)
            self.posiciones_carriles.append(posicion_x)
            
        # Recalcular posiciones de obstáculos predefinidos cuando cambie el tamaño de ventana
        self.recalcular_posiciones_obstaculos()
        
    def recalcular_posiciones_obstaculos(self):
        """Recalcula las posiciones X de los obstáculos según el nuevo ancho de pantalla"""
        if hasattr(self, 'obstaculos_predefinidos'):
            ancho_carril = self.ancho_pantalla // self.total_carriles
            for obstaculo in self.obstaculos_predefinidos:
                # Determinar en qué carril estaba originalmente
                carril_actual = min(2, max(0, int(obstaculo.x // ancho_carril)))
                # Reposicionar en el mismo carril con nuevo ancho
                obstaculo.x = (carril_actual * ancho_carril) + (ancho_carril // 2) - 20
    
    def actualizar_posicion_carril(self):
        """Actualiza la posición X del carrito según el carril actual"""
        if self.posiciones_carriles:
            self.carrito.x = self.posiciones_carriles[self.carril_actual]
            
    def actualizar_obstaculos_visibles(self):
        """Actualiza la lista de obstáculos visibles según la posición del carrito"""
        # Limpiar lista de obstáculos visibles
        self.obstaculos = []
        
        # Rango de visibilidad: obstáculos que están cerca del carrito
        margen = 200
        limite_superior = self.carrito.y + margen  # Detrás del carrito
        limite_inferior = self.carrito.y - self.alto_pantalla - margen  # Adelante del carrito
        
        # Agregar obstáculos predefinidos que están en el rango visible
        for obstaculo in self.obstaculos_predefinidos:
            if obstaculo.activo and limite_inferior <= obstaculo.y <= limite_superior:
                self.obstaculos.append(obstaculo)
        
    def reiniciar_juego(self):
        """Reinicia el juego"""
        self.obstaculos.clear()
        self.arbol_obstaculos = ArbolAVLObstaculos()
        self.puntuacion = 0
        self.juego_activo = True
        self.velocidad_juego = 1.0
        self.velocidad_carrito_x = 2.0  # Resetear velocidad del carrito
        self.carrito.x = self.ancho_pantalla // 2 - 25
        self.carrito.y = self.alto_pantalla - 50  # Posición inicial en la parte inferior  
        self.carrito.energia_actual = self.carrito.energia_maxima
        # Resetear estado de salto
        self.carrito.saltando = False
        self.carrito.tiempo_salto = 0
        
        # Recargar obstáculos desde JSON y reactivar todos
        self.cargar_obstaculos_json()
        for obstaculo in self.obstaculos_predefinidos:
            obstaculo.activo = True
    
    def obtener_superficie_arbol(self):
        """Obtiene la superficie renderizada del árbol AVL"""
        if self.mostrar_arbol and not self.arbol_obstaculos.esta_vacio():
            return self.visualizador_avl.dibujar_arbol(
                self.arbol_obstaculos, 
                mostrar_recorrido=True, 
                tipo_recorrido=self.tipo_recorrido_actual
            )
        return None
    
    def imprimir_recorridos(self):
        """Imprime todos los recorridos del árbol en consola"""
        print("\n" + "="*50)
        print("RECORRIDOS DEL ÁRBOL AVL DE OBSTÁCULOS")
        print("="*50)
        
        if self.arbol_obstaculos.esta_vacio():
            print("El árbol está vacío")
            return
        
        tipos_recorrido = {
            'inorden': 'RECORRIDO EN ORDEN (Izq-Raíz-Der)',
            'preorden': 'RECORRIDO PRE ORDEN (Raíz-Izq-Der)',
            'postorden': 'RECORRIDO POST ORDEN (Izq-Der-Raíz)',
            'anchura': 'RECORRIDO EN ANCHURA (BFS)'
        }
        
        for tipo, nombre in tipos_recorrido.items():
            print(f"\n{nombre}:")
            recorrido = self.arbol_obstaculos.obtener_recorrido(tipo)
            secuencia = []
            for i, nodo in enumerate(recorrido, 1):
                secuencia.append(f"{i}.({nodo.x},{nodo.y})-{nodo.tipo}")
            print(" → ".join(secuencia))
        
        print(f"\nESTADÍSTICAS DEL ÁRBOL:")
        print(f"- Nodos: {self.arbol_obstaculos.obtener_tamaño()}")
        print(f"- Altura: {self.arbol_obstaculos.obtener_altura()}")
        print("="*50 + "\n")