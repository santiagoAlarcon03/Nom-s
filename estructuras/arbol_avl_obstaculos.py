from .nodo_avl import NodoAVL
from collections import deque
import pygame

class ObstaculoNode:
    """Representa un nodo del árbol AVL que contiene un obstáculo"""
    def __init__(self, obstaculo):
        self.obstaculo = obstaculo
        # Usar coordenadas originales del JSON para comparación en AVL
        self.x = obstaculo.x_original if hasattr(obstaculo, 'x_original') and obstaculo.x_original is not None else obstaculo.x
        self.y = obstaculo.y_original if hasattr(obstaculo, 'y_original') and obstaculo.y_original is not None else obstaculo.y
        self.tipo = obstaculo.tipo
        self.altura = 1
        self.izquierdo = None
        self.derecho = None
        
    def comparar_con(self, otro):
        """Compara este nodo con otro según las reglas especificadas"""
        # Primero comparar x
        if self.x < otro.x:
            return -1
        elif self.x > otro.x:
            return 1
        else:
            # En caso de empate en x, comparar y
            if self.y < otro.y:
                return -1
            elif self.y > otro.y:
                return 1
            else:
                return 0  # Coordenadas idénticas (no permitidas)
    
    def obtener_factor_balance(self):
        """Calcula el factor de balance del nodo"""
        altura_izq = self.izquierdo.altura if self.izquierdo else 0
        altura_der = self.derecho.altura if self.derecho else 0
        return altura_izq - altura_der
    
    def actualizar_altura(self):
        """Actualiza la altura del nodo"""
        altura_izq = self.izquierdo.altura if self.izquierdo else 0
        altura_der = self.derecho.altura if self.derecho else 0
        self.altura = 1 + max(altura_izq, altura_der)
    
    def es_hoja(self):
        """Verifica si el nodo es una hoja"""
        return self.izquierdo is None and self.derecho is None
    
    def tiene_un_hijo(self):
        """Verifica si el nodo tiene exactamente un hijo"""
        return (self.izquierdo is None) != (self.derecho is None)
    
    def obtener_hijo_unico(self):
        """Obtiene el único hijo del nodo"""
        return self.izquierdo if self.izquierdo else self.derecho
    
    def __str__(self):
        return f"({self.x},{self.y})-{self.tipo}"

class ArbolAVLObstaculos:
    """Árbol AVL específico para gestionar obstáculos del juego"""
    
    def __init__(self):
        self.raiz = None
        self.tamaño = 0
        self.recorrido_actual = []
        self.recorridos_guardados = {
            'inorden': [],
            'preorden': [],
            'postorden': [],
            'anchura': []
        }
    
    def insertar_obstaculo(self, obstaculo):
        """Inserta un obstáculo en el árbol AVL"""
        nuevo_nodo = ObstaculoNode(obstaculo)
        if self._coordenadas_existen(nuevo_nodo.x, nuevo_nodo.y):
            print(f"Advertencia: Coordenadas ({nuevo_nodo.x}, {nuevo_nodo.y}) ya existen. No se insertará.")
            return False
        
        self.raiz = self._insertar_recursivo(self.raiz, nuevo_nodo)
        self.tamaño += 1
        self._actualizar_recorridos()
        return True
    
    def _coordenadas_existen(self, x, y):
        """Verifica si las coordenadas ya existen en el árbol"""
        return self._buscar_coordenadas(self.raiz, x, y) is not None
    
    def _buscar_coordenadas(self, nodo, x, y):
        """Busca un nodo con las coordenadas especificadas"""
        if nodo is None:
            return None
        
        if x < nodo.x or (x == nodo.x and y < nodo.y):
            return self._buscar_coordenadas(nodo.izquierdo, x, y)
        elif x > nodo.x or (x == nodo.x and y > nodo.y):
            return self._buscar_coordenadas(nodo.derecho, x, y)
        else:
            return nodo  # Coordenadas encontradas
    
    def _insertar_recursivo(self, nodo, nuevo_nodo):
        """Inserción recursiva con balanceo AVL"""
        # Caso base
        if nodo is None:
            return nuevo_nodo
        
        # Comparación según las reglas especificadas
        comparacion = nuevo_nodo.comparar_con(nodo)
        
        if comparacion < 0:
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, nuevo_nodo)
        elif comparacion > 0:
            nodo.derecho = self._insertar_recursivo(nodo.derecho, nuevo_nodo)
        else:
            # Coordenadas idénticas - no debería pasar si verificamos antes
            return nodo
        
        # Actualizar altura
        nodo.actualizar_altura()
        
        # Obtener factor de balance
        balance = nodo.obtener_factor_balance()
        
        # Realizar rotaciones si es necesario
        # Caso Izquierda-Izquierda
        if balance > 1 and nuevo_nodo.comparar_con(nodo.izquierdo) < 0:
            return self._rotacion_derecha(nodo)
        
        # Caso Derecha-Derecha
        if balance < -1 and nuevo_nodo.comparar_con(nodo.derecho) > 0:
            return self._rotacion_izquierda(nodo)
        
        # Caso Izquierda-Derecha
        if balance > 1 and nuevo_nodo.comparar_con(nodo.izquierdo) > 0:
            nodo.izquierdo = self._rotacion_izquierda(nodo.izquierdo)
            return self._rotacion_derecha(nodo)
        
        # Caso Derecha-Izquierda
        if balance < -1 and nuevo_nodo.comparar_con(nodo.derecho) < 0:
            nodo.derecho = self._rotacion_derecha(nodo.derecho)
            return self._rotacion_izquierda(nodo)
        
        return nodo
    
    def _rotacion_izquierda(self, z):
        """Rotación simple a la izquierda"""
        y = z.derecho
        T2 = y.izquierdo
        
        y.izquierdo = z
        z.derecho = T2
        
        z.actualizar_altura()
        y.actualizar_altura()
        
        return y
    
    def _rotacion_derecha(self, z):
        """Rotación simple a la derecha"""
        y = z.izquierdo
        T3 = y.derecho
        
        y.derecho = z
        z.izquierdo = T3
        
        z.actualizar_altura()
        y.actualizar_altura()
        
        return y
    
    def _actualizar_recorridos(self):
        """Actualiza todos los recorridos del árbol"""
        self.recorridos_guardados['inorden'] = self.recorrido_inorden()
        self.recorridos_guardados['preorden'] = self.recorrido_preorden()
        self.recorridos_guardados['postorden'] = self.recorrido_postorden()
        self.recorridos_guardados['anchura'] = self.recorrido_anchura()
    
    def recorrido_inorden(self):
        """Recorrido en profundidad: Inorden (Izquierdo-Raíz-Derecho)"""
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado
    
    def _inorden_recursivo(self, nodo, resultado):
        if nodo is not None:
            self._inorden_recursivo(nodo.izquierdo, resultado)
            resultado.append(nodo)
            self._inorden_recursivo(nodo.derecho, resultado)
    
    def recorrido_preorden(self):
        """Recorrido en profundidad: Preorden (Raíz-Izquierdo-Derecho)"""
        resultado = []
        self._preorden_recursivo(self.raiz, resultado)
        return resultado
    
    def _preorden_recursivo(self, nodo, resultado):
        if nodo is not None:
            resultado.append(nodo)
            self._preorden_recursivo(nodo.izquierdo, resultado)
            self._preorden_recursivo(nodo.derecho, resultado)
    
    def recorrido_postorden(self):
        """Recorrido en profundidad: Postorden (Izquierdo-Derecho-Raíz)"""
        resultado = []
        self._postorden_recursivo(self.raiz, resultado)
        return resultado
    
    def _postorden_recursivo(self, nodo, resultado):
        if nodo is not None:
            self._postorden_recursivo(nodo.izquierdo, resultado)
            self._postorden_recursivo(nodo.derecho, resultado)
            resultado.append(nodo)
    
    def recorrido_anchura(self):
        """Recorrido en anchura (BFS - Breadth-First Search)"""
        if self.raiz is None:
            return []
        
        resultado = []
        cola = deque([self.raiz])
        
        while cola:
            nodo = cola.popleft()
            resultado.append(nodo)
            
            if nodo.izquierdo:
                cola.append(nodo.izquierdo)
            if nodo.derecho:
                cola.append(nodo.derecho)
        
        return resultado
    
    def obtener_recorrido(self, tipo):
        """Obtiene un recorrido específico"""
        return self.recorridos_guardados.get(tipo, [])
    
    def obtener_obstaculos_ordenados(self):
        """Obtiene todos los obstáculos en orden (inorden)"""
        return [nodo.obstaculo for nodo in self.recorrido_inorden()]
    
    def limpiar(self):
        """Limpia el árbol"""
        self.raiz = None
        self.tamaño = 0
        self.recorridos_guardados = {
            'inorden': [],
            'preorden': [],
            'postorden': [],
            'anchura': []
        }
    
    def obtener_altura(self):
        """Obtiene la altura del árbol"""
        return self.raiz.altura if self.raiz else 0
    
    def esta_vacio(self):
        """Verifica si el árbol está vacío"""
        return self.raiz is None
    
    def obtener_tamaño(self):
        """Obtiene el número de nodos en el árbol"""
        return self.tamaño
    
    def imprimir_estructura(self):
        """Imprime la estructura del árbol para debugging"""
        print("Estructura del Árbol AVL:")
        self._imprimir_nodo(self.raiz, "", True)
    
    def _imprimir_nodo(self, nodo, prefijo, es_ultimo):
        if nodo is not None:
            print(f"{prefijo}{'└── ' if es_ultimo else '├── '}{nodo} (h:{nodo.altura}, b:{nodo.obtener_factor_balance()})")
            
            if nodo.izquierdo or nodo.derecho:
                if nodo.derecho:
                    self._imprimir_nodo(nodo.derecho, prefijo + ("    " if es_ultimo else "│   "), not nodo.izquierdo)
                if nodo.izquierdo:
                    self._imprimir_nodo(nodo.izquierdo, prefijo + ("    " if es_ultimo else "│   "), True)