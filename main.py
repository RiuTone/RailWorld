from gamecontrol import Control

import pgzrun


WIDTH = 720
HEIGHT = 480

mouse_button = None
mouse_pos = None

game = Control(WIDTH, HEIGHT, sounds)

def on_mouse_move(pos, rel, buttons):
    global mouse_pos

    mouse_pos = pos

    return


def draw():
    game.draw(screen)
    return
        

def update():
    global mouse_button, mouse_pos

    if keyboard.escape:
        quit()

    game.update(keyboard, mouse_button, mouse_pos)

    mouse_button = None
    mouse_pos = None
    return


def on_mouse_down(pos, button):
    global mouse_button, mouse_pos
    
    mouse_button = button
    mouse_pos = pos

    return


pgzrun.go()
