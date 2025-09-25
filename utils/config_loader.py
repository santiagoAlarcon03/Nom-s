# Manejo de JSON
import json
import os

class ConfigLoader:
    def __init__(self, archivo_config="config.json"):
        """Inicializa el cargador de configuración"""
        self.archivo_config = archivo_config
        self.config_por_defecto = {
            "juego": {
                "ancho_pantalla": 600,
                "alto_pantalla": 800,
                "fps": 60,
                "velocidad_inicial": 3,
                "incremento_velocidad": 0.001
            },
            "carrito": {
                "velocidad": 5,
                "ancho": 40,
                "alto": 60,
                "color": [255, 0, 0]
            },
            "obstaculos": {
                "ancho": 35,
                "alto": 50,
                "velocidad_inicial": 3,
                "intervalo_generacion": 2000,
                "probabilidad_especial": 0.25,
                "colores": {
                    "normal": [0, 0, 255],
                    "especial": [255, 255, 0],
                    "bonus": [0, 255, 0]
                }
            },
            "carretera": {
                "numero_carriles": 3,
                "velocidad_lineas": 3,
                "espaciado_lineas": 40,
                "color_fondo": [50, 50, 50],
                "color_lineas": [255, 255, 255]
            },
            "puntuacion": {
                "puntos_por_obstaculo_evitado": 1,
                "puntos_por_especial": 10,
                "puntos_por_bonus": 25
            },
            "controles": {
                "tecla_izquierda": ["LEFT", "a"],
                "tecla_derecha": ["RIGHT", "d"],
                "tecla_pausa": ["SPACE"],
                "tecla_reiniciar": ["r"],
                "tecla_salir": ["ESCAPE"]
            },
            "audio": {
                "volumen_musica": 0.7,
                "volumen_efectos": 0.8,
                "archivos": {
                    "musica_fondo": "assets/music/background.mp3",
                    "sonido_colision": "assets/sounds/crash.wav",
                    "sonido_especial": "assets/sounds/pickup.wav"
                }
            },
            "avl": {
                "mostrar_visualizacion": False,
                "ancho_visualizador": 800,
                "alto_visualizador": 600,
                "guardar_estadisticas": True
            }
        }
        
    def cargar_configuracion(self):
        """Carga la configuración desde el archivo JSON"""
        try:
            if os.path.exists(self.archivo_config):
                with open(self.archivo_config, 'r', encoding='utf-8') as archivo:
                    config_cargada = json.load(archivo)
                    # Fusionar con configuración por defecto
                    return self._fusionar_configs(self.config_por_defecto, config_cargada)
            else:
                # Crear archivo de configuración por defecto
                self.guardar_configuracion(self.config_por_defecto)
                return self.config_por_defecto.copy()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error al cargar configuración: {e}")
            print("Usando configuración por defecto")
            return self.config_por_defecto.copy()
            
    def guardar_configuracion(self, config):
        """Guarda la configuración en el archivo JSON"""
        try:
            with open(self.archivo_config, 'w', encoding='utf-8') as archivo:
                json.dump(config, archivo, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error al guardar configuración: {e}")
            return False
            
    def _fusionar_configs(self, config_base, config_nueva):
        """Fusiona recursivamente dos diccionarios de configuración"""
        resultado = config_base.copy()
        
        for clave, valor in config_nueva.items():
            if (clave in resultado and 
                isinstance(resultado[clave], dict) and 
                isinstance(valor, dict)):
                resultado[clave] = self._fusionar_configs(resultado[clave], valor)
            else:
                resultado[clave] = valor
                
        return resultado
        
    def obtener_valor(self, config, ruta, valor_defecto=None):
        """Obtiene un valor de la configuración usando una ruta de puntos"""
        try:
            claves = ruta.split('.')
            actual = config
            
            for clave in claves:
                actual = actual[clave]
                
            return actual
        except (KeyError, TypeError):
            return valor_defecto
            
    def establecer_valor(self, config, ruta, valor):
        """Establece un valor en la configuración usando una ruta de puntos"""
        try:
            claves = ruta.split('.')
            actual = config
            
            # Navegar hasta el penúltimo nivel
            for clave in claves[:-1]:
                if clave not in actual:
                    actual[clave] = {}
                actual = actual[clave]
                
            # Establecer el valor final
            actual[claves[-1]] = valor
            return True
        except (KeyError, TypeError):
            return False
            
    def validar_configuracion(self, config):
        """Valida que la configuración tenga los valores correctos"""
        errores = []
        
        # Validar dimensiones de pantalla
        ancho = self.obtener_valor(config, 'juego.ancho_pantalla')
        alto = self.obtener_valor(config, 'juego.alto_pantalla')
        
        if not isinstance(ancho, int) or ancho < 400:
            errores.append("ancho_pantalla debe ser un entero >= 400")
        if not isinstance(alto, int) or alto < 300:
            errores.append("alto_pantalla debe ser un entero >= 300")
            
        # Validar FPS
        fps = self.obtener_valor(config, 'juego.fps')
        if not isinstance(fps, int) or fps < 30 or fps > 120:
            errores.append("fps debe ser un entero entre 30 y 120")
            
        # Validar colores
        for tipo_color in ['carrito.color', 'obstaculos.colores.normal', 
                          'obstaculos.colores.especial']:
            color = self.obtener_valor(config, tipo_color)
            if not self._validar_color(color):
                errores.append(f"{tipo_color} debe ser una lista de 3 enteros [R,G,B] entre 0-255")
                
        return errores
        
    def _validar_color(self, color):
        """Valida que un color sea una lista RGB válida"""
        if not isinstance(color, list) or len(color) != 3:
            return False
        return all(isinstance(c, int) and 0 <= c <= 255 for c in color)
        
    def crear_perfil_personalizado(self, nombre_perfil, modificaciones):
        """Crea un perfil de configuración personalizado"""
        archivo_perfil = f"config_{nombre_perfil}.json"
        config_base = self.cargar_configuracion()
        
        # Aplicar modificaciones
        config_personalizada = self._fusionar_configs(config_base, modificaciones)
        
        # Validar
        errores = self.validar_configuracion(config_personalizada)
        if errores:
            return False, errores
            
        # Guardar perfil
        loader_perfil = ConfigLoader(archivo_perfil)
        if loader_perfil.guardar_configuracion(config_personalizada):
            return True, f"Perfil '{nombre_perfil}' creado exitosamente"
        else:
            return False, ["Error al guardar el perfil"]
            
    def listar_perfiles(self):
        """Lista todos los perfiles de configuración disponibles"""
        perfiles = []
        for archivo in os.listdir('.'):
            if archivo.startswith('config_') and archivo.endswith('.json'):
                nombre_perfil = archivo[7:-5]  # Remover 'config_' y '.json'
                perfiles.append(nombre_perfil)
        return perfiles