from pgzero import actor, screen
from weapon import Weapon

from pygame import Rect


class Player:
    def __init__(self, inicial_vel: int, enemylist: list, pos: tuple[int], **kwargs):
        self.enemies = enemylist
        
        self.kwargs = kwargs

        self.sprites = [
            ('mig_0', 'mig_0_f'),
            ('mig_1', 'mig_1_f'),
            ('mig_moving', 'mig_moving_f'),
            ('mig_attacking', 'mig_attacking_f.png'),
            'mig_damage',
            ]

        self.vel = inicial_vel

        self.playerGroup: list[actor.Actor] = []

        self.actor = actor.Actor(self.sprites[0][0], center=pos)
        self.rect = Rect(*self.actor.topleft, self.actor._surf.get_size()[0] - 25, self.actor._surf.get_size()[1])
        
        self.playerGroup.append(self.actor)

        self.weapon = Weapon()

        self.level = 0

        self.stamina = 15 + (15 * (0.2 * self.level))
        self.hp = 20 + (20 * (0.2 * self.level))

        self.xpPoints = 0
        self.machineCores = 0

        self.moving = False
        self.hurting = False
        self.flipped = False
        self.invisible = False
        self.attacking = False

        self.collisions = (
            Rect(-29,0, 30, 480),
            Rect(719,0, 30, 480),
            Rect(0, 160, 720, 30),
            Rect(6, 202, 58, 90),
            Rect(652, 212, 50, 90)
        )

        self.frameCounter: dict[str, int | list] = {
            'moving': [0, 0],
            'stepping': 0,
            'attacking': 0,
            'hurting': 0,
            'alphastep': 0,
            'stopped': 0,
            'blink': 0,
            'stmreg': 0,
            'hpreg': 0,
            }

    
    def control(self, keyboard, mouse, pos):
        moving = False

        if keyboard.a:
            self.actor.x -= self.vel
            self.flipped = True
            moving = True
            
        elif keyboard.d:
            self.actor.x += self.vel
            self.flipped = False
            moving = True


        if keyboard.w:
            self.actor.y -= self.vel
            moving = True

        elif keyboard.s:
            self.actor.y += self.vel
            moving = True

        if moving:
            self.frameCounter['moving'][0] += 1
            self.moving = True


        if mouse == 1:
            self.attack()

        # if mouse == 2:
        #     print(pos)
        
        # if mouse == 3:
        #     self.weapon.index = (self.weapon.index + 1) % len(self.weapon.sprites)
        #     print(self.weapon.index)

        return


    def draw(self, screen: screen.Screen):
        # screen.draw.rect(self.rect, (255,0,0))
        
        # for c in self.collisions:
        #     screen.draw.rect(c, (255,0,0))
        return


    def update(self):
        self.rect.x = self.actor.topleft[0] + 12
        self.rect.y = self.actor.topleft[1]


        if self.attacking:
            self.actor.image = self.flippedsprite(3)
            
            if self.frameCounter['attacking'] >= 5:
                self.attacking = False
                
                for i in range(len(self.playerGroup)):
                    if len(self.playerGroup) == 1:
                        break
                    else:
                        self.playerGroup.pop(0)

                self.frameCounter['attacking'] = 0
                self.frameCounter['moving'] = [0,0]
                
                self.weapon.rect = None
            
            else:
                self.frameCounter['attacking'] += 1


        elif self.moving:

            previousframe, correntframe = self.frameCounter['moving']

            if previousframe + 4 <= correntframe:
                self.frameCounter['moving'] = [0,0]
                self.moving = False
            
            else:
                if self.frameCounter['stepping'] < 10:
                    self.actor.image = self.flippedsprite(0)
                    
                elif self.frameCounter['stepping'] < 20:
                    self.actor.image = self.flippedsprite(2)

                    
                else:
                    self.frameCounter['stepping'] = 0
                
                self.frameCounter['stepping'] += 1
                self.frameCounter['moving'][1] += 1


        else:
            self.actor.image = self.flippedsprite(0)

            if self.frameCounter['stopped'] >= 80:
                self.actor.image = self.flippedsprite(1)
                self.frameCounter['blink'] += 1
        
                if self.frameCounter['blink'] >= 40:
                    self.actor.image = self.flippedsprite(0)
                    self.frameCounter['stopped'] = 0
                    self.frameCounter['blink'] = 0
            else:
                self.frameCounter['stopped'] += 1
        
        if self.hurting:

            self.actor.image = self.sprites[-1]

            if self.frameCounter['hurting'] >= 40:
                self.frameCounter['hurting'] = 0
                self.hurting = False
                self.invisible = False
                self.actor.image = self.flippedsprite(0)
                self.actor._surf.set_alpha(255)

            else:

                if self.frameCounter['alphastep'] >= 7:

                    self.actor._surf.set_alpha(0 if self.invisible else 255)
                    
                    self.frameCounter['alphastep'] = 0
                    self.invisible = not self.invisible
                    
                else:
                    self.frameCounter['alphastep'] += 1

                self.frameCounter['hurting'] += 1

        if self.stamina < 15 + (15 * (0.2 * self.level)) and not self.attacking:
            if self.frameCounter['stmreg'] >= 90:
                self.frameCounter['stmreg'] = 0
                self.stamina += 4
                
                if self.stamina > 15 + (15 * (0.2 * self.level)):
                    self.stamina = 15 + (15 * (0.2 * self.level))

            else:
                self.frameCounter['stmreg'] += 1
        
        if self.hp < 20 + (20 * (0.2 * self.level)) and not self.hurting:
            if self.frameCounter['hpreg'] >= 90:
                self.frameCounter['hpreg'] = 0
                self.hp += 4
                
                if self.hp > 20 + (20 * (0.2 * self.level)):
                    self.hp = 20 + (20 * (0.2 * self.level))

            else:
                self.frameCounter['hpreg'] += 1

        if len(colliders_index := self.rect.collidelistall(self.collisions)) != 0:
            for i in colliders_index:
                match i:
                    case 0:
                        self.actor.x += self.vel
                    
                    case 1:
                        self.actor.x -= self.vel
                   
                    case 2:
                        self.actor.y += self.vel
                    
                    case 3:
                        self.actor.x += self.vel
                    
                    case 4:
                        self.actor.x -= self.vel

        return


    def flippedsprite(self, index: int):
        if not isinstance(self.sprites[index], tuple):
            return self.sprites[index]
        
        if self.flipped:
            return self.sprites[index][1]
        
        return self.sprites[index][0]        


    def attack(self):
        
        if self.stamina - self.weapon.staminaCost < 0: 
            return
        
        if self.kwargs['control'].audios:
            self.kwargs['sounds'].attack.play()

        self.stamina -= self.weapon.staminaCost 
        self.attacking = True

        self.playerGroup.insert(0, self.weapon.draw(self.actor.pos, self.flipped))
        self.weapon.rect = Rect(*self.weapon.actor.topleft, *self.weapon.actor._surf.get_size())

        return


    def aplydamage(self, value: int) -> None:

        self.hp -= value
        
        if self.hp <= 0:
            self.level = 0
            self.xpPoints = 0
            self.machineCores = 0

            self.hp = 20 + (20 * (0.2 * self.level))

            self.kwargs['control'].onMainMenu = True
            self.kwargs['control'].onTrain = False
            self.kwargs['control'].mainmenu.isClosed = False
            self.kwargs['control'].clear()

        if self.hp < 0:
            self.hp = 0
        
        return


    def getelement(self, value: int, elementindex: int):

        if elementindex == 0:
            self.xpPoints += value

            if self.xpPoints >= 10 + (10 * self.level):
                self.xpPoints -= 10 + (10 * self.level)
                self.level += 1

        else:
            self.machineCores += value

        return

