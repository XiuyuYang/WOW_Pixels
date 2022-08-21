import keyboard
import time
import attack
import move
import utilities
from minimap import MiniMap
from utilities import set_foreground

mm = MiniMap()
mv = move.Move()
mv.minimap = mm
mm.init_path()

at = attack.Magic()

if __name__ == '__main__':
    set_foreground()
    while True:
        # user stop by press ","
        if keyboard.is_pressed(","):
            mv.stop_moving()
        # find target then attack
        if at.search_target():
            print("found the target.")
            # found target
            mv.stop_moving()
            at.attack()
            print("finished combat, coming back.")
            mv.move_back()
        # patrol
        else:
            mv.patrol()

            # mm.record_path()

        mm.show_minimap()
