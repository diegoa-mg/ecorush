import pygame 

successes, failures = pygame.init() 
print("{0} successes and {1} failures".format(successes, failures))   

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("EcoRush!")
clock = pygame.time.Clock() 
FPS = 60  # Frames per second. &

# BLACK = (0, 0, 0) 
WHITE = (255, 255, 255) 
# RED = (255, 0, 0), GREEN = (0, 255, 0), BLUE = (0, 0, 255).  

# Cargar fondos y botones
background = pygame.image.load("C:/Users/ddieg/Documents/ECORUSH/ecorush/assets/imglimpia_definitiva.png")
titulo = pygame.image.load("C:/Users/ddieg/Documents/ECORUSH/ecorush/assets/titulo.png")
botoninicio = pygame.image.load("C:/Users/ddieg/Documents/ECORUSH/ecorush/assets/botoninicio.png")
botonconfig = pygame.image.load("C:/Users/ddieg/Documents/ECORUSH/ecorush/assets/botonconfig.png")
botontuto = pygame.image.load("C:/Users/ddieg/Documents/ECORUSH/ecorush/assets/botontuto.png")

# Escalar
background = pygame.transform.scale(background, (1280, 720))  # Ajustar al tamaño de ventanas
titulo = pygame.transform.scale(titulo, (1118, 178))
# botoninicio = pygame.transform.scale(titulo, ())
botonconfig = pygame.transform.scale(botonconfig, (334.66, 85.33))
botontuto = pygame.transform.scale(botontuto, (334.66, 85.33))

running = True
while True:     
    clock.tick(FPS)      
    for event in pygame.event.get():         
        if event.type == pygame.QUIT:             
            running = False              
    
    screen.blit(background, (0, 0))             
    screen.blit(titulo, (81, 65)) 
    # screen.blit(botoninicio, ())
    screen.blit(botonconfig, (157.7, 500))
    screen.blit(botontuto, (792.7, 500))

    pygame.display.flip()
    