import keyboard

import move
from minimap import MiniMap
from utilities import set_foreground

mm = MiniMap()
move = move.Move()
move.minimap = mm
mm.init_path()

if __name__ == '__main__':
    set_foreground()
    while True:
        if keyboard.is_pressed(","):
            move.stop_moving()
            break

        move.patrol()

        # mm.record_path()

        mm.show_minimap()
