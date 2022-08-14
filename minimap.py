import math

import cv2
import numpy as np

from utilities import get_screenshot, vector_angle, rotate_image


class MiniMap:
    def __init__(self):
        self.anchors = []
        self.orientation = None
        self.magnitude = 3
        self.move_angle = 0
        self.center_point = (1818, 131)
        self.minimap_half_size = 80
        self.minimap_img_last_frame = None
        self.minimap_img = None
        self.draw_minimap = True
        self.draw_minimap_img = None

        self.get_anchors()

    def get_minimap(self):
        bbox = (self.center_point[0] - self.minimap_half_size,
                self.center_point[1] - self.minimap_half_size,
                self.center_point[0] + self.minimap_half_size,
                self.center_point[1] + self.minimap_half_size)
        self.minimap_img = get_screenshot(bbox=bbox)
        if self.minimap_img_last_frame is None:
            self.minimap_img_last_frame = self.minimap_img

    def get_anchors(self):
        if self.minimap_img is None:
            self.get_minimap()
        shape = self.minimap_img.shape
        points = [
            (shape[0] / 2.0, shape[1] / 4.0),
            (shape[0] / 4.0, shape[1] / 2.0),
            (shape[0] / 4.0 * 3, shape[1] / 2.0),
            (shape[0] / 2.0, shape[1] / 4.0 * 3)
        ]
        for i in range(len(points)):
            anchor = Anchor(self.minimap_img)
            anchor.center = points[i]
            anchor.id = i
            self.anchors.append(anchor)

    def get_direction(self):
        most_confidence = 0
        angle = None
        for anchor in self.anchors:
            anchor.update_minimap_img(self.minimap_img)
            anchor.get_direction()
            if anchor.moved_distance > self.magnitude and anchor.confidence > most_confidence:
                most_confidence = anchor.confidence
                angle = anchor.move_angle
        if angle is not None:
            self.move_angle = int(angle)
            for anchor in self.anchors:
                anchor.minimap_img_last_frame = self.minimap_img

    def get_orientation(self):
        arrow = Arrow()
        if self.minimap_img is None:
            self.get_minimap()
        arrow.minimap_img = self.minimap_img
        arrow.get_template_arrow()
        arrow.get_rotation()
        self.orientation = arrow.orientation

    def show_minimap(self):
        if self.draw_minimap:
            self.draw()
            cv2.imshow('Computer Vision', self.draw_minimap_img)
        else:
            cv2.imshow('Computer Vision', self.minimap_img)
        cv2.waitKey(1)
        self.draw_minimap_img = None

    def draw(self):
        if self.draw_minimap_img is None:
            self.draw_minimap_img = self.minimap_img.copy()
        colors = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255))

        # draw orientation
        text = "ori:" + str(self.orientation) + "\'"
        org = (10, 40)
        self.draw_minimap_img = cv2.putText(self.draw_minimap_img, text, org, cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                            (255, 255, 255), 1, cv2.LINE_AA)
        # draw anchors rectangle
        for i in range(len(self.anchors)):
            anchor = self.anchors[i]
            rec = anchor.rec
            self.draw_minimap_img = cv2.rectangle(self.draw_minimap_img,
                                                  (rec[0], rec[2]), (rec[1], rec[3]),
                                                  colors[i], 1)
            text = str(int(anchor.confidence * 100)) + "%"
            org = (rec[0], rec[2])
            self.draw_minimap_img = cv2.putText(self.draw_minimap_img, text, org, cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                                                (0, 255, 255), 1, cv2.LINE_AA)


class Anchor:
    def __init__(self, minimap_img):
        self.moved_distance = 0
        self.id = None
        self.draw_minimap_img = None
        self.confidence = None
        self.center = None
        self.move_angle = None
        self.init_offset = None
        self.is_drawing_rec = True
        self.img = None
        self.rec = None
        self.anchors_half_size = 20
        self.minimap_img = minimap_img
        self.minimap_img_last_frame = minimap_img

    def get_anchor_img(self):
        center = self.center
        x_start = int(center[0] - self.anchors_half_size)
        x_end = int(center[0] + self.anchors_half_size)
        y_start = int(center[1] - self.anchors_half_size)
        y_end = int(center[1] + self.anchors_half_size)
        self.img = self.minimap_img[y_start:y_end, x_start:x_end]
        self.rec = [x_start, x_end, y_start, y_end]

    def get_direction(self):
        self.get_anchor_img()
        res = cv2.matchTemplate(self.minimap_img_last_frame, self.img, cv2.TM_CCOEFF_NORMED)
        self.confidence = np.max(res)
        offset = (cv2.minMaxLoc(res)[3][0], cv2.minMaxLoc(res)[3][1])
        if self.init_offset is None:
            self.init_offset = offset
        else:
            move = [self.init_offset[0] - offset[0], self.init_offset[1] - offset[1]]
            self.moved_distance = math.sqrt(sum(v ** 2 for v in move))
            self.move_angle = vector_angle((0, 1), move)

    def update_minimap_img(self, minimap_img):
        self.minimap_img = minimap_img


class Arrow:
    def __init__(self):
        self.orientation = None
        self.player_arrow_img = None
        self.template_arrow = None
        self.minimap_img = None
        self.template_arrow_path = "minimap_img/PlayerTemplate.jpg"
        self.player_arrow_size = 20

    def get_template_arrow(self):
        self.template_arrow = cv2.imread(self.template_arrow_path)

    def get_player_arrow(self):
        shape = self.minimap_img.shape
        center = (shape[0] / 2, shape[1] / 2)
        x_start = int(center[0] - (self.player_arrow_size / 2))
        x_end = int(center[0] + (self.player_arrow_size / 2))
        y_start = int(center[1] - (self.player_arrow_size / 2))
        y_end = int(center[1] + (self.player_arrow_size / 2))
        self.player_arrow_img = self.minimap_img[y_start:y_end, x_start:x_end]

    def get_rotation(self):
        self.get_player_arrow()
        rotate_angle = [0, 0]
        for i in range(0, 360):
            rotated_template_arrow = rotate_image(self.template_arrow, i)
            res = cv2.matchTemplate(rotated_template_arrow, self.player_arrow_img, cv2.TM_CCOEFF_NORMED)
            confidence = np.max(res)
            if confidence > rotate_angle[1]:
                rotate_angle = [i, confidence]
        self.orientation = rotate_angle[0]
        pass

    def show(self):
        cv2.imshow('arrow', self.player_arrow_img)
        cv2.waitKey(1)
