import pygame
import sys
from game.motor import Motor
from game.gui import GUI

def main():
    """Función principal del juego"""
    pygame.init()
    
    # Crear instancias del motor y GUI
    motor = Motor()
    gui = GUI()
    
    # Bucle principal del juego
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and not motor.juego_activo:
                    motor.reiniciar_juego()
                elif event.key == pygame.K_ESCAPE:
                    running = False
            
            # Manejar eventos del juego
            motor.manejar_eventos(event)
        
        # Actualizar lógica del juego
        motor.actualizar()
        
        # Renderizar
        gui.renderizar(motor)
        
        clock.tick(60)  # 60 FPS
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()