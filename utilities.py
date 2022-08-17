import cv2
import numpy as np
import win32gui
from PIL import ImageGrab


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


if __name__ == '__main__':
    print(get_delta_angle(340, 10))
