# Implementación AVL
from .nodo_avl import NodoAVL

class ArbolAVL:
    def __init__(self):
        """Inicializa el árbol AVL"""
        self.raiz = None
        self.tamaño = 0
        
    def insertar(self, clave, valor=None):
        """Inserta un elemento en el árbol AVL"""
        self.raiz = self._insertar_recursivo(self.raiz, clave, valor)
        self.tamaño += 1
        
    def _insertar_recursivo(self, nodo, clave, valor):
        """Inserción recursiva con balanceo"""
        # Caso base: insertar el nodo
        if nodo is None:
            return NodoAVL(clave, valor)
            
        # Inserción normal de BST
        if clave < nodo.clave:
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, clave, valor)
        elif clave > nodo.clave:
            nodo.derecho = self._insertar_recursivo(nodo.derecho, clave, valor)
        else:
            # Clave duplicada, actualizar valor
            nodo.valor = valor
            self.tamaño -= 1  # No incrementar tamaño
            return nodo
            
        # Actualizar altura
        nodo.actualizar_altura()
        
        # Obtener factor de balance
        balance = nodo.obtener_factor_balance()
        
        # Rotaciones para mantener balance
        # Caso Izquierda-Izquierda
        if balance > 1 and clave < nodo.izquierdo.clave:
            return self._rotacion_derecha(nodo)
            
        # Caso Derecha-Derecha
        if balance < -1 and clave > nodo.derecho.clave:
            return self._rotacion_izquierda(nodo)
            
        # Caso Izquierda-Derecha
        if balance > 1 and clave > nodo.izquierdo.clave:
            nodo.izquierdo = self._rotacion_izquierda(nodo.izquierdo)
            return self._rotacion_derecha(nodo)
            
        # Caso Derecha-Izquierda
        if balance < -1 and clave < nodo.derecho.clave:
            nodo.derecho = self._rotacion_derecha(nodo.derecho)
            return self._rotacion_izquierda(nodo)
            
        return nodo
        
    def eliminar(self, clave):
        """Elimina un elemento del árbol AVL"""
        if self.buscar(clave) is not None:
            self.raiz = self._eliminar_recursivo(self.raiz, clave)
            self.tamaño -= 1
            
    def _eliminar_recursivo(self, nodo, clave):
        """Eliminación recursiva con balanceo"""
        # Caso base
        if nodo is None:
            return nodo
            
        # Buscar el nodo a eliminar
        if clave < nodo.clave:
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, clave)
        elif clave > nodo.clave:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, clave)
        else:
            # Nodo encontrado
            if nodo.es_hoja():
                return None
            elif nodo.tiene_un_hijo():
                return nodo.obtener_hijo_unico()
            else:
                # Nodo con dos hijos
                sucesor = self._encontrar_minimo(nodo.derecho)
                nodo.clave = sucesor.clave
                nodo.valor = sucesor.valor
                nodo.derecho = self._eliminar_recursivo(nodo.derecho, sucesor.clave)
                
        # Actualizar altura
        nodo.actualizar_altura()
        
        # Rebalancear
        balance = nodo.obtener_factor_balance()
        
        # Rotaciones
        if balance > 1:
            if nodo.izquierdo.obtener_factor_balance() >= 0:
                return self._rotacion_derecha(nodo)
            else:
                nodo.izquierdo = self._rotacion_izquierda(nodo.izquierdo)
                return self._rotacion_derecha(nodo)
                
        if balance < -1:
            if nodo.derecho.obtener_factor_balance() <= 0:
                return self._rotacion_izquierda(nodo)
            else:
                nodo.derecho = self._rotacion_derecha(nodo.derecho)
                return self._rotacion_izquierda(nodo)
                
        return nodo
        
    def _rotacion_izquierda(self, z):
        """Rotación simple a la izquierda"""
        y = z.derecho
        T2 = y.izquierdo
        
        # Realizar rotación
        y.izquierdo = z
        z.derecho = T2
        
        # Actualizar alturas
        z.actualizar_altura()
        y.actualizar_altura()
        
        return y
        
    def _rotacion_derecha(self, z):
        """Rotación simple a la derecha"""
        y = z.izquierdo
        T3 = y.derecho
        
        # Realizar rotación
        y.derecho = z
        z.izquierdo = T3
        
        # Actualizar alturas
        z.actualizar_altura()
        y.actualizar_altura()
        
        return y
        
    def buscar(self, clave):
        """Busca un elemento en el árbol"""
        return self._buscar_recursivo(self.raiz, clave)
        
    def _buscar_recursivo(self, nodo, clave):
        """Búsqueda recursiva"""
        if nodo is None or nodo.clave == clave:
            return nodo
            
        if clave < nodo.clave:
            return self._buscar_recursivo(nodo.izquierdo, clave)
        return self._buscar_recursivo(nodo.derecho, clave)
        
    def _encontrar_minimo(self, nodo):
        """Encuentra el nodo con el valor mínimo"""
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo
        
    def _encontrar_maximo(self, nodo):
        """Encuentra el nodo con el valor máximo"""
        while nodo.derecho is not None:
            nodo = nodo.derecho
        return nodo
        
    def recorrido_inorden(self):
        """Recorrido inorden del árbol"""
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado
        
    def _inorden_recursivo(self, nodo, resultado):
        """Recorrido inorden recursivo"""
        if nodo is not None:
            self._inorden_recursivo(nodo.izquierdo, resultado)
            resultado.append((nodo.clave, nodo.valor))
            self._inorden_recursivo(nodo.derecho, resultado)
            
    def obtener_altura(self):
        """Obtiene la altura del árbol"""
        if self.raiz is None:
            return 0
        return self.raiz.altura
        
    def esta_vacio(self):
        """Verifica si el árbol está vacío"""
        return self.raiz is None
        
    def obtener_tamaño(self):
        """Obtiene el número de elementos en el árbol"""
        return self.tamaño
        
    def limpiar(self):
        """Limpia el árbol"""
        self.raiz = None
        self.tamaño = 0