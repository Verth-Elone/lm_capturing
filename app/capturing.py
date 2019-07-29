# Copyright (c) Peter Majko.

"""

"""
from PIL import ImageGrab, Image, ImageOps
import win32gui
import pytesseract
import cv2 as cv
import numpy as np
import os

toplist, winlist = [], []


def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))


win32gui.EnumWindows(enum_cb, toplist)
bluestacks = [(hwnd, title) for hwnd, title in winlist if 'bluestacks' in title.lower()]
print(bluestacks)
# just grab the hwnd for first window matching bluestacks
bluestacks = bluestacks[0]
hwnd = bluestacks[0]

win32gui.SetForegroundWindow(hwnd)
bbox = win32gui.GetWindowRect(hwnd)
img_rgb = ImageGrab.grab(bbox)
img_rgb.format = 'BMP'

# img.save('text.png')
# img.show()
# print(pytesseract.image_to_string(Image.open('text.png')))
# print(pytesseract.image_to_string(img_rgb))

img_np = np.asarray(img_rgb, dtype=np.uint8)
img_gray = cv.cvtColor(img_np, cv.COLOR_BGR2GRAY)

for temp_img in [
    os.path.join(r'.\img\scout_report\troops', f) for f in
    os.listdir(r'.\img\scout_report\troops') if
    os.path.isfile(os.path.join(r'.\img\scout_report\troops', f))
]:
    print(temp_img)
    template = cv.imread(temp_img, 0)  # read in greyscale

    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.90
    loc = np.where(res >= threshold)
    imgs = []

    for pt in zip(*loc[::-1]):
        cv.rectangle(
            img_np,
            (pt[0] + 30, pt[1]),
            (pt[0] + 520, pt[1] + 30),
            (255, 0, 0),
            1
        )
        imgs.append(
            Image.fromarray(cv.fastNlMeansDenoising(img_gray, h=20)).copy().crop(
                (pt[0] + 30, pt[1], pt[0] + 520, pt[1] + 30)
            )
        )
    for img in imgs:
        inv_img = ImageOps.invert(img.convert('L'))
        inv_img.format = "BMP"
        print(pytesseract.image_to_string(inv_img, lang='eng+fra'))
        print("="*40)

Image.fromarray(img_np).show()
input('~')
