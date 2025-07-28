from pgzero import actor, screen
from enemy import Enemy


class Weapon:
    def __init__(self):
        self.sprites = [
            (('atk_sword', 'atk_sword_f'), 25),
            (('atk_spear', 'atk_spear_f'), 55),
            (('atk_hammer', 'atk_hammer_f'), 35),
            ('atk_nunchaku', 'atk_nunchaku_f'),
        ]

        self.index = 0

        self.actor = None
        self.rect = None

        self.damage = 3
        self.staminaCost = 4


    def draw(self, pos: tuple[int], flipped: bool = False) -> actor.Actor:

        if isinstance(sprite := self.sprites[self.index], tuple):
            sprite_name, offset = sprite

            if isinstance(offset, str):
                offset = 0

            if isinstance(sprite_name, tuple):
                if flipped:
                    self.actor = actor.Actor(sprite_name[1], pos=(pos[0] + (offset * (-1)), pos[1]))
                    return self.actor
                
                self.actor = actor.Actor(sprite_name[0], pos=(pos[0] + offset, pos[1]))
                return self.actor

            self.actor = actor.Actor(sprite_name, pos=(pos[0] + offset, pos[1]))
            return self.actor
        
        self.actor = actor.Actor(self.sprites[self.index], pos)
        return self.actor
    

    def update(self, screen: screen.Screen, enemylist: list[Enemy]):
        
        if self.actor == None:
            return

        if self.rect == None:
            return

        # screen.draw.rect(self.rect, (255,0,0))

        for e in enemylist:

            if e.rect == None:
                continue

            collide = self.rect.colliderect(e.rect)
            
            if collide and not e.hurting:
                e.aplydamage(self.damage)
                e.hurting = True
            
        return