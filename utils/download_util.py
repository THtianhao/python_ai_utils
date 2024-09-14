import os
import hashlib
import requests
from requests.exceptions import RequestException
from urllib.parse import urlparse


def download_file(url, save_path_dir, expected_hash=None, hash_algorithm='sha256'):
    """
    下载文件到指定目录，并以URL中的文件名保存。

    :param url: 文件的下载链接
    :param save_path_dir: 文件保存的目录
    :param expected_hash: 期望的文件哈希值，用于验证文件完整性（可选）
    :param hash_algorithm: 哈希算法，默认为'sha256'
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

                # Initialize hash calculation
                hash_func = getattr(hashlib, hash_algorithm)()

                # Write file in binary mode
                with open(save_path, 'wb') as f:
                    total_size = int(response.headers.get('content-length', 0))
                    downloaded_size = 0

                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:  # Filter out keep-alive chunks
                            f.write(chunk)
                            hash_func.update(chunk)  # Update hash with the chunk
                            downloaded_size += len(chunk)
                            # Print download progress
                            progress = (downloaded_size / total_size) * 100 if total_size else 0
                            print(f"Downloading: {progress:.2f}% complete", end='\r')

                print(f"\nDownload complete. File saved to {save_path}")

                # Verify the file hash if expected_hash is provided
                if expected_hash:
                    file_hash = hash_func.hexdigest()
                    if file_hash != expected_hash:
                        print(f"Warning: File hash does not match. Expected {expected_hash}, got {file_hash}")
                        return None  # Return None if hash does not match
                    else:
                        print("File hash matches.")

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
