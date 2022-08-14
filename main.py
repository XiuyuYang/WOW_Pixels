import cv2
import numpy as np
import time

from minimap import MiniMap
from utilities import set_foreground

mm = MiniMap()

if __name__ == '__main__':
    set_foreground()
    # mm.show_arrow()
    while True:
        mm.get_minimap()
        mm.get_template_arrow()
        mm.get_direction()
        mm.get_rotation()
        mm.show_minimap()
        # mm.show_arrow()
