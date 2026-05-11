"""灰度阈值分割对话框"""

import sys
import os
import time
import cv2
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSlider, QGroupBox, QGridLayout, QFileDialog,
    QSplitter, QFrame, QMessageBox, QRadioButton, QButtonGroup
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from image_utils import cv2_to_qpixmap, fit_pixmap_to_label
from algorithms import gray_threshold_seg


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)


class GraySegDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('灰度阈值分割')
        self.setMinimumSize(960, 580)
        self.resize(1100, 650)
        self._source_img = None  # BGR
        self._result_img = None  # BGR
        self._init_ui()
        self._load_default_image()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)

        # === 上部：图像显示区 ===
        img_splitter = QSplitter(Qt.Horizontal)

        # 原图
        orig_frame = QFrame()
        orig_layout = QVBoxLayout(orig_frame)
        orig_title = QLabel('原始图像')
        orig_title.setAlignment(Qt.AlignCenter)
        orig_title.setFont(QFont('Microsoft YaHei', 11, QFont.Bold))
        self.label_orig = QLabel('加载中...')
        self.label_orig.setAlignment(Qt.AlignCenter)
        self.label_orig.setFixedSize(480, 360)
        self.label_orig.setStyleSheet('border: 2px dashed #ccc; background: #f5f5f5;')
        self.label_orig.setAcceptDrops(True)
        self.label_orig.dragEnterEvent = self._drag_enter
        self.label_orig.dropEvent = self._drop_event
        orig_layout.addWidget(orig_title)
        orig_layout.addWidget(self.label_orig)

        # 结果图
        result_frame = QFrame()
        result_layout = QVBoxLayout(result_frame)
        result_title = QLabel('处理结果')
        result_title.setAlignment(Qt.AlignCenter)
        result_title.setFont(QFont('Microsoft YaHei', 11, QFont.Bold))
        self.label_result = QLabel('等待处理...')
        self.label_result.setAlignment(Qt.AlignCenter)
        self.label_result.setFixedSize(480, 360)
        self.label_result.setStyleSheet('border: 2px dashed #ccc; background: #f5f5f5;')
        result_layout.addWidget(result_title)
        result_layout.addWidget(self.label_result)

        img_splitter.addWidget(orig_frame)
        img_splitter.addWidget(result_frame)
        main_layout.addWidget(img_splitter, stretch=1)

        # === 下部：参数面板 ===
        param_group = QGroupBox('参数设置')
        param_group.setFont(QFont('Microsoft YaHei', 10))
        param_layout = QGridLayout(param_group)

        # 低阈值
        param_layout.addWidget(QLabel('低阈值:'), 0, 0)
        self.slider_low = QSlider(Qt.Horizontal)
        self.slider_low.setRange(0, 255)
        self.slider_low.setValue(50)
        self.label_low_val = QLabel('50')
        self.label_low_val.setMinimumWidth(30)
        self.slider_low.valueChanged.connect(lambda v: self.label_low_val.setText(str(v)))
        param_layout.addWidget(self.slider_low, 0, 1, 1, 2)
        param_layout.addWidget(self.label_low_val, 0, 3)

        # 高阈值
        param_layout.addWidget(QLabel('高阈值:'), 1, 0)
        self.slider_high = QSlider(Qt.Horizontal)
        self.slider_high.setRange(0, 255)
        self.slider_high.setValue(200)
        self.label_high_val = QLabel('200')
        self.slider_high.valueChanged.connect(lambda v: self.label_high_val.setText(str(v)))
        param_layout.addWidget(self.slider_high, 1, 1, 1, 2)
        param_layout.addWidget(self.label_high_val, 1, 3)

        # 二值化模式
        param_layout.addWidget(QLabel('二值化模式:'), 2, 0)
        self.radio_inside = QRadioButton('保留区间内为白色')
        self.radio_outside = QRadioButton('保留区间外为白色')
        self.radio_inside.setChecked(True)
        self.btn_group = QButtonGroup(self)
        self.btn_group.addButton(self.radio_inside, 0)
        self.btn_group.addButton(self.radio_outside, 1)

        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.radio_inside)
        mode_layout.addWidget(self.radio_outside)
        param_layout.addLayout(mode_layout, 2, 1, 1, 3)

        main_layout.addWidget(param_group)

        # === 按钮栏 ===
        btn_layout = QHBoxLayout()
        btn_style = '''
            QPushButton {
                background-color: #4A90D9; color: white; border: none;
                border-radius: 6px; padding: 10px 20px; font-size: 14px;
                font-family: 'Microsoft YaHei';
            }
            QPushButton:hover { background-color: #357ABD; }
        '''
        btn_open = QPushButton('📂 打开图像')
        btn_open.setStyleSheet(btn_style)
        btn_open.clicked.connect(self._open_image)

        btn_process = QPushButton('✅ 确认处理')
        btn_process.setStyleSheet(btn_style.replace('#4A90D9', '#5CB85C').replace('#357ABD', '#449D44'))
        btn_process.clicked.connect(self._process)

        btn_save = QPushButton('💾 保存结果')
        btn_save.setStyleSheet(btn_style.replace('#4A90D9', '#F0AD4E').replace('#357ABD', '#EC971F'))
        btn_save.clicked.connect(self._save_result)

        self.label_time = QLabel('')
        self.label_time.setStyleSheet('color: #888;')

        btn_layout.addWidget(btn_open)
        btn_layout.addWidget(btn_process)
        btn_layout.addWidget(btn_save)
        btn_layout.addStretch()
        btn_layout.addWidget(self.label_time)
        main_layout.addLayout(btn_layout)

    def _load_default_image(self):
        path = resource_path('resources/sample.jpg')
        if os.path.exists(path):
            self._source_img = cv2.imread(path)
            self._display_orig()
        else:
            self.label_orig.setText('未找到默认图片\n请点击"打开图像"')

    def _display_orig(self):
        if self._source_img is not None:
            pm = cv2_to_qpixmap(self._source_img)
            self.label_orig.setPixmap(fit_pixmap_to_label(pm, self.label_orig))

    def _open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择图像', '',
            'Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff);;All Files (*)'
        )
        if file_path:
            img = cv2.imread(file_path)
            if img is not None:
                self._source_img = img
                self._result_img = None
                self._display_orig()
                self.label_result.clear()
                self.label_result.setText('等待处理...')
            else:
                QMessageBox.warning(self, '错误', '无法加载图像文件。')

    def _drag_enter(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def _drop_event(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile().lower()
            if file_path.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')):
                img = cv2.imread(urls[0].toLocalFile())
                if img is not None:
                    self._source_img = img
                    self._result_img = None
                    self._display_orig()
                    self.label_result.clear()
                    self.label_result.setText('等待处理...')

    def _process(self):
        if self._source_img is None:
            QMessageBox.warning(self, '提示', '请先加载一张图像。')
            return

        low = self.slider_low.value()
        high = self.slider_high.value()
        mode = 'inside' if self.radio_inside.isChecked() else 'outside'

        t0 = time.time()
        self._result_img = gray_threshold_seg(self._source_img, low, high, mode)
        elapsed = (time.time() - t0) * 1000

        if self._result_img is not None:
            pm = cv2_to_qpixmap(self._result_img)
            self.label_result.setPixmap(fit_pixmap_to_label(pm, self.label_result))
            self.label_time.setText(f'处理耗时: {elapsed:.1f} ms')

    def _save_result(self):
        if self._result_img is None:
            QMessageBox.warning(self, '提示', '请先执行处理。')
            return
        file_path, _ = QFileDialog.getSaveFileName(
            self, '保存结果', 'result_gray.png',
            'PNG (*.png);;JPEG (*.jpg);;All Files (*)'
        )
        if file_path:
            cv2.imwrite(file_path, self._result_img)
            QMessageBox.information(self, '成功', f'结果已保存至:\n{file_path}')

