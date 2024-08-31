import hashlib
import os
import shutil

MAX_SIZE = 1024

def is_image_file(filename):
    # 检查文件是否是图片文件（可以根据需要添加更多的图片格式）
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    return any(filename.lower().endswith(ext) for ext in image_extensions)

def calculate_hash(file_path):
    sha1_hash = hashlib.sha1()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha1_hash.update(chunk)
    return sha1_hash.hexdigest()

def traverse_folder_for_images(folder_path):
    output_path = folder_path + '_out'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    image_files = []
    # 遍历文件夹及其所有子文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.startswith("._"):
                continue
            file_path = os.path.join(root, file)
            if is_image_file(file):
                old_path = os.path.join(root, file)
                file_extension = os.path.splitext(file)[1]
                file_hash = calculate_hash(old_path)
                new_filename = file_hash + file_extension
                new_path = os.path.join(output_path, new_filename)
                try:
                    shutil.copy2(old_path, new_path)
                    print(f"文件已成功复制：{file} -> {new_path}")
                except Exception as e:
                    print(f"复制文件时发生错误：{e}")
                image_files.append(file_path)

    return image_files

if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("Usage: python resize_images.py <input_directory> <output_directory>")
    #     sys.exit(1)
    #
    # input_directory = sys.argv[1]
    # output_directory = sys.argv[2]
    #
    # if not os.path.isdir(input_directory):
    #     print("Invalid input directory.")
    #     sys.exit(1)
    # process_image("/Volumes/HIKSEMI/third_filter", "/Volumes/HIKSEMI/third_filter_out")

    traverse_folder_for_images("/Volumes/HIKSEMI/third_filter")
