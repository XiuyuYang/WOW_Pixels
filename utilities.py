import cv2
import numpy as np
import os
import win32con
import win32gui
import win32ui
from PIL import ImageGrab


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    is_exists = os.path.exists(path)
    # 判断结果
    if not is_exists:
        # 如果不存在则创建目录1
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False


def set_foreground():
    hwnd = win32gui.FindWindow(None, '魔兽世界')
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)


def get_screenshot(bbox):
    img = ImageGrab.grab(bbox=bbox)  # x, y, w, h
    img_np = np.array(img)
    return cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)


def angle(v1, v2):
    x1, y1 = v1
    x2, y2 = v2
    dot = x1 * x2 + y1 * y2
    det = x1 * y2 - y1 * x2
    theta = np.arctan2(det, dot)
    theta = theta if theta > 0 else 2 * np.pi + theta
    return theta * 180 / np.pi
