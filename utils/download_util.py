import os
import requests
from urllib.parse import urlparse
from requests.exceptions import RequestException


def download_file(url, save_path_dir):
    """
    下载文件到指定目录，并以URL中的文件名保存。

    :param url: 文件的下载链接
    :param save_path_dir: 文件保存的目录
    :return: 返回下载文件的完整路径
    """

    # Extract the file name from the URL
    file_name = os.path.basename(urlparse(url).path)
    save_path = os.path.join(save_path_dir, file_name)

    # Ensure the save directory exists
    os.makedirs(save_path_dir, exist_ok=True)

    # Check if the file already exists
    if not os.path.exists(save_path):
        print(f"File not found. Attempting to download from {url}...")
        try:
            # Download the file
            with requests.get(url, stream=True, timeout=10) as response:
                response.raise_for_status()  # Raise an error for bad status codes
                # Write file in binary mode
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:  # Filter out keep-alive chunks
                            f.write(chunk)
            print(f"Download complete. File saved to {save_path}")

        except RequestException as e:
            print(f"Error occurred during download: {e}")
            return None  # Return None if the download fails

        except IOError as e:
            print(f"File I/O error: {e}")
            return None  # Return None if file writing fails

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None  # Return None if any other unexpected error occurs

    else:
        print(f"File already exists at {save_path}")

    return save_path  # Return the complete file path

# 使用示例