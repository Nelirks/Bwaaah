# coding: utf-8
import os
import entities
import pygame
import menu
import engine
pygame.init()
pygame.key.set_repeat(50, 1)

# résolution du rendu :512*288
# résolution cible : 1024*576


def mainLoop(game):
    wall = engine.Carte(os.path.join("assets", "levels", "test"),
                        mode="load")  # objet carte
    back = wall.renderSurface()  # surface carte
    print(wall.playerPosition)
    px = wall.playerPosition[0] * wall.tileSize
    py = wall.playerPosition[1] * wall.tileSize
    print(px, py)
    p1 = entities.Player(
        px, py, "1")  # joueur

    events = []
    while game.state == 1 or game.state == 2:  # en jeu ou dans le menu pause
        p1.movement(wall.get_rects(), events)

        game.screen.blit(back, (0, 0))

        p1.render(game.screen)

        game.waitFramerate()

        events = game.runEvents()  # en fin de boucle pour éviter les conflicts
