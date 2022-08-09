import time

import cv2
import numpy as np

from minimap import minimap
mm = minimap()

from utilities import set_foreground, get_screenshot

if __name__ == '__main__':
    set_foreground()

    while (True):

        mm.get_minimap()
        mm.get_anchors()
        anchor_img = mm.anchor_imgs[0] # 50,10
        w, h = anchor_img.shape[:2]
        if mm.minimap_img_last_frame is not None:
            # Apply template Matching
            res = cv2.matchTemplate(mm.minimap_img_last_frame, anchor_img, cv2.TM_CCOEFF)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            offset = (cv2.minMaxLoc(res)[3][0],cv2.minMaxLoc(res)[3][1])
            print(offset)
            mm.draw_rec()
            cv2.imshow('Computer Vision', mm.minimap_img_last_frame)


        mm.minimap_img_last_frame = mm.minimap_img


        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break
        time.sleep(0.5)
