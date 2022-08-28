import time

import cv2
import keyboard
import easyocr
import mouse
import numpy as np
import win32gui
from PIL import ImageGrab

reader = easyocr.Reader(['ch_sim'])


def set_foreground():
    hwnd = win32gui.FindWindow(None, '魔兽世界')
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)


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


def find_target(dead=False, threshold=0.75, skip=[]):
    bbox = (300, 52, 450, 90)
    target_area_img = get_screenshot(bbox)
    confidence_dead = compair_imgs("Source_img/dead.jpg", target_area_img)
    if dead:
        print(confidence_dead)
        return confidence_dead > 0.5

    # yellow names
    confidence1 = compair_imgs("Source_img/Target_1.jpg", target_area_img)
    # red names
    confidence2 = compair_imgs("Source_img/Target_2.jpg", target_area_img)
    # print(confidence1,confidence2)
    if confidence1 > threshold or confidence2 > threshold:
        name = read_target_name()
        if name:
            for i in skip:
                if i in name:
                    print("skip target:", name)
                    return False
            return True
        else:
            print("target name read error.")
            return True
        # return True
    else:
        return False


def read_target_name():
    bbox = (300, 52, 450, 90)
    target_area_img = get_screenshot(bbox)
    img = cv2.split(target_area_img)[1]
    try:
        result = reader.readtext(img)
    except:
        result = None
    if result:
        result = reader.readtext(img)[0][1]
        print(result)
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


def get_skill_img(index):
    size = 49.5 * (int(index) - 1)
    bbox = (367 + size, 998, 405 + size, 1012)
    skill_num_img = get_screenshot(bbox)
    # cv2.imshow(str(index), skill_num_img)
    # cv2.waitKey(1)
    return skill_num_img


def skill_in_range(index=1):
    skill_num_img = get_skill_num_img(index)
    # avaiable
    available_confidence = compair_imgs("Source_img/" + str(index) + "_0.jpg", skill_num_img)
    # unavailable
    unavailable_confidence = compair_imgs("Source_img/" + str(index) + "_1.jpg", skill_num_img)

    return available_confidence > unavailable_confidence


def compair_imgs(temp_img, target_img):
    if isinstance(temp_img, str):
        img = cv2.imread(temp_img)
    else:
        img = temp_img
    res = cv2.matchTemplate(target_img, img, cv2.TM_CCOEFF_NORMED)
    return np.max(res)


def compair_birghtness(img1, img2):
    all_value_1 = 0
    for i in img1:
        for j in i:
            all_value_1 += (sum(j))
    all_value_2 = 0
    for i in img2:
        for j in i:
            all_value_2 += (sum(j))
    result = all_value_2 / all_value_1
    return result > 0.7


def spelling_check():
    bbox = (1072, 822, 1080, 850)
    spell_img = get_screenshot(bbox)
    confidence = compair_imgs("Source_img/spelling.jpg", spell_img)
    return confidence > 0.8


def right_btn_pressed():
    return mouse.is_pressed("right")


def run_macro(macro_str):
    keyboard.press_and_release("enter")
    keyboard.write(macro_str)
    keyboard.press_and_release("enter")


def mount():
    keyboard.press_and_release("8")
    time.sleep(3)


if __name__ == '__main__':
    set_foreground()
    print()
