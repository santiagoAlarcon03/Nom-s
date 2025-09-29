import pygame
import sys
from game.motor import Motor
from game.gui import GUI

def main():
    pygame.init()
    motor = Motor()
    gui = GUI()
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
            motor.manejar_eventos(event)
        
        motor.actualizar()
        gui.renderizar(motor)
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()