import keyboard
import time

import mouse

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
    time.sleep(1)
    mm.init_path()
    # at = attack.Magic()
    at = attack.Druid()
    at.need_loot = True
    at.skinning = True
    mv.mouse_press_right()
    utilities.mount()
    while True:
        # find target then attack
        if at.search_target():
            # found target
            at.attack()
            mv.move_back()
        # patrol
        else:
            mv.patrol()


def record():
    utilities.mount()
    while True:
        mm.record_path()


if __name__ == '__main__':
    utilities.set_foreground()

    run()
    # record()
    # just_patrol()

    # mm.show_minimap()
