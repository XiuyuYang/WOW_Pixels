import cv2
from utilities import mkdir, set_foreground

from utilities import get_screenshot


class minimap():
    def __init__(self):
        self.center_point = (1818, 131)
        self.minimap_half_size = 80
        self.minimap_img_last_frame = None
        self.minimap_img = None
        self.anchors_half_size = 30
        self.anchor_imgs = []
        self.anchor_rec_list = []

    def get_minimap(self):
        bbox = (self.center_point[0] - self.minimap_half_size,
                self.center_point[1] - self.minimap_half_size,
                self.center_point[0] + self.minimap_half_size,
                self.center_point[1] + self.minimap_half_size)
        self.minimap_img = get_screenshot(bbox=bbox)

    def get_anchors(self):
        shape = self.minimap_img.shape
        points = [
            (shape[0] / 2.0, shape[1] / 4.0),
            (shape[0] / 4.0, shape[1] / 2.0),
            (shape[0] / 4.0 * 3, shape[1] / 2.0),
            (shape[0] / 2.0, shape[1] / 4.0 * 3)
        ]
        self.anchor_rec_list = []
        for center in points:
            x_start = int(center[0] - self.anchors_half_size)
            x_end = int(center[0] + self.anchors_half_size)
            y_start = int(center[1] - self.anchors_half_size)
            y_end = int(center[1] + self.anchors_half_size)
            anchor_img = self.minimap_img[y_start:y_end, x_start:x_end]
            self.anchor_rec_list.append([x_start, x_end, y_start, y_end])
            self.anchor_imgs.append(anchor_img)

    def draw_rec(self):
        # image = cv2.rectangle(image, start_point, end_point, color, thickness)
        colors = ((255, 0, 0),(0, 255, 0),(0, 0, 255),(255, 0, 255))
        print(self.anchor_rec_list)
        for i in range(len(self.anchor_rec_list)):
            rec = self.anchor_rec_list[i]
            self.minimap_img = cv2.rectangle(self.minimap_img, (rec[0], rec[1]), (rec[2], rec[3]), colors[i], 2)
