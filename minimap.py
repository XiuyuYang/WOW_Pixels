import math

import cv2
import numpy as np
import time

from utilities import get_screenshot, angle


# noinspection PyStatementEffect
class MiniMap():
    def __init__(self):
        self.magnitude = 3
        self.angle = None
        self.move_vector = []
        self.player_arrow_img = None
        self.show_minimap_start_time = None
        self.refresh_time = 0.1
        self.center_point = (1818, 131)
        self.minimap_half_size = 80
        self.minimap_img_last_frame = None
        self.minimap_img = None
        self.anchors_half_size = 20
        self.anchor_rec_list = []
        self.draw_minimap = True
        self.draw_minimap_img = None
        self.offsets = None
        self.template_arrow_path = "minimap_img/PlayerTemplate.jpg"
        self.player_arrow_size = 20

    def get_minimap(self):
        bbox = (self.center_point[0] - self.minimap_half_size,
                self.center_point[1] - self.minimap_half_size,
                self.center_point[0] + self.minimap_half_size,
                self.center_point[1] + self.minimap_half_size)
        self.minimap_img = get_screenshot(bbox=bbox)
        if self.minimap_img_last_frame is None:
            self.minimap_img_last_frame = self.minimap_img

    def get_anchors(self):
        anchor_imgs = []
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
            anchor_imgs.append(anchor_img)
        return anchor_imgs

    def get_direction(self):
        anchor_imgs = self.get_anchors()
        offsets = {}
        for i in range(len(anchor_imgs)):
            res = cv2.matchTemplate(self.minimap_img_last_frame, anchor_imgs[i], cv2.TM_CCOEFF_NORMED)
            confidence = np.max(res)
            offset = (cv2.minMaxLoc(res)[3][0], cv2.minMaxLoc(res)[3][1])
            offsets[i] = offset
            if self.draw_minimap:
                self.draw_rec(i, confidence)
        if self.offsets is None:
            self.offsets = list(offsets.values())
        else:
            most_confidence = max(offsets, key=offsets.get)
            move = [[self.offsets[0][0] - offsets[0][0], self.offsets[0][1] - offsets[0][1]],
                    [self.offsets[1][0] - offsets[1][0], self.offsets[1][1] - offsets[1][1]],
                    [self.offsets[2][0] - offsets[2][0], self.offsets[2][1] - offsets[2][1]],
                    [self.offsets[3][0] - offsets[3][0], self.offsets[3][1] - offsets[3][1]]]
            magnitude = math.sqrt(sum(v ** 2 for v in move[0]))
            if magnitude > self.magnitude:
                self.angle = angle((0, self.magnitude), (move[most_confidence][0], move[most_confidence][1]))
                print(self.angle)
                self.minimap_img_last_frame = self.minimap_img

    def show_minimap(self):
        if self.show_minimap_start_time is not None:
            delta_time = time.time() - self.show_minimap_start_time
            if delta_time <= self.refresh_time:
                return
        if not self.draw_minimap:
            img = self.minimap_img
        else:
            img = self.draw_minimap_img

        cv2.imshow('Computer Vision', img)
        self.draw_minimap_img = None

        self.show_minimap_start_time = time.time()

    def get_template_arrow(self):
        template_arrow = cv2.imread(self.template_arrow_path)
        return template_arrow

    def get_player_arrow(self):
        shape = self.minimap_img.shape
        center = (shape[0] / 2, shape[1] / 2)
        x_start = int(center[0] - (self.player_arrow_size / 2))
        x_end = int(center[0] + (self.player_arrow_size / 2))
        y_start = int(center[1] - (self.player_arrow_size / 2))
        y_end = int(center[1] + (self.player_arrow_size / 2))
        player_arrow_img = self.minimap_img[y_start:y_end, x_start:x_end]
        return player_arrow_img

    def get_rotation(self):
        template_arrow = self.get_template_arrow()
        pass

    def show_arrow(self):
        img = self.get_player_arrow()
        cv2.imshow('arrow', img)
        cv2.waitKey(1)

    def draw_rec(self, index, confidence):
        if self.draw_minimap_img is None:
            self.draw_minimap_img = self.minimap_img.copy()
        # image = cv2.rectangle(image, start_point, end_point, color, thickness)
        colors = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255))
        rec = self.anchor_rec_list[index]
        self.draw_minimap_img = cv2.rectangle(self.draw_minimap_img,
                                              (rec[0], rec[2]), (rec[1], rec[3]),
                                              colors[index], 1)
        text = str(int(confidence * 100)) + "%"
        org = (rec[0], rec[2])
        self.draw_minimap_img = cv2.putText(self.draw_minimap_img, text, org, cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                                            (0, 255, 255), 1, cv2.LINE_AA)
