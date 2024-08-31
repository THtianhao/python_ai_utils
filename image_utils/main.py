# This is a sample Python script.
import os

import cv2

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

folder_path = "/Users/toto/Desktop/filter"
new_folder = "/Users/toto/Desktop/new_filter"

def bright(img, beta_value):
    img_bright = cv2.convertScaleAbs(img, beta=beta_value)
    return img_bright

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
    for index, filename in enumerate(os.listdir(folder_path)):
        end = filename.split('.')[-1]
        if end == "jpg" or end == "jpeg" or end == "png":
            image = cv2.imread(os.path.join(folder_path, filename))
            cv2.imwrite(os.path.join(new_folder, filename), bright(image, -20))
