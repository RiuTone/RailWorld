from pgzero import actor, screen, animation

from random import randint
from pygame import Rect


class Element:
    elements: list = None
    sounds = None
    player = None

    def __init__(self, pos: tuple[int]):
        self.sprites = ('xp_point', 'machine_core')
        self.index = randint(0,1)

        self.value = randint(5,15)

        self.actor = actor.Actor(self.sprites[self.index], pos)
        self.elements.append(self)

        self.rect = Rect(*self.actor.topleft, *self.actor._surf.get_size())


    def draw(self, screen: screen.Screen):
        self.actor.draw()
        animation.animate(self.actor, pos=self.player.actor.pos, duration=0.5)
        # screen.draw.rect(self.rect, (255,0,0))
        return
    

    def update(self):
        self.rect.x, self.rect.y = self.actor.topleft

        if self.rect.colliderect(self.player.rect):
            self.player.getelement(self.value, self.index)
            self.elements.remove(self)

        return

    
    @classmethod
    def init(cls, player, elements, sounds):
        if elements == None:
            pass
        else:
            cls.elements = elements

        cls.sounds = sounds        
        cls.player = player
        return
