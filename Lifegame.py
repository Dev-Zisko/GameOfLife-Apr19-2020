import pygame
import numpy as np
import time

pygame.init()

# Ancho y alto de la pantalla del juego
width, height = 600, 600

# Creacion de la pantalla del juego
screen = pygame.display.set_mode((height, width))

# Color del fondo = Casi negro, casi oscuro
bg = 25, 25, 25

# Pinta el fondo con el color elegido
screen.fill(bg)

# Numero de celdas
nxC, nyC = 25, 25

# Dimensiones de la celda
dimCW = width / nxC
dimCH = height / nyC

# Estado de las celdas. Vivas = 1. Muertas = 0
gameState = np.zeros((nxC, nyC))

# Automata palo
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

# Automata movil
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

# Control de la ejecucion del juego
pauseExect = False

# Bucle de ejecucion del juego
while(True):

    #Copia del estado antiguo
    newGameState = np.copy(gameState)

    # Limpiando la pantalla
    screen.fill(bg)

    # Registrando eventos de teclado y mouse
    ev = pygame.event.get()

    for event in ev:
        # Detectamos si se presiona una tecla
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        # Detectamos si se hace click
        mouseClick = pygame.mouse.get_pressed()
        
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]
    
    # Cerrar juego
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()

    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExect:

                # Calculamos el numero de vecinos cercanos
                n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                        gameState[(x)     % nxC, (y-1) % nyC] + \
                        gameState[(x+1)   % nxC, (y-1) % nyC] + \
                        gameState[(x-1)   % nxC, (y)   % nyC] + \
                        gameState[(x+1)   % nxC, (y)   % nyC] + \
                        gameState[(x-1)   % nxC, (y+1) % nyC] + \
                        gameState[(x)     % nxC, (y+1) % nyC] + \
                        gameState[(x+1)   % nxC, (y+1) % nyC]   

                # Regla N°1: Una celula muerta con exactamente 3 vecinas vivas, "revive"
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1
                
                # Regla N°2: Una celula viva con menos de 2 o mas de 3 vecinas vivas, "muere"
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0 

            # Creamos el polígono de cada celda a dibujar
            poly = [((x)   * dimCW, y     * dimCH),
                    ((x+1) * dimCW, y     * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x)   * dimCW, (y+1) * dimCH)]

            # Dibujamos la celda para cada par de x e y
            if newGameState[x, y] == 0: 
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Actualizamos el estado del juego
    gameState = np.copy(newGameState)

    # Actualiza la pantalla
    pygame.display.flip()