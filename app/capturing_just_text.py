# Copyright (c) Peter Majko.

"""

"""

from PIL import Image, ImageOps
import pytesseract
import cv2 as cv
import numpy as np


image_path = r'test_3.png'

img_rgb = cv.imread(image_path)
img_gray = cv.cvtColor(img_rgb, cv.COLOR_RGB2GRAY)
img_gray = cv.fastNlMeansDenoising(img_gray, h=25)
inv_img = ImageOps.invert(Image.fromarray(img_gray).convert('L'))
inv_img.format = "BMP"
# img_gray = np.asarray(inv_img, dtype=np.uint8)
# img_gray

s = pytesseract.image_to_string(inv_img, lang='eng+fra')
print(s)
# print(s.replace('\n', ' ').replace(',', '').split(' '))
print("=" * 40)
