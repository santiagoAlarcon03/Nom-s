import pygame
import json
import os
from .carrito import Carrito
from .carretera import Carretera
from .obstaculo import Obstaculo
from .visualizador_avl import VisualizadorArbolAVL
from estructuras.arbol_avl_obstaculos import ArbolAVLObstaculos

class Motor:
    def __init__(self):
        self.ancho_pantalla = 800
        self.alto_pantalla = 600
        self.carretera = Carretera(self.ancho_pantalla, self.alto_pantalla)
        self.carrito = Carrito(self.ancho_pantalla // 2 - 25, self.alto_pantalla - 50)
        self.obstaculos = []
        self.obstaculos_predefinidos = []
        self.arbol_obstaculos = ArbolAVLObstaculos()
        self.visualizador_avl = VisualizadorArbolAVL()
        self.mostrar_arbol = False
        self.tipo_recorrido_actual = 'inorden'
        self.juego_activo = True
        self.velocidad_juego = 1.0
        self.velocidad_carrito_x = 2.0
        self.carril_actual = 1
        self.total_carriles = 3
        self.posiciones_carriles = []
        self.cargar_obstaculos_json()
        
    def manejar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                if self.carril_actual > 0:
                    self.carril_actual -= 1
                    self.actualizar_posicion_carril()
            elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                if self.carril_actual < self.total_carriles - 1:
                    self.carril_actual += 1
                    self.actualizar_posicion_carril()
            elif evento.key == pygame.K_SPACE:
                self.carrito.saltar()
            elif evento.key == pygame.K_t:
                self.mostrar_arbol = not self.mostrar_arbol
            elif evento.key == pygame.K_1:
                self.tipo_recorrido_actual = 'inorden'
            elif evento.key == pygame.K_2:
                self.tipo_recorrido_actual = 'preorden'
            elif evento.key == pygame.K_3:
                self.tipo_recorrido_actual = 'postorden'
            elif evento.key == pygame.K_4:
                self.tipo_recorrido_actual = 'anchura'
            elif evento.key == pygame.K_5:
                if self.mostrar_arbol:
                    if self.visualizador_avl.modo_eliminacion:
                        self.visualizador_avl.desactivar_modo_eliminacion()
                    else:
                        self.visualizador_avl.activar_modo_eliminacion()
            elif evento.key == pygame.K_q:
                if self.mostrar_arbol and not self.visualizador_avl.esta_animando():
                    self.visualizador_avl.iniciar_animacion(self.arbol_obstaculos, self.tipo_recorrido_actual)
            elif evento.key == pygame.K_e:
                if self.visualizador_avl.esta_animando():
                    self.visualizador_avl.detener_animacion()
            elif evento.key == pygame.K_MINUS:
                self.visualizador_avl.cambiar_velocidad_animacion('lenta')
            elif evento.key == pygame.K_EQUALS:
                self.visualizador_avl.cambiar_velocidad_animacion('rapida')
            elif evento.key == pygame.K_0:
                self.visualizador_avl.cambiar_velocidad_animacion('normal')
            elif evento.key == pygame.K_r and not self.juego_activo:
                self.reiniciar_juego()
            elif evento.key == pygame.K_ESCAPE:
                if self.visualizador_avl.modo_eliminacion:
                    self.visualizador_avl.desactivar_modo_eliminacion()
                else:
                    return False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1 and self.mostrar_arbol and self.visualizador_avl.modo_eliminacion:
                if self.visualizador_avl.manejar_click_eliminacion(evento.pos, self.arbol_obstaculos):
                    self.imprimir_recorridos()
        elif evento.type == pygame.VIDEORESIZE:
            self.ancho_pantalla = evento.w
            self.alto_pantalla = evento.h
            self.calcular_posiciones_carriles()
                    
    def cargar_obstaculos_json(self):
        try:
            ruta_json = os.path.join(os.path.dirname(__file__), "..", "obstaculos.json")
            with open(ruta_json, 'r', encoding='utf-8') as archivo:
                datos_obstaculos = json.load(archivo)
            self.obstaculos_predefinidos = []
            self.arbol_obstaculos = ArbolAVLObstaculos()
            for obs_data in datos_obstaculos:
                self.crear_obstaculo_en_posicion(obs_data["x"], obs_data["y"], obs_data["tipo"])
            self.imprimir_recorridos()
        except FileNotFoundError:
            print("Archivo obstaculos.json no encontrado. No se cargarán obstáculos.")
        except json.JSONDecodeError:
            print("Error al leer obstaculos.json. Formato JSON inválido.")
        except Exception as e:
            print(f"Error al cargar obstáculos: {e}")

    def crear_obstaculo_en_posicion(self, distancia, carril, tipo):
        ancho_carril = self.ancho_pantalla // self.total_carriles
        pos_x = (carril * ancho_carril) + (ancho_carril // 2) - 20
        pos_y = (self.alto_pantalla - 50) - distancia
        obstaculo = Obstaculo(pos_x, pos_y, tipo)
        obstaculo.x_original = distancia
        obstaculo.y_original = carril
        self.obstaculos_predefinidos.append(obstaculo)
        if self.arbol_obstaculos.insertar_obstaculo(obstaculo):
            print(f"Obstáculo insertado en AVL: ({distancia}, {carril}) - {tipo}")
        else:
            print(f"Error: Obstáculo duplicado en ({distancia}, {carril})")
            self.obstaculos_predefinidos.remove(obstaculo)
        
    def actualizar(self):
        if not self.juego_activo:
            return
        if not self.posiciones_carriles:
            self.calcular_posiciones_carriles()
            self.actualizar_posicion_carril()
        self.carrito.actualizar_salto()
        self.carrito.y -= self.velocidad_carrito_x
        if self.carrito.y < -self.carrito.alto:
            self.carrito.y = self.alto_pantalla
        self.actualizar_obstaculos_visibles()
        for obstaculo in self.obstaculos:
            if self.verificar_colision(self.carrito, obstaculo):
                if not self.carrito.esta_saltando():
                    danio = obstaculo.obtener_danio_energia()
                    sin_energia = self.carrito.reducir_energia(danio)
                    if sin_energia:
                        self.juego_activo = False
                obstaculo.desactivar()
        self.velocidad_juego += 0.001
        self.velocidad_carrito_x += 0.001
        
    def verificar_colision(self, carrito, obstaculo):
        if not obstaculo.activo:
            return False
        rect_carrito = carrito.obtener_rect()
        rect_obstaculo = obstaculo.obtener_rect()
        rect_carrito_reducido = pygame.Rect(rect_carrito.x + 2, rect_carrito.y + 2, 
                                          rect_carrito.width - 4, rect_carrito.height - 4)
        rect_obstaculo_reducido = pygame.Rect(rect_obstaculo.x + 2, rect_obstaculo.y + 2, 
                                            rect_obstaculo.width - 4, rect_obstaculo.height - 4)
        return rect_carrito_reducido.colliderect(rect_obstaculo_reducido)
    
    def calcular_posiciones_carriles(self):
        ancho_carril = self.ancho_pantalla // self.total_carriles
        self.posiciones_carriles = []
        for i in range(self.total_carriles):
            posicion_x = (i * ancho_carril) + (ancho_carril // 2) - (self.carrito.ancho // 2)
            self.posiciones_carriles.append(posicion_x)
        self.recalcular_posiciones_obstaculos()
        
    def recalcular_posiciones_obstaculos(self):
        if hasattr(self, 'obstaculos_predefinidos'):
            ancho_carril = self.ancho_pantalla // self.total_carriles
            for obstaculo in self.obstaculos_predefinidos:
                carril_actual = min(2, max(0, int(obstaculo.x // ancho_carril)))
                obstaculo.x = (carril_actual * ancho_carril) + (ancho_carril // 2) - 20
    
    def actualizar_posicion_carril(self):
        if self.posiciones_carriles:
            self.carrito.x = self.posiciones_carriles[self.carril_actual]
            
    def actualizar_obstaculos_visibles(self):
        self.obstaculos = []
        margen = 200
        limite_superior = self.carrito.y + margen
        limite_inferior = self.carrito.y - self.alto_pantalla - margen
        for obstaculo in self.obstaculos_predefinidos:
            if obstaculo.activo and limite_inferior <= obstaculo.y <= limite_superior:
                self.obstaculos.append(obstaculo)
        
    def reiniciar_juego(self):
        self.obstaculos.clear()
        self.arbol_obstaculos = ArbolAVLObstaculos()
        self.juego_activo = True
        self.velocidad_juego = 1.0
        self.velocidad_carrito_x = 2.0
        self.carrito.x = self.ancho_pantalla // 2 - 25
        self.carrito.y = self.alto_pantalla - 50
        self.carrito.energia_actual = self.carrito.energia_maxima
        self.carrito.saltando = False
        self.carrito.tiempo_salto = 0
        self.cargar_obstaculos_json()
        for obstaculo in self.obstaculos_predefinidos:
            obstaculo.activo = True
    
    def obtener_superficie_arbol(self):
        if self.mostrar_arbol and not self.arbol_obstaculos.esta_vacio():
            return self.visualizador_avl.dibujar_arbol(self.arbol_obstaculos, 
                                                     mostrar_recorrido=True, 
                                                     tipo_recorrido=self.tipo_recorrido_actual)
        return None
    
    def imprimir_recorridos(self):
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