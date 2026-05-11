"""算法模块 - 颜色阈值分割与灰度阈值分割的纯函数实现"""

import cv2
import numpy as np


def color_threshold_seg(image, h_range, s_range, v_range):
    """
    颜色阈值分割（HSV 空间）

    参数:
        image:   BGR 格式图像 (numpy array)
        h_range: (low, high) 色相范围 0~360
        s_range: (low, high) 饱和度范围 0~100 (%)
        v_range: (low, high) 明度范围 0~100 (%)

    返回:
        BGR 格式的结果图像，掩膜区域保留原图，其余区域置黑
    """
    if image is None:
        return None

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 将用户友好的范围映射到 OpenCV HSV 实际存储范围
    # H: 0~360 -> 0~179,  S: 0~100 -> 0~255,  V: 0~100 -> 0~255
    lower = np.array([
        int(h_range[0] / 2),
        int(s_range[0] * 255 / 100),
        int(v_range[0] * 255 / 100)
    ], dtype=np.uint8)

    upper = np.array([
        int(h_range[1] / 2),
        int(s_range[1] * 255 / 100),
        int(v_range[1] * 255 / 100)
    ], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(image, image, mask=mask)
    return result


def gray_threshold_seg(image, low, high, mode='inside'):
    """
    灰度图像灰阶过滤分割

    参数:
        image: BGR 格式图像 (numpy array)
        low:   低阈值 (0~255)
        high:  高阈值 (0~255)
        mode:  'inside' 保留区间内为白色 / 'outside' 保留区间外为白色

    返回:
        BGR 格式的二值图像
    """
    if image is None:
        return None

    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    if mode == 'inside':
        mask = cv2.inRange(gray, low, high)
    else:
        mask_low = cv2.threshold(gray, low, 255, cv2.THRESH_BINARY_INV)[1]
        mask_high = cv2.threshold(gray, high, 255, cv2.THRESH_BINARY)[1]
        mask = cv2.bitwise_and(mask_low, mask_high)

    result = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    return result
