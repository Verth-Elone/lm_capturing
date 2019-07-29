"""
https://github.com/agiledots/multiscale-template-matching/blob/master/match.py
"""
import imutils
from PIL import ImageGrab, Image, ImageOps
import win32gui
import pytesseract
import cv2 as cv
import numpy as np
import os

UNITS = (
    "Ancient Drake Rider",
    "Archer",
    "Cataphract",
    "Catapult",
    "Destroyer",
    "Fire Trebuchet",
    "Gladiator",
    "Grunt",
    "Heroic Cannoneer",
    "Heroic Fighter",
    "Reptilian Rider",
    "Royal Cavalry",
    "Royal Guard",
    "Sharpshooter",
    "Stealth Sniper"
)


def find_one_template_in_image(template_path: str, image_path: str):
    img_rgb = cv.imread(image_path)
    if img_rgb.shape[0] > 719:
        img_rgb = imutils.resize(img_rgb, height=719)
        # cv.imshow("Image", img_rgb)
        # cv.waitKey(0)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_RGB2GRAY)
    ## IF DISABLED, it's very fast
    #img_gray = cv.fastNlMeansDenoising(img_gray, h=25)
    #inv_img = ImageOps.invert(Image.fromarray(img_gray).convert('L'))
    #inv_img.format = "BMP"
    #img_gray = np.asarray(inv_img, dtype=np.uint8)

    # print(template_path)
    template = cv.imread(template_path, 0)  # read in greyscale
    template = cv.Canny(template, 10, 50)
    (tH, tW) = template.shape[:2]

    gray = img_gray
    resized = imutils.resize(
        gray, width=int(gray.shape[1])
    )
    r = gray.shape[1] / float(resized.shape[1])

    edged = cv.Canny(resized, 10, 50)
    result = cv.matchTemplate(edged, template, cv.TM_CCOEFF)
    (_, maxVal, _, maxLoc) = cv.minMaxLoc(result)

    start = (int(maxLoc[0] * r), int(maxLoc[1] * r))
    end = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

    cv.rectangle(img_rgb, start, end, (0, 0, 255), 1)
    # cv.imshow("Image", img_rgb)
    # cv.waitKey(0)

    return (img_rgb, img_gray), start, end


def crop(imgs, start, end):
    """
    :param imgs: tuple of rgb and gray image np array
    :param start: tuple of coordinates of start point
    :param end: tuple of coordinates of end point
    :return:
    """

    cv.rectangle(
        imgs[0],
        start,
        end,
        (255, 0, 0),
        1
    )
    # cv.imshow("Image", imgs[0])
    # cv.waitKey(0)

    img_copy = Image.fromarray(imgs[1])
    # print(img_copy.size, start, end)
    img_crop = img_copy.crop((start[0], start[1], end[0], end[1]))
    img_crop.format = 'BMP'
    return img_crop


def save_screenshot(window_name: str, save_path: str = r'.\test.png') -> None:
    toplist, winlist = [], []

    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

    win32gui.EnumWindows(enum_cb, toplist)
    window = [
        (hwnd, title) for hwnd, title in winlist
        if window_name in title.lower()
    ]
    # just grab the hwnd for first window matching window
    window = window[0]
    hwnd = window[0]

    win32gui.SetForegroundWindow(hwnd)
    bbox = win32gui.GetWindowRect(hwnd)
    ImageGrab.grab(bbox).save(save_path)


test_imgs = [
    r'test.png',  # doesn't find Heroic Fighter
    r'.\img\scout_report\rep_from_line_1.jpg',  # one $ sign instead of 5
    r'.\img\scout_report\report_2.png',
    r'.\img\scout_report\157371.jpg',
    r'.\img\scout_report\37984.jpg',
    r'.\img\scout_report\71403.jpg',  # doesn't find Ancient Drake Rider
    r'.\img\scout_report\S__24158211.jpg'  # doesn't find many
]

if __name__ == '__main__':
    """The problem is in aspect ratio for sure
    
    write some tests!
    """
    #save_screenshot('bluestacks', 'test.png')
    print("=" * 40)
    for main_img in test_imgs:

        star = find_one_template_in_image(r'.\img\star_1.png', main_img)
        star_x = star[2][0]
        cross = find_one_template_in_image(r'.\img\cross_1.png', main_img)
        cross_x = cross[1][0]

        units_from_ocr = {}

        for temp_img in [
            os.path.join(r'.\img\scout_report\troops', f) for f in
            os.listdir(r'.\img\scout_report\troops') if
            os.path.isfile(os.path.join(r'.\img\scout_report\troops', f))
        ]:
            match = find_one_template_in_image(temp_img, main_img)
            img = crop(
                match[0],
                (match[2][0], match[1][1]),
                (star_x + (cross_x - star_x)//2 + 20, match[2][1] + 2)
            )
            s = pytesseract.image_to_string(img, lang='eng+fra')
            tokens_ocr = s.lower().replace('\n', ' ').replace(',', '').split(' ')
            for unit in UNITS:
                tokens_unit = unit.lower().split(' ')
                all_tokens_match = True
                # print(tokens_unit, '\n', tokens_ocr)
                for u_token in tokens_unit:
                    if u_token not in tokens_ocr:
                        all_tokens_match = False
                    else:
                        pass
                if all_tokens_match:
                    units_from_ocr[unit] = tokens_ocr[-1]

        print(f'Finalized analysing image: {main_img}')

        for k, v in units_from_ocr.items():
            print(k, v)
        print("=" * 40)
