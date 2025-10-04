import pygame, os, math, sys
from settings import WIDTH, HEIGHT, FPS, with_fade, fade_to_black
import menu_principal
import menu_niveles
import sel_nivel1
import sel_nivel2
import sel_nivel3
import nivel1
# import nivel1_extremo
# import nivel2_sencillo
# import nivel2_extremo
# import nivel3_sencillo
# import nivel3_extremo

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("EcoRush!")
    clock = pygame.time.Clock()

    SCENES = {
        "menu":        menu_principal.run,
        "niveles":     menu_niveles.run,
        "sel_nivel1":  with_fade(sel_nivel1.run,     in_ms=100),
        "sel_nivel2":  with_fade(sel_nivel2.run,     in_ms=100),
        "sel_nivel3":  with_fade(sel_nivel3.run,     in_ms=100),
        "nivel1":      with_fade(nivel1.run,         in_ms=100),
    }

    # Arranca en el menú principal
    scene = "menu"

    while True:
        # Ejecuta la escena actual (viene con fade-in integrado)
        next_scene = SCENES[scene](screen, clock)

        if next_scene == "quit":
            pygame.quit()
            sys.exit()

        # Si la escena cambia, aplicamos fade-out antes de entrar a la nueva
        if next_scene != scene:
            fade_to_black(screen, duration_ms=25)
            scene = next_scene
        else:
            # Por si la escena decide quedarse (no cambia), evita bucles raros
            scene = scene
        
if __name__ == "__main__":
    main()