# Clase Nodo del AVL
class NodoAVL:
    def __init__(self, clave, valor=None):
        """Inicializa un nodo del árbol AVL"""
        self.clave = clave
        self.valor = valor
        self.altura = 1
        self.izquierdo = None
        self.derecho = None
        
    def obtener_factor_balance(self):
        """Calcula el factor de balance del nodo"""
        altura_izq = self.obtener_altura(self.izquierdo)
        altura_der = self.obtener_altura(self.derecho)
        return altura_izq - altura_der
        
    @staticmethod
    def obtener_altura(nodo):
        """Obtiene la altura de un nodo"""
        if nodo is None:
            return 0
        return nodo.altura
        
    def actualizar_altura(self):
        """Actualiza la altura del nodo"""
        altura_izq = self.obtener_altura(self.izquierdo)
        altura_der = self.obtener_altura(self.derecho)
        self.altura = 1 + max(altura_izq, altura_der)
        
    def es_hoja(self):
        """Verifica si el nodo es una hoja"""
        return self.izquierdo is None and self.derecho is None
        
    def tiene_un_hijo(self):
        """Verifica si el nodo tiene exactamente un hijo"""
        return (self.izquierdo is None) != (self.derecho is None)
        
    def obtener_hijo_unico(self):
        """Obtiene el único hijo del nodo (si existe)"""
        if self.izquierdo is not None:
            return self.izquierdo
        return self.derecho
        
    def __str__(self):
        """Representación en string del nodo"""
        return f"Nodo(clave={self.clave}, altura={self.altura})"
        
    def __repr__(self):
        """Representación del nodo para debugging"""
        return self.__str__()