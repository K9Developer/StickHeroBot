from ppadb.client import Client
import cv2
import numpy
import time

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [0, 0, 255]


def get_device(devices):
    return devices[0]


def take_screenshot(file, device):
    result = device.screencap()
    with open(file, "wb") as fp:
        fp.write(result)
    return file


def compare_arrays(arr1, arr2):
    for (val1, val2) in zip(arr1, arr2):
        if val1 != val2:
            return False
    return True


def filter_image(img):
    h, w, _ = img.shape
    y = int(h-h/3+109)
    crop_img = img[y:y+1, 100:100+w]
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    x, img = cv2.threshold(crop_img, 75, 255, cv2.THRESH_BINARY)
    return img


def get_press_length(file):
    img = cv2.imread(file)
    h, w, _ = img.shape

    img = filter_image(img)
    cv2.imwrite("filtered.png", img)
    press_length = 1

    was_white = False
    was_black = False
    curr_color = None
    for j in range(w):
        curr_color = img[0, j]

        if compare_arrays(curr_color, WHITE):
            was_white = True

        if compare_arrays(curr_color, BLACK):
            was_black = True

        # Switched from black tower to void
        if was_black and (type(curr_color) == numpy.ndarray and (not compare_arrays(curr_color, BLACK) or (compare_arrays(curr_color, BLACK) and was_white))):
            press_length += 1

        if curr_color[0] == 0 and curr_color[2] == 255 and press_length and was_black and was_white:
            break

    return press_length


def fix_pixel_length(pixels):
    prev = pixels
    if 550 > pixels > 500:
        pixels -= pixels//3.8
        print("550 > pixels > 500")

    elif 600 > pixels > 550:
        pixels -= pixels//3.3
        print("600 > pixels > 550")

    elif 700 > pixels > 600:
        pixels -= pixels//3.5
        print("700 > pixels > 600")

    elif 750 > pixels > 700:
        pixels -= pixels//5
        print("750 > pixels > 700")  # 1

    elif 800 > pixels > 760:
        pixels -= pixels//3.8
        print("800 > pixels > 750")  # 1

    elif 870 > pixels > 800:
        pixels -= pixels//4.2
        print("870 > pixels > 800")  # 1

    elif 900 > pixels > 870:
        pixels -= pixels//3.8
        print("900 > pixels > 870")  # 1

    elif 1000 > pixels > 900:
        pixels -= pixels//3.7
        print("1000 > pixels > 900")

    elif pixels > 1000:
        pixels -= pixels//3.5
        print("pixels > 1000")

    elif 400 < pixels < 450:
        pixels -= pixels//3
        print("450 < pixels < 500")

    elif 450 < pixels < 500:
        pixels -= pixels//4.5
        print("450 < pixels < 500")

    elif 500 > pixels > 400:
        pixels -= pixels//4.4
        print("500 > pixels < 400")

    elif 250 > pixels > 200:
        pixels -= pixels // 4
        print("250 > pixels > 200")

    elif 350 > pixels > 250:
        pixels -= pixels // 4.6
        print("350 > pixels > 250")

    elif 400 > pixels > 350:
        pixels -= pixels // 5
        print("400 > pixels > 350")

    elif 200 > pixels > 100:
        pixels -= pixels // 5
        print("200 > pixels > 100")

    else:
        pixels -= pixels // 5
        print("default pixels -= pixels // 3.5")

    print(f"Original distance: {int(prev)}")
    print(f"Fixed distance: {int(pixels)}")
    return int(pixels)


def press_long(pixels, device):
    device.shell(
        f"input touchscreen swipe 500 500 500 500 {fix_pixel_length(pixels)}")


def main():
    adb = Client(host="127.0.0.1", port=5037)
    devices = adb.devices()

    if not len(devices):
        print("No devices attached!")
        exit(1)

    device = get_device(devices)

    for i in range(10):
        file = take_screenshot("game_ss.png", device)
        press_length = get_press_length(file)
        press_long(press_length, device)
        print("------------------------\n")
        time.sleep(3.5)


if __name__ == "__main__":
    main()
