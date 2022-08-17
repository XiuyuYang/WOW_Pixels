import move
from minimap import MiniMap
from utilities import set_foreground

mm = MiniMap()

move = move.Move()
move.minimap = mm
move.need_rotate = True
# mm.find_closest_point()
mm.init_path()

if __name__ == '__main__':
    set_foreground()
    while True:
        mm.get_minimap()
        move.rotate_to()
        move.go_to()

        # mm.record_path()

        mm.show_minimap()