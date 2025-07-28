from pgzero import screen, actor

from pygame import Rect

from interfaces.mainmenu import Mainmenu
from interfaces.hud import Hud

from elements import Element
from random import randint
from player import Player
from enemy import Enemy


class Control:
    def __init__(self, width, height, sounds):

        self.onMainMenu = True
        self.mainmenu = Mainmenu()

        self.onTrain = False

        self.room = 0
        self.clearRoom = True

        self.gameOver = False

        self.enemies: list[Enemy] = []
        self.elements: list[Element] = []

        self.audios = True

        self.player = Player(4, self.enemies, (82, 312), control=self, sounds=sounds)
        self.hud = Hud(self.player)

        Enemy.init(self.player, self.enemies, sounds)
        Element.init(self.player, self.elements, sounds)

        self.bgList = [actor.Actor('background', topleft=(720 * i, -100)) for i in range(2)]
        self.train = actor.Actor('train', topleft=(0,0))

        self.transition = 0

        
    def draw(self, screen: screen.Screen):
        
        if self.onMainMenu:
            self.mainmenu.draw(screen)
            return

        if self.transition != 0:
            pos = -480
            
            if pos + 10 * self.transition >= 0:
                pos = 0
            else:
                pos = pos + 15 * self.transition

            screen.draw.filled_rect(Rect(0, pos, 720, 480), (0,0,0))

        if self.onTrain:


            if len(self.enemies) == 0:
                
                if self.transition > 90:
                    self.transition = 0
                    self.clear()
                else:
                    self.transition += 1
                
                return

            for img in self.bgList:

                if img.topleft[0] <= -720:
                    img.topleft = (720, -100)
                else:
                    img.x -= 10

                img.draw()

            self.train.draw()

            for act in reversed(self.player.playerGroup):
                act.draw()

            for enemy in self.enemies:
                enemy.draw(screen)

            for element in self.elements:
                element.draw(screen)

            self.hud.draw(screen)

            self.player.weapon.update(screen, self.enemies)
            self.player.draw(screen)

        return
    

    def update(self, keyboard, mouse_button, pos):

        if self.onMainMenu:

            if self.mainmenu.isClosed:
                self.onMainMenu = False
                self.onTrain = True
                self.audios = self.mainmenu.audios
                self.genEnemies()

            self.mainmenu.update(keyboard, mouse_button, pos)
            return

        if self.onTrain:
            self.player.control(keyboard, mouse_button, pos)

            self.player.update()
            self.hud.update()

            for enemy in self.enemies:
                enemy.update()

            for element in self.elements:
                element.update()

        return


    def genEnemies(self):
        self.clearRoom = False

        for i in range(randint(1,5)):
            Enemy((536 - 25 * randint(0,1), 257 + 30 * i), randint(0,1))

        return


    def clear(self):
        self.player.actor.pos = (82, 312)

        self.enemies.clear()
        self.genEnemies()

        self.room += 1

        return
