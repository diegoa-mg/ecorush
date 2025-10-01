import pygame, os, math, sys
from settings import WIDTH, HEIGHT, FPS
import menu_principal
import menu_niveles
import sel_nivel1
import sel_nivel2
import sel_nivel3

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("EcoRush!")
    clock = pygame.time.Clock()

    # Arranca en el menú principal
    scene = "menu"

    while True:
        if scene == "menu":
            scene = menu_principal.run(screen, clock)

        elif scene == "niveles":
            scene = menu_niveles.run(screen, clock)

        elif scene == "sel_nivel1":
            scene = sel_nivel1.run(screen, clock)

        elif scene == "sel_nivel2":
            scene = sel_nivel2.run(screen, clock)

        elif scene == "sel_nivel3":
            scene = sel_nivel3.run(screen, clock)

        elif scene == "quit":
            pygame.quit()
            sys.exit()

        else:
            # Por si alguien devuelve algo inesperado
            scene = "menu"
        
if __name__ == "__main__":
    main()