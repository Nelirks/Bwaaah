# coding: utf-8
import pygame
from math import ceil
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

    def render(self):
        """
        retourne une surface avec l'item
        """
        surface = pygame.Surface(CONST_TileItemSize, CONST_TileItemSize)
        surface.blit(self.texture, (0, 0))
        return surface

class Consommable(Item) :
    #Classe consommmable : Item avec des effets quand il est consommé
    def __init__(self, nom, quantity, texture, lifegain = 0, hungergain = 0, thirstgain = 0, buff = "", description = "") :
        self.lifegain = lifegain
        self.hungergain = hungergain
        self.thirstgain = thirstgain
        self.buff = buff
        super().__init__(nom, quantity, texture, description)

class Apple(Consommable):
    def __init__(self, quantity):
        super().__init__("Pomme", quantity, os.path.join("assets", "items", "Apple.png"), 10, 25, 10)

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


'''
class MagicWeapon(Weapon):
    """
    arme magiqe : applique des dégats magiques d'un certain type
    pour une arme totalement magique, mettre damage = 0
    """
    mDamageType = "fire"
    magicDamage = 0

    def __init__(self, nom, texture, damage=0, magicDamage=0, mDamageType="fire", description=''):
        self.mDamageType = mDamageType
        self.magicDamage = magicDamage
        super().__init__(nom, texture, damage=damage, description=description)

    def applyDamage(self, entity):
        entity.takeMagicDamage(self.magicDamage, self.mDamageType)
        super().applyDamage(entity)
'''
class ItemContainer :
    
    def __init__(self, size) : #Création de deux listes liste ayant une longueur size
        self.items = []
        for n in range(size) :
            self.items.append("0")

    def sizeincrease(self ,sizeup): #Augmentation de la longueur des listes en cas d'augmentation de l'inventaire
        for n in range (sizeup):
            self.items.append("0")

#Fonction permettant : l'ajout d'un item en donnant l'item et sa position, ou l'ajout d'un item dans la première case libre en donnant -1 comme position.
#Permet également de retirer des objets de l'inventaire en rajoutant un objet "0", avec 3 modes : all, half et one
    def additem(self, itemadded, place, mode = "all"):
        if itemadded == "0" :
            if mode == "all" :
                olditem = self.items[place]
                self.items[place] = "0"
                return(olditem)

            if mode == "half" :
                olditem = copy.copy(self.items[place])
                olditem.quantity = ceil(olditem.quantity/2)
                self.items[place].quantity -= olditem.quantity
                if self.items[place].quantity == 0:
                    self.items[place] = "0"
                    return(olditem)

            if mode == "one" :
                olditem = copy.copy(self.items[place])
                olditem.quantity = 1
                self.items[place].quantity -= 1
                if self.items[place].quantity == 0:
                    self.items[place] = "0"

        else :    
            if place == -1 : 
                for n in range (len(self.items)) :
                    if self.items[n] == "0":
                        self.items[n] = itemadded
                        break
                    if self.items[n].nom == itemadded.nom :
                        self.items[n].quantity += itemadded.quantity
                        break

            elif self.items[place] != "0":
                if self.items[place].nom == itemadded.nom :
                    self.items[place].quantity += itemadded.quantity
                    return ("It worked !")
                else : 
                    olditem = self.items[place]
                    self.items[place] = itemadded
                    return (olditem)
            else :
                self.items[place] = itemadded
                return ("It worked !")




    def render(self, largeur) : #Crée une surface avec tous les items dans un rectangle de largeur donnée en pixel
        itemperline = (largeur)//34
        itempercolumn = ceil(len(self.items)/itemperline)
        surfacefinale = pygame.Surface((itemperline*34, itempercolumn*34),pygame.SRCALPHA, 32).convert_alpha()
        for n in range (len(self.items)) :
            x = n%itemperline
            y = n//itemperline
            if self.items[n] != "0" :
                surfacefinale.blit(self.items[n].texture,(x*34+1,y*34+1))
        return surfacefinale

