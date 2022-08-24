import keyboard
import time
import attack
import move
import minimap
import utilities

mm = minimap.MiniMap()
mv = move.Move()
mv.minimap = mm


def just_patrol():
    mm.init_path()
    while True:
        mv.patrol()


def run():
    utilities.init_ocr()
    time.sleep(1)
    mm.init_path()
    at = attack.Magic()
    at.need_loot = True
    while True:
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


def record():
    while True:
        mm.record_path()


if __name__ == '__main__':
    utilities.set_foreground()

    run()
    # record()
    # just_patrol()

    mm.show_minimap()
