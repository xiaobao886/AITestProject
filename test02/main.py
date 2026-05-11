"""图像处理工具箱 - 入口文件"""

import sys
import os


def resource_path(relative_path):
    """获取资源文件的绝对路径，兼容 PyInstaller 打包"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QFont
    from ui_mainwindow import MainWindow

    app = QApplication(sys.argv)

    # 全局字体
    font = QFont('Microsoft YaHei', 9)
    app.setFont(font)

    # 全局样式
    app.setStyleSheet('''
        QMainWindow {
            background-color: #f8f9fa;
        }
        QDialog {
            background-color: #f8f9fa;
        }
        QGroupBox {
            border: 1px solid #ddd;
            border-radius: 6px;
            margin-top: 10px;
            padding-top: 16px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 6px;
        }
        QSlider::groove:horizontal {
            height: 6px;
            background: #ddd;
            border-radius: 3px;
        }
        QSlider::handle:horizontal {
            background: #4A90D9;
            width: 16px;
            margin: -5px 0;
            border-radius: 8px;
        }
        QSlider::sub-page:horizontal {
            background: #4A90D9;
            border-radius: 3px;
        }
    ''')

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
