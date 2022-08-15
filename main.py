import move
from minimap import MiniMap
from utilities import set_foreground

mm = MiniMap()
mm.load_path_img("Test")

move = move.Move()
move.minimap = mm
move.need_rotate = True

mm.get_direction()

if __name__ == '__main__':
    set_foreground()
    while True:
        mm.get_minimap()
        mm.get_direction()
        move.rotate_to()
        move.go_to()
        mm.show_minimap()
