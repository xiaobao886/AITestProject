"""主窗口模块"""

import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QStatusBar, QLabel, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

from ui_color_dialog import ColorSegDialog
from ui_gray_dialog import GraySegDialog


def resource_path(relative_path):
    """获取资源文件的绝对路径，兼容 PyInstaller 打包"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('图像处理工具箱 - 算法聚合器')
        self.setMinimumSize(420, 320)
        self.resize(480, 360)
        self._init_ui()

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setSpacing(16)
        layout.setContentsMargins(40, 30, 40, 30)

        # 标题
        title = QLabel('图像处理工具箱')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Microsoft YaHei', 18, QFont.Bold))
        layout.addWidget(title)

        subtitle = QLabel('选择一个算法开始处理图像')
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet('color: #888; font-size: 13px;')
        layout.addWidget(subtitle)

        layout.addSpacing(10)

        # 按钮样式
        btn_style = '''
            QPushButton {
                background-color: #4A90D9;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 14px;
                font-size: 15px;
                font-family: 'Microsoft YaHei';
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
            QPushButton:pressed {
                background-color: #2A6099;
            }
        '''
        exit_style = '''
            QPushButton {
                background-color: #999;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 14px;
                font-size: 15px;
                font-family: 'Microsoft YaHei';
            }
            QPushButton:hover {
                background-color: #777;
            }
        '''

        btn_color = QPushButton('🎨  颜色阈值分割')
        btn_color.setStyleSheet(btn_style)
        btn_color.setCursor(Qt.PointingHandCursor)
        btn_color.clicked.connect(self._open_color_seg)
        layout.addWidget(btn_color)

        btn_gray = QPushButton('🖤  灰度阈值分割')
        btn_gray.setStyleSheet(btn_style)
        btn_gray.setCursor(Qt.PointingHandCursor)
        btn_gray.clicked.connect(self._open_gray_seg)
        layout.addWidget(btn_gray)

        layout.addSpacing(10)

        btn_exit = QPushButton('退出')
        btn_exit.setStyleSheet(exit_style)
        btn_exit.setCursor(Qt.PointingHandCursor)
        btn_exit.clicked.connect(self.close)
        layout.addWidget(btn_exit)

        # 状态栏
        self.statusBar().showMessage('就绪 - 请选择一个算法')

    def _open_color_seg(self):
        self.statusBar().showMessage('正在打开颜色阈值分割...')
        dialog = ColorSegDialog(self)
        dialog.exec_()
        self.statusBar().showMessage('就绪 - 请选择一个算法')

    def _open_gray_seg(self):
        self.statusBar().showMessage('正在打开灰度阈值分割...')
        dialog = GraySegDialog(self)
        dialog.exec_()
        self.statusBar().showMessage('就绪 - 请选择一个算法')
