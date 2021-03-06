# coding: utf-8
import pygame
from math import ceil
from math import floor
import os
import copy

CONST_TileItemSize = 16


class Item:
    """
    Classe Item permettant de base pour tout item de l'inventaire

    """
    nom = ""
    description = ""
    quantity = 0

    def __init__(self, nom, quantity, texturedir, description=""):
        """
        crée un objet Item pour être utilisé dans l'inventaire,
        il est préférable d'utiliser un objet enfant du type adapté (ex: potion, arme)
        """
        self.nom = nom
        self.description = description
        self.texture = pygame.image.load(texturedir).convert_alpha()
        self.quantity = quantity
        self.textures = []

        self.framequantity = self.texture.get_width() // 32
        for n in range (self.framequantity):
            self.textures.append(self.texture.subsurface(pygame.rect.Rect(n*32, 0, 32, 32)))
        self.frame = 0



    def render(self):
        """
        retourne une surface avec l'item
        """
        surface = pygame.Surface((32, 32))
        surface.blit(self.texture, (0, 0))
        return surface

    def use(self, user):
        return(self, "0")


class Consommable(Item):
    # Classe consommmable : Item avec des effets quand il est consommé
    def __init__(self, nom, quantity, texture, lifegain=0, hungergain=0, thirstgain=0, buff="", description=""):
        self.lifegain = lifegain
        self.hungergain = hungergain
        self.thirstgain = thirstgain
        self.buff = buff
        super().__init__(nom, quantity, texture, description)

    def use(self, user):
        user.life += self.lifegain
        user.hunger += self.hungergain
        user.thirst += self.thirstgain
        self.quantity -= 1
        if self.quantity <= 0:
            return("0", "0")
        else:
            return(self, "0")


class Wood(Item):
    def __init__(self, quantity):
        super().__init__("Wood", quantity, os.path.join("assets", "items", "Wood.png"))


class Apple(Consommable):
    def __init__(self, quantity):
        super().__init__("Apple", quantity, os.path.join(
            "assets", "items", "Apple.png"), 10, 25, 10)


class Pompot(Consommable):
    def __init__(self,  quantity):
        super().__init__("Pompot", quantity, os.path.join("assets", "items",
                                                          "Pompot.png"), lifegain=30, hungergain=40, thirstgain=30)

class Coconut(Item):
    def __init__(self, quantity):
        super().__init__("Coconut", quantity, os.path.join("assets", "items", "Coconut.png"))

class HalfCoconut(Consommable):
    def __init__(self,  quantity):
        super().__init__("HalfCoconut", quantity, os.path.join("assets", "items",
                                                          "HalfCoconut.png"), lifegain=5, hungergain=5, thirstgain=40)

itemsList = {"Apple": Apple,
             "Wood": Wood,
             "Pompot": Pompot,
             "Coconut": Coconut,
             "HalfCoconut" : HalfCoconut}


class Weapon(Item):
    """
    Classe arme : un item avec une caratéristique de dégats
    """

    damage = 0
    portee = 1

    def __init__(self, nom, texture, damage=0, portee=1, description=''):
        self.damage = damage
        self.portee = portee
        super().__init__(nom, texture, description)

    def applyDamage(self, entity):
        """
        applique les dégats à un entitée
        """
        entity.takeDamage(self.damage)


class Tool(Item):
    def __init__(self, nom, quantity,  texture, description):
        super().__init__(nom, quantity, texture, description)

    def use(self, user):
        #playerpos = (user.rect.centerx + user.facing[0]*15, user.rect.centery + user.facing[1]*18)
        return(self, "usetool")


class PlasmaPickaxaxe(Tool):
    def __init__(self, quantity):
        super().__init__("Axe", quantity, os.path.join("assets", "items", "PlasmaPickaxaxeAnimated.png"), "")


class ItemContainer:

    def __init__(self, size):  # Création de deux listes liste ayant une longueur size
        self.items = []
        for n in range(size):
            self.items.append("0")
        self.basicfont = pygame.font.SysFont("Source Code Pro", 12)

    # Augmentation de la longueur des listes en cas d'augmentation de l'inventaire
    def sizeincrease(self, sizeup):
        for n in range(sizeup):
            self.items.append("0")

# Fonction permettant : l'ajout d'un item en donnant l'item et sa position, ou l'ajout d'un item dans la première case libre en donnant -1 comme position.
# Permet également de retirer des objets de l'inventaire en rajoutant un objet "0", avec 3 modes : all, half et one
    def additem(self, itemadded, place, mode="all"):
        itemalreadyadded = 0
        itemplace = 0  # besoin de fix le placement auto quand l'inventaire est plein
        if itemadded == "0":
            if mode == "all":
                olditem = self.items[place]
                self.items[place] = "0"

            if mode == "half":
                olditem = copy.copy(self.items[place])
                olditem.quantity = ceil(olditem.quantity/2)
                self.items[place].quantity -= olditem.quantity
                if self.items[place].quantity == 0:
                    self.items[place] = "0"

            if mode == "one":
                olditem = copy.copy(self.items[place])
                olditem.quantity = 1
                self.items[place].quantity -= 1
                if self.items[place].quantity == 0:
                    self.items[place] = "0"

        else:
            if place == -1:
                for n in range(len(self.items)):
                    if self.items[len(self.items)-n-1] != "0":
                        if self.items[len(self.items)-n-1].nom == itemadded.nom and self.items[len(self.items)-n-1].quantity + itemadded.quantity <= 99:
                            self.items[len(self.items)-n -
                                       1].quantity += itemadded.quantity
                            olditem = "0"
                            itemalreadyadded = 1
                            if self.items[len(self.items)-n - 1].quantity < 0:
                                item = self.items[len(self.items)-n - 1]
                                self.items[len(self.items)-n - 1] = "0"
                                self.additem(item, -1)
                            elif self.items[len(self.items)-n - 1].quantity == 0:
                                self.items[len(self.items)-n - 1] = "0"
                            break
                    else:
                        itemplace = len(self.items)-n-1
                if itemalreadyadded == 0:
                    self.items[itemplace] = itemadded
                    olditem = "0"

            elif self.items[place] != "0":
                if self.items[place].nom == itemadded.nom:
                    self.items[place].quantity += itemadded.quantity
                    olditem = "0"
                else:
                    olditem = self.items[place]
                    self.items[place] = itemadded
            else:
                self.items[place] = itemadded
                olditem = "0"
        if self.items[place] != "0":
            if self.items[place].quantity > 99:
                olditem = copy.copy(self.items[place])
                olditem.quantity -= 99
                self.items[place].quantity = 99
        return(olditem)

    def getFreePlace(self):
        compteur = 0
        for i in self.items:
            if i == "0":
                compteur += 1
        return compteur

    def haveItem(self, name, quantity):
        q = 0
        for i in self.items:
            if i != "0":
                if i.nom == name:
                    q += i.quantity
        return q >= quantity

    # Crée une surface avec tous les items dans un rectangle de largeur donnée en pixel

    def render(self, largeur):

        itemperline = (largeur)//34
        itempercolumn = ceil(len(self.items)/itemperline)
        surfacefinale = pygame.Surface(
            (itemperline*34, itempercolumn*34), pygame.SRCALPHA, 32).convert_alpha()
        for n in range(len(self.items)):
            x = n % itemperline
            y = n//itemperline
            if self.items[n] != "0":
                itemquantity = self.basicfont.render(
                    str(self.items[n].quantity), False, (255, 255, 255))
                surfacefinale.blit(self.items[n].textures[floor(self.items[n].frame)], (x*34+1, y*34+1))
                self.items[n].frame += 0.2
                if floor(self.items[n].frame) == self.items[n].framequantity :
                    self.items[n].frame = 0
                surfacefinale.blit(itemquantity, (x*34+18, y*34+21))
        return surfacefinale
