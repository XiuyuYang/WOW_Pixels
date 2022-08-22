import time

import cv2
import keyboard
import easyocr
import numpy as np
import win32gui
from PIL import ImageGrab

reader = None


def set_foreground():
    hwnd = win32gui.FindWindow(None, '魔兽世界')
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)


def init_ocr():
    # init ocr
    global reader
    reader = easyocr.Reader(['ch_sim'])


def get_screenshot(bbox):
    img = ImageGrab.grab(bbox=bbox)  # x, y, w, h
    img_np = np.array(img)
    return cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)


def vector_angle(v1, v2):
    x1, y1 = v1
    x2, y2 = v2
    dot = x1 * x2 + y1 * y2
    det = x1 * y2 - y1 * x2
    theta = np.arctan2(det, dot)
    theta = theta if theta > 0 else 2 * np.pi + theta
    res = theta * 180 / np.pi
    if res == 360:
        res = 0
    return res


def rotate_image(image, angle):
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    m = cv2.getRotationMatrix2D(center, 360 - angle, 1.0)
    rotated = cv2.warpAffine(image, m, (w, h))
    # cv2.imshow('rotated', rotated)
    # cv2.waitKey(1)
    return rotated


def get_delta_angle(angle1, angle2):
    angle = abs(angle1 - angle2)
    if angle > 180:
        return 360 - angle
    else:
        return angle


def find_target(dead=False, threshold=0.9, skip=[]):
    bbox = (300, 52, 450, 90)
    target_area_img = get_screenshot(bbox)
    # cv2.imshow('target_area', target_area_img)
    # cv2.imwrite("Source_img/Target_2.jpg", target_area_img)
    # cv2.waitKey(0)
    temp_dead = cv2.imread("Source_img/dead.jpg")
    res = cv2.matchTemplate(target_area_img, temp_dead, cv2.TM_CCOEFF_NORMED)
    confidence_dead = np.max(res)
    if dead:
        return confidence_dead > 0.5

    # yellow names
    temp_img1 = cv2.imread("Source_img/Target_1.jpg")
    res1 = cv2.matchTemplate(target_area_img, temp_img1, cv2.TM_CCOEFF_NORMED)
    confidence1 = np.max(res1)
    # red names
    temp_img2 = cv2.imread("Source_img/Target_2.jpg")
    res2 = cv2.matchTemplate(target_area_img, temp_img2, cv2.TM_CCOEFF_NORMED)
    confidence2 = np.max(res2)
    if confidence1 > threshold or confidence2 > threshold:
        name = read_target_name()
        if name not in skip:
            return True
    else:
        return False


def read_target_name():
    t = time.time()
    bbox = (300, 52, 450, 90)
    target_area_img = get_screenshot(bbox)
    img = cv2.split(target_area_img)[1]
    # result = reader.readtext(img)[0][1]
    result = reader.readtext(img)
    if result:
        result = reader.readtext(img)[0][1]
        return result.strip(".")
    else:
        return None


def get_skill_num_img(index):
    size = 49.5 * (int(index) - 1)
    bbox = (395 + size, 987, 402 + size, 998)
    skill_num_img = get_screenshot(bbox)
    return skill_num_img
    # cv2.imshow('target_area', skill_num_img)
    # cv2.imwrite("Source_img/"+str(index+1)+"_1.jpg", skill_num_img)
    # cv2.waitKey(0)


def skill_in_range(index=1):
    skill_num_img = get_skill_num_img(index)
    # avaiable
    available_img = cv2.imread("Source_img/" + str(index) + "_0.jpg")
    available_res = cv2.matchTemplate(skill_num_img, available_img, cv2.TM_CCOEFF_NORMED)
    available_confidence = np.max(available_res)
    # unavailable
    unavailable_img = cv2.imread("Source_img/" + str(index) + "_1.jpg")
    unavailable_res = cv2.matchTemplate(skill_num_img, unavailable_img, cv2.TM_CCOEFF_NORMED)
    unavailable_confidence = np.max(unavailable_res)

    return available_confidence > unavailable_confidence


def spelling_check():
    bbox = (1072, 822, 1080, 850)
    spell_img = get_screenshot(bbox)
    # cv2.imshow('target_area', spell_img)
    # cv2.imwrite("Source_img/spelling.jpg", spell_img)
    # cv2.waitKey(1)
    spell_temp_img = cv2.imread("Source_img/spelling.jpg")
    res = cv2.matchTemplate(spell_img, spell_temp_img, cv2.TM_CCOEFF_NORMED)
    confidence = np.max(res)
    return confidence > 0.8


if __name__ == '__main__':
    # print(find_target(dead=False))
    print(read_target_name())
    # print(find_target(dead=True,threshold=0.5))
