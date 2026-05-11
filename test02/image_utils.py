"""图像格式转换工具模块 - OpenCV 与 PyQt5 之间的图像互转"""

import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap


def cv2_to_qpixmap(cv_img):
    """将 OpenCV BGR 格式的图像转换为 QPixmap，用于 Qt 控件显示"""
    if cv_img is None:
        return QPixmap()

    if len(cv_img.shape) == 2:
        # 灰度图
        h, w = cv_img.shape
        bytes_per_line = w
        q_img = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
    elif cv_img.shape[2] == 3:
        # BGR -> RGB
        rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_img.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
    elif cv_img.shape[2] == 4:
        # BGRA -> RGBA
        rgba_img = cv2.cvtColor(cv_img, cv2.COLOR_BGRA2RGBA)
        h, w, ch = rgba_img.shape
        bytes_per_line = ch * w
        q_img = QImage(rgba_img.data, w, h, bytes_per_line, QImage.Format_RGBA8888)
    else:
        return QPixmap()

    return QPixmap.fromImage(q_img.copy())


def qpixmap_to_cv2(pixmap):
    """将 QPixmap 转换为 OpenCV BGR 格式的 numpy 数组"""
    if pixmap.isNull():
        return None

    q_img = pixmap.toImage()

    if q_img.format() == QImage.Format_RGB888:
        # RGB -> BGR
        w, h = q_img.width(), q_img.height()
        ptr = q_img.bits()
        ptr.setsize(h * w * 3)
        arr = np.frombuffer(ptr, dtype=np.uint8).reshape((h, w, 3))
        return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
    elif q_img.format() == QImage.Format_Grayscale8:
        w, h = q_img.width(), q_img.height()
        ptr = q_img.bits()
        ptr.setsize(h * w)
        arr = np.frombuffer(ptr, dtype=np.uint8).reshape((h, w))
        return cv2.cvtColor(arr, cv2.COLOR_GRAY2BGR)
    else:
        # 统一转换到 Format_RGB888 再处理
        q_img = q_img.convertToFormat(QImage.Format_RGB888)
        w, h = q_img.width(), q_img.height()
        ptr = q_img.bits()
        ptr.setsize(h * w * 3)
        arr = np.frombuffer(ptr, dtype=np.uint8).reshape((h, w, 3))
        return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)


def fit_pixmap_to_label(pixmap, label):
    """将 QPixmap 等比缩放以适应 QLabel 的尺寸"""
    if pixmap.isNull():
        return pixmap
    return pixmap.scaled(label.size(), aspectRatioMode=1, transformMode=1)  # KeepAspectRatio + SmoothTransformation
