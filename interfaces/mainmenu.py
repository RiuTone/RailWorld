from pgzero import screen

from pygame import Rect


class Mainmenu:
    def __init__(self):
        self.cursorRect = Rect(0, 0, 10, 10)

        self.isClosed = False
        self.mouseIn = None
        self.audios = True

        self.options = (
            'Jogar',
            'Audio: {}',
            'Sair'
        )

    
    def draw(self, screen: screen.Screen):
        screen.fill((31, 37, 54))

        screen.draw.text('RailWorld', fontname='pixelify_sans', pos=(35, 24), fontsize=64)
        
        for i, optionName in enumerate(self.options):
            rect = Rect(*(35, 120 + 40 * i), 120, 24)
            color = (255, 255, 255)

            # screen.draw.rect(rect, color=(255,0,0))

            if self.cursorRect.colliderect(rect):
                color = (252, 52, 8)
                self.mouseIn = i

            if i == 1:
                screen.draw.text(optionName.format(self.audios), fontname='pixelify_sans', pos=(35, 120 + 40 * i), fontsize=24, color=color)
                continue

            screen.draw.text(optionName, fontname='pixelify_sans', pos=(35, 120 + 40 * i), fontsize=24, color=color)
        
        # screen.draw.rect(self.cursorRect, (255,0,0))

        return
    

    def update(self, keyboard, mouse_button, mouse_pos):
        if mouse_button == 1 and (index := self.mouseIn) != None:
            match index:
                case 0:
                    self.isClosed = True

                case 1:
                    self.audios = not self.audios

                case 2:
                    quit()

        if mouse_pos != None:
            self.cursorRect.x, self.cursorRect.y = mouse_pos

        return


