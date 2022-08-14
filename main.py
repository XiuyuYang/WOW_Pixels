from minimap import MiniMap
from utilities import set_foreground

mm = MiniMap()

if __name__ == '__main__':
    set_foreground()
    while True:
        mm.get_minimap()
        mm.get_direction()
        mm.get_orientation()
        mm.show_minimap()
