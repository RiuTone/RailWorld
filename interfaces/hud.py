from pgzero import screen
from player import Player

from pygame import Rect


class Hud:
    def __init__(self, player: Player):
        self.player = player
        
        self.rect = Rect(0, 480-62, 720, 62)
        
    
    def draw(self, screen: screen.Screen):
        screen.draw.filled_rect(self.rect, (34, 29, 33))

        screen.draw.text(f'Hp: {int(self.player.hp)}', (20, 432), fontname='pixelify_sans', fontsize=23)
        screen.draw.text(f'Stamina: {int(self.player.stamina)}', (238, 432), fontname='pixelify_sans', fontsize=23)
        
        screen.draw.text(f'Machine Cores: {int(self.player.machineCores)}', (483, 425), fontname='pixelify_sans', fontsize=17, color=(227, 60, 8))
        screen.draw.text(f'Level: {int(self.player.level)}', (483, 454), fontname='pixelify_sans', fontsize=17, color=(247, 112, 20))
        
        return
    
    def update(self):
        if self.rect.colliderect(self.player.rect):
            self.player.actor.y -= self.player.vel

        return