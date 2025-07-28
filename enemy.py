from pgzero import actor, screen

from elements import Element
from pygame import Rect


class Enemy:
    enemies = None
    player = None
    sounds = None

    def __init__(self, pos: tuple[int], index: int = 0):

        self.sprites = [
            ('enemy_1', 'enemy_1_f'),
            ('mine_01', 'mine_02')
        ]

        self.stats = [
            {'vel': 1.5, 'atk': 3, 'hp': 15},
            {'vel': 1.5, 'atk': 15, 'hp': 10}
        ]

        self.frameCounter = {
            'hurting': 0,
            'alphastep': 0,
            'litstep': 0,
            'supressed': 0,
            'exploding': 0,
            'explosionradius': 1,
        }

        self.index = index

        self.lited = False
        self.hurting = False
        self.stucking = False
        self.invisible = False
        self.supressed = False

        self.explosive = index == 1
        self.explosionPos = None

        self.direction = [0, 0]

        self.hp = self.stats[index]['hp']

        self.actor = actor.Actor(self.sprites[index][0], pos=pos)
        self.rect = Rect(*self.actor.topleft, 64, 64)
        
        self.enemies.append(self)


    def update(self):

        if self.supressed:
            self.stucking = True

            if self.frameCounter['supressed'] >= 50:
                self.frameCounter['supressed'] = 0
                self.supressed = False
                self.stucking = False
            else:
                self.frameCounter['supressed'] += 1


        if self.hurting:
            
            if self.frameCounter['hurting'] >= 50:
                self.frameCounter['hurting'] = 0
                self.hurting = False
                self.invisible = False

                self.actor._surf.set_alpha(255)

            else:

                if self.frameCounter['alphastep'] >= 7:

                    self.actor._surf.set_alpha(0 if self.invisible else 255)
                    
                    self.frameCounter['alphastep'] = 0
                    self.invisible = not self.invisible
                    
                else:
                    self.frameCounter['alphastep'] += 1

                self.frameCounter['hurting'] += 1


        if not self.stucking:

            if self.actor.x < self.player.actor.x and self.index == 0:
                self.actor.image = self.sprites[0][0]

            elif self.index == 0:
                self.actor.image = self.sprites[0][1]

            lead_distance = 40
            target_x = self.player.actor.x + self.direction[0] * lead_distance
            target_y = self.player.actor.y + self.direction[1] * lead_distance

            dx = target_x - self.actor.x
            dy = target_y - self.actor.y

            dist = (dx**2 + dy**2) ** 0.5
            if dist != 0:
                self.actor.x += self.stats[self.index]['vel'] * dx / dist
                self.actor.y += self.stats[self.index]['vel'] * dy / dist
            
            self.rect.x, self.rect.y = self.actor.topleft


        if self.explosive:
            distance = self.actor.distance_to(self.player.actor)
            
            if distance <= 64:
                self.stucking = True

                if self.frameCounter['exploding'] >= 80:

                    if self.player.kwargs['control'].audios:
                        self.sounds.explosion.play()

                    self.actor._surf.set_alpha(0)
                    self.stucking = True
                    self.explosive = False
                    self.explosionPos = self.rect.center

                else:
                    self.frameCounter['exploding'] += 1

                    if self.frameCounter['litstep'] >= 7:
                        self.actor.image = self.sprites[self.index][1 if self.lited else 0]
                        self.lited = not self.lited
                        self.frameCounter['litstep'] = 0
                    else:
                        self.frameCounter['litstep'] += 1
            else:
                self.actor.image = self.sprites[self.index][0]
                self.frameCounter['exploding'] = 0
                self.stucking = False
        
        elif self.rect.colliderect(self.player.rect) and not self.player.hurting:
            self.player.hurting = True
            self.player.aplydamage(self.stats[self.index]['atk'])

        return
    

    def draw(self, screen: screen.Screen):
        self.actor.draw()
        # screen.draw.rect(self.rect, (255, 0,0))

        if self.explosionPos != None:
            screen.draw.filled_circle(self.explosionPos, radius= self.frameCounter['explosionradius'], color=(255, 60, 0))
            self.rect.w, self.rect.h = [self.frameCounter['explosionradius'] * 2] * 2
            self.rect.center = self.explosionPos
            
            if self.frameCounter['explosionradius'] >= 120:
                self.enemies.remove(self)
                return
            
            else:
                self.frameCounter['explosionradius'] += 10

        return


    def aplydamage(self, value: int) -> None:
        self.supressed = True

        self.hp -= value

        if self.hp <= 0:
            Element(self.actor.pos)
            self.enemies.remove(self)
        
        return


    @classmethod
    def init(cls, player, enemies, sounds):
        if enemies == None:
            pass
        else:
            cls.enemies = enemies

        cls.sounds = sounds
        cls.player = player
        return
