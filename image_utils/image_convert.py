import numpy as np
import cv2
import io
from fastapi import UploadFile


def byte_to_cv2_image(image_bytes: bytes):
    """
    将 UploadFile 转换为 OpenCV 图像 (cv2.Mat).

    :param file: FastAPI 的 UploadFile 对象
    :return: OpenCV 格式的图像 (cv2.Mat)
    """

    # 将字节流转换为 OpenCV 格式的图像
    np_arr = np.frombuffer(image_bytes, np.uint8)
    cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if cv_image is None:
        raise ValueError("Failed to decode image to OpenCV format")

    return cv_image


def byte_to_pil_image(image_bytes: bytes):
    from PIL import Image
    """
    将 UploadFile 转换为 Pillow 图像 (PIL.Image).

    :param file: FastAPI 的 UploadFile 对象
    :return: Pillow 格式的图像 (PIL.Image)
    """

    # 将字节流转换为 Pillow 格式的图像
    pil_image = Image.open(io.BytesIO(image_bytes))
    return pil_image


def byte_to_ndarray(image_bytes: bytes):
    """
    将 UploadFile 转换为 NumPy 数组 (ndarray).

    :param file: FastAPI 的 UploadFile 对象
    :return: NumPy 数组格式的图像 (ndarray)
    """
    # 先将文件转换为 Pillow 图像
    pil_image = byte_to_pil_image(image_bytes)

    # 将 Pillow 图像转换为 NumPy 数组
    np_image = np.array(pil_image)
    return np_image

