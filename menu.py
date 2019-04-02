import pygame
import main
import os
import random
import math
import engine


class Star:

    def __init__(self, position, size, speed=(-10, 0)):
        self.speed = speed
        self.x = position[0]
        self.y = position[1]
        self.surface = pygame.surface.Surface((size*2, size))
        self.surface.fill((255, 255, 255))

    def render(self, surface):
        surface.blit(self.surface, (self.x, self.y))

    def update(self):

        self.x += self.speed[0]
        self.y += self.speed[1]


class Stars:
    """
    une nuée d'étoiles défilant
    """

    liste = []
    line = 5
    frame = 0

    def render(self, surface):
        if self.frame % 8 == 0:
            width = surface.get_width()
            height = surface.get_height()
            for i in range(self.line):
                x = width + random.randint(-10, 10)
                y = random.randint(10, height-10)
                self.liste.append(Star((x, y), random.randint(1, 5)))
        i = 0
        for s in self.liste:
            s.render(surface)
            s.update()
            if s.x < 0:
                self.liste.pop(i)
            else:
                i += 1
        self.frame += 1


game = engine.Engine((1280, 720),
                     (1280, 720), framerate=100)  # fenêtre 1:1 pour les boutons
game.state = 0

playerKeyConfig = {
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "down": pygame.K_DOWN,
    "up": pygame.K_UP
}
playerKeyConfigUnicode = {
    "left": "d",
    "right": "a",
    "down": "s",
    "up": "z"
}

playEvent = pygame.USEREVENT + 4
creditsEvent = pygame.USEREVENT + 3
settingsEvent = pygame.USEREVENT + 2


playButton = engine.Button(
    (10, 10), (130, 50),  "Jouer", playEvent, fontSize=60, focusedBackground=(100, 100, 100))
creditsButton = engine.Button(
    (10, 70), (110, 40),  "Crédits", creditsEvent, fontSize=40, focusedBackground=(100, 100, 100))
fullScreenButton = engine.Button((10, 120), (170, 40), "Plein Écran",
                                 game.fullscreenEvent, fontSize=40, focusedBackground=(100, 100, 100))
settingsButton = engine.Button((10, 170), (170, 40), "Paramètres",
                               settingsEvent, fontSize=40, focusedBackground=(100, 100, 100))
closeButton = engine.Button(
    (10, 220), (240, 40),  "Retour au bureau", pygame.QUIT, fontSize=40, focusedBackground=(100, 100, 100))


def mainMenu():
    global game
    game.state = 0
    spaceShip = pygame.image.load(os.path.join("assets", "spaceship2.png"))
    spaceShip = pygame.transform.scale2x(spaceShip)
    game.changeMode((1280, 720), (1280, 720))
    events = []
    stars = Stars()
    pygame.mixer_music.load(os.path.join("assets", "music", "main_Menu.mp3"))
    pygame.mixer_music.play(-1)
    frame = 0
    while game.state == 0:
        playButton.update(events)
        creditsButton.update(events)
        settingsButton.update(events)
        fullScreenButton.update(events)
        closeButton.update(events)
        game.screen.fill((0, 0, 0))
        stars.render(game.screen)
        frame += 1  # frame +1 pour le vaisseau
        # affichage du vaisseau
        game.screen.blit(spaceShip, (300, 260 + math.sin(frame/80)*20))
        # affichage des boutons
        game.screen.blit(playButton.render(), playButton.position)
        game.screen.blit(creditsButton.render(), creditsButton.position)
        game.screen.blit(fullScreenButton.render(), fullScreenButton.position)
        game.screen.blit(settingsButton.render(), settingsButton.position)
        game.screen.blit(closeButton.render(), closeButton.position)
        # gestion des événements
        for event in events:
            if event.type == creditsEvent:
                game.state = 3
                credits()
                game.changeMode((1280, 720), (1280, 720))
                game.state = 0
            if event.type == settingsEvent:
                game.state = 3
                settings()
                game.state = 0

            if event.type == playEvent:
                # lancement du jeu
                pygame.mixer_music.fadeout(1000)
                game.state = 1
                # fenêtre pour le jeu
                game.changeMode((512, 288), (1280, 720))
                main.mainLoop(game, playerKeyConfig)
                game.changeMode((1280, 720), (1280, 720))
                pygame.mixer_music.load(os.path.join(
                    "assets", "music", "main_Menu.mp3"))
                pygame.mixer_music.play(-1)
                game.state = 0

        game.waitFramerate()
        events = game.runEvents()


def settings():
    global game

    font40 = pygame.font.Font(None, 40)
    game.screen.fill((0, 0, 0))
    font30 = pygame.font.Font(None, 30)
    setting = 1
    editUpEvent = pygame.USEREVENT + 5
    editLeftEvent = pygame.USEREVENT + 6
    editRightEvent = pygame.USEREVENT + 0
    editDownEvent = pygame.USEREVENT + 7
    editUpButton = engine.Button(
        (490, 40), (70, 50), playerKeyConfigUnicode["up"], editUpEvent, fontSize=50, background=(100, 100, 100))
    editDownButton = engine.Button(
        (490, 100), (70, 50), playerKeyConfigUnicode["down"], editDownEvent, fontSize=50, background=(100, 100, 100))
    editLeftButton = engine.Button(
        (490, 160), (70, 50), playerKeyConfigUnicode["left"], editLeftEvent, fontSize=50, background=(100, 100, 100))
    editRightButton = engine.Button(
        (490, 220), (70, 50), playerKeyConfigUnicode["right"], editRightEvent, fontSize=50, background=(100, 100, 100))
    editUp = 0
    editDown = 0
    editLeft = 0
    editRight = 0
    while setting == 1:
        events = game.runEvents()
        game.screen.fill((0, 0, 0))  # effacer l'écran
        game.screen.blit(font40.render(
            "Touches :", 1, (255, 255, 255)), (480, 10))
        game.screen.blit(font30.render(
            "Haut :", 1, (255, 255, 255)), (400, 50))
        game.screen.blit(font30.render(
            "Bas :", 1, (255, 255, 255)), (400, 110))
        game.screen.blit(font30.render(
            "Gauche :", 1, (255, 255, 255)), (400, 170))
        game.screen.blit(font30.render(
            "Droite :", 1, (255, 255, 255)), (400, 230))
        game.screen.blit(font30.render(
            "Echap pour retour arrière", 1, (255, 255, 255)), (0, 690))

        game.screen.blit(editUpButton.render(), editUpButton.position)
        game.screen.blit(editLeftButton.render(), editLeftButton.position)
        game.screen.blit(editRightButton.render(), editRightButton.position)

        game.screen.blit(editDownButton.render(), editDownButton.position)
        editLeftButton.update(events)
        editDownButton.update(events)
        editRightButton.update(events)
        editUpButton.update(events)
        for event in events:
            if event.type == editDownEvent:
                editDown = 1
                editDownButton.text = "..."
            if event.type == editUpEvent:
                editUp = 1
                editUpButton.text = "..."
            if event.type == editLeftEvent:
                editLeft = 1
                editLeftButton.text = "..."
            if event.type == editRightEvent:
                editRight = 1
                editRightButton.text = "..."

            if event.type == pygame.KEYDOWN:
                if event.key != pygame.K_ESCAPE:
                    if editLeft:
                        editLeft = 0
                        playerKeyConfig["left"] = event.key
                        playerKeyConfigUnicode["left"] = event.unicode
                        editLeftButton.text = event.unicode
                    if editRight:
                        editRight = 0
                        playerKeyConfig["right"] = event.key
                        playerKeyConfigUnicode["right"] = event.unicode
                        editRightButton.text = event.unicode
                    if editUp:
                        editUp = 0
                        playerKeyConfig["up"] = event.key
                        playerKeyConfigUnicode["up"] = event.unicode
                        editUpButton.text = event.unicode
                    if editDown:
                        editDown = 0
                        playerKeyConfig["down"] = event.key
                        playerKeyConfigUnicode["down"] = event.unicode
                        editDownButton.text = event.unicode

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    events = []
                    setting = 0
        events = []
        game.waitFramerate()


def credits():
    global game
    game.screen.fill((162, 155, 254))
    font40 = pygame.font.Font(None, 40)
    credit = 1
    game.screen.blit(font40.render("Developpeurs :",
                                   1, (255, 255, 255)), (480, 10))
    game.screen.blit(font40.render(
        "Nils PONSARD", 1, (255, 255, 255)), (510, 40))
    game.screen.blit(font40.render("Raphaël LESBROS",
                                   1, (255, 255, 255)), (510, 70))
    game.screen.blit(font40.render("Design Visuel :",
                                   1, (255, 255, 255)), (480, 120))
    game.screen.blit(font40.render("Raphaël LESBROS",
                                   1, (255, 255, 255)), (510, 150))
    game.screen.blit(font40.render("Nils PONSARD",
                                   1, (255, 255, 255)), (510, 180))
    game.screen.blit(font40.render("Léo MOUGIN",
                                   1, (255, 255, 255)), (510, 210))

    while credit == 1:
        events = game.runEvents()
        for event in events:
            if event.type == pygame.KEYUP:
                credit = 0
        events = []
        game.waitFramerate()
