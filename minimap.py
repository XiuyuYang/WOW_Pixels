import math

from os import walk
import cv2
import numpy as np

from utilities import get_screenshot, vector_angle, rotate_image


class MiniMap:
    def __init__(self):
        self.current_path_fname = None
        self.path_img_list = []
        self.record_img_index = 0
        self.record_distance = 3
        self.path_img = None
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
        self.save_path = "Path"

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

    def get_target(self):
        most_confidence = 0
        angle = None
        distance = None
        for anchor in self.anchors:
            anchor.minimap_img_last_frame = self.path_img
            anchor.update_minimap_img(self.minimap_img)
            anchor.get_target()
            if anchor.confidence > most_confidence:
                most_confidence = anchor.confidence
                angle = anchor.move_angle
                distance = anchor.distance
        self.move_angle = int(angle)
        self.distance = distance

    def record_path(self, title="path"):
        if self.distance > self.record_distance:
            self.path_img = self.minimap_img
            name = title + "_" + str(self.record_img_index)
            self.save_img(name)
            print("recorded:", self.record_img_index)
            self.record_img_index += 1
        pass

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
        self.get_orientation()
        colors = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255))

        # draw orientation
        orientation = "ori:" + str(self.orientation) + "\'"
        org = (10, 40)
        self.draw_minimap_img = cv2.putText(self.draw_minimap_img, orientation, org, cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                                            (255, 255, 255), 1, cv2.LINE_AA)

        # draw distance
        distance = "dis:" + str(int(self.distance))
        org = (10, 140)
        self.draw_minimap_img = cv2.putText(self.draw_minimap_img, distance, org, cv2.FONT_HERSHEY_SIMPLEX, 0.4,
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

    def save_img(self, name):
        if self.minimap_img is None:
            self.get_minimap()
        file_name = self.save_path + "/" + name + ".jpg"
        cv2.imwrite(file_name, self.minimap_img)

    def load_path_img(self, name):
        try:
            self.path_img = cv2.imread(self.save_path + "/" + name)
        except:
            self.path_img = cv2.imread(self.save_path + "/" + "path_0.jpg")

    def load_next_path_img(self):
        fname = self.current_path_fname[:-4]
        fname, index = fname.split("_")
        index = str(int(index) + 1)
        self.current_path_fname = fname + "_" + index + ".jpg"
        print("loading next")
        print(self.current_path_fname)
        self.load_path_img(self.current_path_fname)

    def load_path_img_list(self):
        for (dirpath, dirnames, filenames) in walk(self.save_path):
            self.path_img_list.extend(filenames)
            break

    def find_closest_point(self):
        self.load_path_img_list()
        closest_point = {}
        for img_file_name in self.path_img_list:
            path_img = cv2.imread(self.save_path + "/" + img_file_name)
            res = cv2.matchTemplate(self.minimap_img, path_img, cv2.TM_CCOEFF_NORMED)
            confidence = np.max(res)
            closest_point[img_file_name] = confidence
        self.current_path_fname = max(closest_point, key=closest_point.get)
        print("Found closest path:", self.current_path_fname)

    def init_path(self):
        self.current_path_fname = "path_0.jpg"
        self.load_path_img(self.current_path_fname)

class Anchor:
    def __init__(self, minimap_img):
        self.distance = 0
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

    def get_target(self):
        self.get_anchor_img()
        res = cv2.matchTemplate(self.minimap_img_last_frame, self.img, cv2.TM_CCOEFF_NORMED)
        self.confidence = np.max(res)
        offset = (cv2.minMaxLoc(res)[3][0], cv2.minMaxLoc(res)[3][1])
        move = self.center[0] - offset[0] - self.anchors_half_size, self.center[1] - offset[1] - self.anchors_half_size
        self.distance = math.sqrt(sum(v ** 2 for v in move))
        self.move_angle = vector_angle((0, -1), move)

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
