import os

import requests

def download_image(save_dir, url):
    """下载图片并返回文件路径"""
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    local_filename = os.path.join(save_dir, url.split('/')[-1])
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    except Exception as e:
        print(f'download image fail {e}')

    return local_filename

def get_file_size(file_path):
    """读取文件大小"""
    return os.path.getsize(file_path)
