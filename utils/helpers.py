# Funciones auxiliares
import random
import math
import pygame
from typing import Tuple, List, Optional

def calcular_distancia(punto1: Tuple[float, float], punto2: Tuple[float, float]) -> float:
    """Calcula la distancia euclidiana entre dos puntos"""
    x1, y1 = punto1
    x2, y2 = punto2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def punto_en_rectangulo(punto: Tuple[float, float], rect: pygame.Rect) -> bool:
    """Verifica si un punto está dentro de un rectángulo"""
    x, y = punto
    return rect.x <= x <= rect.x + rect.width and rect.y <= y <= rect.y + rect.height

def generar_color_aleatorio() -> Tuple[int, int, int]:
    """Genera un color RGB aleatorio"""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def interpolar_color(color1: Tuple[int, int, int], color2: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
    """Interpola entre dos colores RGB"""
    factor = max(0.0, min(1.0, factor))  # Clamp entre 0 y 1
    r = int(color1[0] + (color2[0] - color1[0]) * factor)
    g = int(color1[1] + (color2[1] - color1[1]) * factor)
    b = int(color1[2] + (color2[2] - color1[2]) * factor)
    return (r, g, b)

def normalizar_velocidad(velocidad: float, min_vel: float = 1.0, max_vel: float = 10.0) -> float:
    """Normaliza una velocidad dentro de un rango específico"""
    return max(min_vel, min(max_vel, velocidad))

def calcular_fps_promedio(fps_list: List[float], max_samples: int = 60) -> float:
    """Calcula el FPS promedio de las últimas muestras"""
    if not fps_list:
        return 0.0
    
    # Mantener solo las últimas muestras
    if len(fps_list) > max_samples:
        fps_list = fps_list[-max_samples:]
    
    return sum(fps_list) / len(fps_list)

def generar_posicion_carril(carril: int, num_carriles: int, ancho_pantalla: int, ancho_objeto: int = 40) -> int:
    """Genera la posición X centrada para un carril específico"""
    if num_carriles <= 0:
        return ancho_pantalla // 2 - ancho_objeto // 2
    
    ancho_carril = ancho_pantalla // num_carriles
    posicion_centro = carril * ancho_carril + ancho_carril // 2
    return posicion_centro - ancho_objeto // 2

def esta_fuera_de_pantalla(x: float, y: float, ancho: float, alto: float, 
                          ancho_pantalla: int, alto_pantalla: int, margen: int = 50) -> bool:
    """Verifica si un objeto está completamente fuera de la pantalla"""
    return (x + ancho < -margen or x > ancho_pantalla + margen or
            y + alto < -margen or y > alto_pantalla + margen)

def limitar_a_pantalla(x: float, y: float, ancho: float, alto: float,
                      ancho_pantalla: int, alto_pantalla: int) -> Tuple[float, float]:
    """Limita las coordenadas de un objeto para que permanezca en pantalla"""
    x = max(0, min(x, ancho_pantalla - ancho))
    y = max(0, min(y, alto_pantalla - alto))
    return x, y

def formatear_tiempo(segundos: float) -> str:
    """Formatea tiempo en segundos a formato MM:SS"""
    minutos = int(segundos // 60)
    segundos_restantes = int(segundos % 60)
    return f"{minutos:02d}:{segundos_restantes:02d}"

def formatear_puntuacion(puntuacion: int) -> str:
    """Formatea la puntuación con separadores de miles"""
    return f"{puntuacion:,}".replace(",", ".")

def generar_distribucion_normal(media: float, desviacion: float, min_val: float = None, max_val: float = None) -> float:
    """Genera un valor con distribución normal"""
    valor = random.normalvariate(media, desviacion)
    
    if min_val is not None:
        valor = max(min_val, valor)
    if max_val is not None:
        valor = min(max_val, valor)
        
    return valor

def probabilidad_evento(probabilidad: float) -> bool:
    """Determina si un evento ocurre basado en una probabilidad (0.0 a 1.0)"""
    return random.random() < probabilidad

def seleccionar_aleatorio_ponderado(opciones: List[Tuple[any, float]]) -> any:
    """Selecciona un elemento aleatorio basado en pesos"""
    if not opciones:
        return None
    
    total_peso = sum(peso for _, peso in opciones)
    if total_peso <= 0:
        return random.choice([opcion for opcion, _ in opciones])
    
    punto_aleatorio = random.uniform(0, total_peso)
    peso_acumulado = 0
    
    for opcion, peso in opciones:
        peso_acumulado += peso
        if punto_aleatorio <= peso_acumulado:
            return opcion
    
    # Fallback
    return opciones[-1][0]

def crear_gradiente_vertical(superficie: pygame.Surface, color_superior: Tuple[int, int, int], 
                           color_inferior: Tuple[int, int, int]) -> None:
    """Crea un gradiente vertical en una superficie de pygame"""
    ancho, alto = superficie.get_size()
    
    for y in range(alto):
        factor = y / alto
        color_actual = interpolar_color(color_superior, color_inferior, factor)
        pygame.draw.line(superficie, color_actual, (0, y), (ancho, y))

def rotar_punto(punto: Tuple[float, float], centro: Tuple[float, float], angulo: float) -> Tuple[float, float]:
    """Rota un punto alrededor de un centro por un ángulo dado (en radianes)"""
    x, y = punto
    cx, cy = centro
    
    cos_a = math.cos(angulo)
    sin_a = math.sin(angulo)
    
    # Trasladar al origen
    x -= cx
    y -= cy
    
    # Rotar
    x_rotado = x * cos_a - y * sin_a
    y_rotado = x * sin_a + y * cos_a
    
    # Trasladar de vuelta
    x_rotado += cx
    y_rotado += cy
    
    return (x_rotado, y_rotado)

def escalar_dificultad(tiempo_juego: float, factor_base: float = 1.0, 
                      incremento_por_minuto: float = 0.1) -> float:
    """Calcula el factor de dificultad basado en el tiempo de juego"""
    minutos_jugados = tiempo_juego / 60.0
    return factor_base + (minutos_jugados * incremento_por_minuto)

def obtener_carril_aleatorio(num_carriles: int, carril_excluir: Optional[int] = None) -> int:
    """Obtiene un carril aleatorio, opcionalmente excluyendo uno específico"""
    carriles_disponibles = list(range(num_carriles))
    
    if carril_excluir is not None and carril_excluir in carriles_disponibles:
        carriles_disponibles.remove(carril_excluir)
    
    return random.choice(carriles_disponibles) if carriles_disponibles else 0

def suavizar_movimiento(posicion_actual: float, posicion_objetivo: float, factor_suavizado: float = 0.1) -> float:
    """Suaviza el movimiento entre dos posiciones"""
    factor_suavizado = max(0.0, min(1.0, factor_suavizado))
    return posicion_actual + (posicion_objetivo - posicion_actual) * factor_suavizado

def generar_secuencia_fibonacci(n: int) -> List[int]:
    """Genera los primeros n números de la secuencia de Fibonacci"""
    if n <= 0:
        return []
    elif n == 1:
        return [1]
    elif n == 2:
        return [1, 1]
    
    secuencia = [1, 1]
    for i in range(2, n):
        secuencia.append(secuencia[i-1] + secuencia[i-2])
    
    return secuencia

def debug_print(mensaje: str, nivel: str = "INFO", mostrar_tiempo: bool = True) -> None:
    """Función de debug para imprimir mensajes con formato"""
    import datetime
    
    if mostrar_tiempo:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{nivel}] {mensaje}")
    else:
        print(f"[{nivel}] {mensaje}")