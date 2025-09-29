from collections import deque
import pygame

class ObstaculoNode:
    def __init__(self, obstaculo):
        self.obstaculo = obstaculo
        self.x = obstaculo.x_original if hasattr(obstaculo, 'x_original') and obstaculo.x_original is not None else obstaculo.x
        self.y = obstaculo.y_original if hasattr(obstaculo, 'y_original') and obstaculo.y_original is not None else obstaculo.y
        self.tipo = obstaculo.tipo
        self.altura = 1
        self.izquierdo = None
        self.derecho = None
        
    def comparar_con(self, otro):
        if self.x < otro.x:
            return -1
        elif self.x > otro.x:
            return 1
        elif self.y < otro.y:
            return -1
        elif self.y > otro.y:
            return 1
        else:
            return 0
    
    def obtener_factor_balance(self):
        altura_izq = self.izquierdo.altura if self.izquierdo else 0
        altura_der = self.derecho.altura if self.derecho else 0
        return altura_izq - altura_der
    
    def actualizar_altura(self):
        altura_izq = self.izquierdo.altura if self.izquierdo else 0
        altura_der = self.derecho.altura if self.derecho else 0
        self.altura = 1 + max(altura_izq, altura_der)
    
    def es_hoja(self):
        return self.izquierdo is None and self.derecho is None
    
    def tiene_un_hijo(self):
        return (self.izquierdo is None) != (self.derecho is None)
    
    def obtener_hijo_unico(self):
        return self.izquierdo if self.izquierdo else self.derecho
    
    def __str__(self):
        return f"({self.x},{self.y})-{self.tipo}"

class ArbolAVLObstaculos:
    def __init__(self):
        self.raiz = None
        self.tamaño = 0
        self.recorrido_actual = []
        self.recorridos_guardados = {'inorden': [], 'preorden': [], 'postorden': [], 'anchura': []}
    
    def insertar_obstaculo(self, obstaculo):
        nuevo_nodo = ObstaculoNode(obstaculo)
        if self._coordenadas_existen(nuevo_nodo.x, nuevo_nodo.y):
            print(f"Advertencia: Coordenadas ({nuevo_nodo.x}, {nuevo_nodo.y}) ya existen. No se insertará.")
            return False
        self.raiz = self._insertar_recursivo(self.raiz, nuevo_nodo)
        self.tamaño += 1
        self._actualizar_recorridos()
        return True
    
    def _coordenadas_existen(self, x, y):
        return self._buscar_coordenadas(self.raiz, x, y) is not None
    
    def _buscar_coordenadas(self, nodo, x, y):
        if nodo is None:
            return None
        if x < nodo.x or (x == nodo.x and y < nodo.y):
            return self._buscar_coordenadas(nodo.izquierdo, x, y)
        elif x > nodo.x or (x == nodo.x and y > nodo.y):
            return self._buscar_coordenadas(nodo.derecho, x, y)
        else:
            return nodo
    
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
        resultado = []
        self._postorden_recursivo(self.raiz, resultado)
        return resultado
    
    def _postorden_recursivo(self, nodo, resultado):
        if nodo is not None:
            self._postorden_recursivo(nodo.izquierdo, resultado)
            self._postorden_recursivo(nodo.derecho, resultado)
            resultado.append(nodo)
    
    def recorrido_anchura(self):
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
        return self.recorridos_guardados.get(tipo, [])
    
    def obtener_obstaculos_ordenados(self):
        return [nodo.obstaculo for nodo in self.recorrido_inorden()]
    
    def limpiar(self):
        self.raiz = None
        self.tamaño = 0
        self.recorridos_guardados = {'inorden': [], 'preorden': [], 'postorden': [], 'anchura': []}
    
    def obtener_altura(self):
        return self.raiz.altura if self.raiz else 0
    
    def esta_vacio(self):
        return self.raiz is None
    
    def obtener_tamaño(self):
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
    
    def eliminar_nodo(self, x, y):
        """Elimina un nodo del árbol AVL por coordenadas"""
        if self.raiz is None:
            return False
        
        # Crear nodo temporal para búsqueda
        from game.obstaculo import Obstaculo
        obstaculo_temp = Obstaculo(0, 0, "temp")
        obstaculo_temp.x_original = x
        obstaculo_temp.y_original = y
        nodo_temp = ObstaculoNode(obstaculo_temp)
        
        self.raiz = self._eliminar_recursivo(self.raiz, nodo_temp)
        
        if self.raiz:
            self._actualizar_recorridos()
        
        return True
    
    def _eliminar_recursivo(self, nodo, nodo_a_eliminar):
        """Elimina un nodo recursivamente manteniendo el balance AVL"""
        # Paso 1: Eliminación estándar de BST
        if nodo is None:
            return nodo
        
        comparacion = nodo_a_eliminar.comparar_con(nodo)
        
        if comparacion < 0:
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, nodo_a_eliminar)
        elif comparacion > 0:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, nodo_a_eliminar)
        else:
            # Nodo encontrado, eliminarlo
            self.tamaño -= 1
            
            # Caso 1: Nodo con 0 o 1 hijo
            if nodo.izquierdo is None:
                return nodo.derecho
            elif nodo.derecho is None:
                return nodo.izquierdo
            
            # Caso 2: Nodo con 2 hijos
            # Encontrar el sucesor inorden (nodo más pequeño en subárbol derecho)
            sucesor = self._encontrar_minimo(nodo.derecho)
            
            # Copiar datos del sucesor al nodo actual
            nodo.obstaculo = sucesor.obstaculo
            nodo.x = sucesor.x
            nodo.y = sucesor.y
            nodo.tipo = sucesor.tipo
            
            # Eliminar el sucesor
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, sucesor)
        
        # Paso 2: Actualizar altura
        nodo.actualizar_altura()
        
        # Paso 3: Obtener factor de balance
        balance = nodo.obtener_factor_balance()
        
        # Paso 4: Rebalancear si es necesario
        # Rotación derecha (caso Left-Left)
        if balance > 1 and nodo.izquierdo.obtener_factor_balance() >= 0:
            return self._rotar_derecha(nodo)
        
        # Rotación izquierda (caso Right-Right)
        if balance < -1 and nodo.derecho.obtener_factor_balance() <= 0:
            return self._rotar_izquierda(nodo)
        
        # Rotación izquierda-derecha (caso Left-Right)
        if balance > 1 and nodo.izquierdo.obtener_factor_balance() < 0:
            nodo.izquierdo = self._rotar_izquierda(nodo.izquierdo)
            return self._rotar_derecha(nodo)
        
        # Rotación derecha-izquierda (caso Right-Left)
        if balance < -1 and nodo.derecho.obtener_factor_balance() > 0:
            nodo.derecho = self._rotar_derecha(nodo.derecho)
            return self._rotar_izquierda(nodo)
        
        return nodo
    
    def _encontrar_minimo(self, nodo):
        """Encuentra el nodo con valor mínimo en un subárbol"""
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo
    
    def _rotar_derecha(self, y):
        """Realiza una rotación derecha (Right Rotation)"""
        x = y.izquierdo
        T2 = x.derecho
        
        # Realizar rotación
        x.derecho = y
        y.izquierdo = T2
        
        # Actualizar alturas
        altura_izq_y = y.izquierdo.altura if y.izquierdo else 0
        altura_der_y = y.derecho.altura if y.derecho else 0
        y.altura = 1 + max(altura_izq_y, altura_der_y)
        
        altura_izq_x = x.izquierdo.altura if x.izquierdo else 0
        altura_der_x = x.derecho.altura if x.derecho else 0
        x.altura = 1 + max(altura_izq_x, altura_der_x)
        
        # Retornar nueva raíz
        return x
    
    def _rotar_izquierda(self, x):
        """Realiza una rotación izquierda (Left Rotation)"""
        y = x.derecho
        T2 = y.izquierdo
        
        # Realizar rotación
        y.izquierdo = x
        x.derecho = T2
        
        # Actualizar alturas
        altura_izq_x = x.izquierdo.altura if x.izquierdo else 0
        altura_der_x = x.derecho.altura if x.derecho else 0
        x.altura = 1 + max(altura_izq_x, altura_der_x)
        
        altura_izq_y = y.izquierdo.altura if y.izquierdo else 0
        altura_der_y = y.derecho.altura if y.derecho else 0
        y.altura = 1 + max(altura_izq_y, altura_der_y)
        
        # Retornar nueva raíz
        return y