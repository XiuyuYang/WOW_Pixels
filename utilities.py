import os

import cv2
from PIL import ImageGrab
import numpy as np
import win32con

import win32gui
import win32ui



def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
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

def get_screenshot(w,h):
    # define your monitor width and height
    # w, h = 1920, 1080

    # for now we will set hwnd to None to capture the primary monitor
    #hwnd = win32gui.FindWindow(None, window_name)
    hwnd = None

    # get the window image data
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)

    # convert the raw data into a format opencv can read
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)

    # free resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    # drop the alpha channel to work with cv.matchTemplate()
    img = img[...,:3]

    # make image C_CONTIGUOUS to avoid errors with cv.rectangle()
    img = np.ascontiguousarray(img)

    return img

def get_screenshot(bbox):
    img = ImageGrab.grab(bbox=bbox)  # x, y, w, h
    img_np = np.array(img)
    return cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)