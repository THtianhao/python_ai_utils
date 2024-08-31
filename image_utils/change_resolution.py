import os

import cv2

# Change the resolution of the image according to the ratio and copy the result to another folder,And recursively all subfolders, and subfolders of subfolders
def change_resolution(input_folder, output_folder, ratio):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".JPG") or file.endswith(".png") or file.endswith(".jpeg"):
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_folder, file)
                img = cv2.imread(input_path)
                if img is None:
                    continue
                height, width, _ = img.shape
                new_height= int(height * ratio)
                new_width = int(width * ratio)
                img = cv2.resize(img, (new_width, new_height))
                cv2.imwrite(output_path, img)
                print(f"{input_path} -> {output_path}")




if __name__ == '__main__':
    change_resolution("/Volumes/HIKSEMI/image/拍摄过滤", "/Volumes/HIKSEMI/外模精修低分辨率", 1/4)
