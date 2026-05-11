# 图像处理工具箱 - 算法聚合器

一个基于 Python + PyQt5 + OpenCV 开发的图像处理工具，集成了多种常规图像分割算法，通过 PyInstaller 打包为独立 EXE 文件，用户无需安装任何环境即可直接使用。

---

## 项目结构

`
D:\AITestProject\test02\
├── main.py                 # 程序入口，启动 QApplication
├── image_utils.py          # OpenCV 与 PyQt5 图像格式互转工具
├── algorithms.py           # 颜色阈值分割 & 灰度阈值分割算法实现
├── ui_mainwindow.py        # 主窗口界面
├── ui_color_dialog.py      # 颜色阈值分割对话框（HSV）
├── ui_gray_dialog.py       # 灰度阈值分割对话框
├── requirements.txt        # Python 依赖清单
├── build_exe.bat           # 一键打包脚本
├── README.md               # 项目说明文档
├── resources/
│   └── sample.jpg          # 默认示例图片（自动生成）
├── dist/
│   └── ImageTool.exe       # 打包后的可执行文件（~86MB）
├── build/                  # PyInstaller 构建临时目录
└── ImageTool.spec          # PyInstaller 打包配置
`

---

## 功能说明

### 主界面
- 窗口标题：**图像处理工具箱 - 算法聚合器**
- 提供 3 个操作按钮：
  - **🎨 颜色阈值分割** — 打开 HSV 颜色阈值分割对话框
  - **🖤 灰度阈值分割** — 打开灰度阈值分割对话框
  - **退出** — 关闭程序
- 底部状态栏实时显示操作提示

### 算法1：颜色阈值分割（HSV 空间）

基于 HSV 色彩空间进行颜色阈值分割，适用于颜色目标提取和光照不变性处理。

| 参数 | 范围 | 含义 |
|------|------|------|
| 色相 H | 0 ~ 360 | 色相角度，0=红, 120=绿, 240=蓝 |
| 饱和度 S | 0 ~ 100% | 色彩纯度，0%=灰色, 100%=纯色 |
| 明度 V | 0 ~ 100% | 亮度强度，0%=黑色, 100%=最亮 |

**处理流程：**
1. 将原图从 BGR 转换到 HSV 色彩空间
2. 界面上的 H/S/V 值自动映射到 OpenCV 内部范围（H→0-179, S→0-255, V→0-255）
3. 使用 `cv2.inRange` 根据滑块范围生成二值掩膜
4. 掩膜区域保留原图颜色，其余区域置黑
5. 输出 RGB 彩色结果图

**典型应用场景：**
- 通过 H 范围提取特定颜色物体（如提取红色物体：H 0~10 和 350~360）
- 通过 S 阈值过滤灰色区域，只保留彩色区域
- 通过 V 通道分离亮度影响，实现光照不变性处理

### 算法2：灰度阈值分割

| 参数 | 范围 | 含义 |
|------|------|------|
| 低阈值 | 0 ~ 255 | 灰度下界，默认 50 |
| 高阈值 | 0 ~ 255 | 灰度上界，默认 200 |
| 二值化模式 | 二选一 | "保留区间内为白色" / "保留区间外为白色" |

**处理流程：**
1. 若原图为彩色，自动转为灰度图
2. 根据阈值范围和所选模式生成二值掩膜
3. 输出黑白二值图像（白色为保留部分，黑色为其他）

### 通用交互功能

- **打开图像**：点击按钮选择本地图片（支持 PNG、JPG、JPEG、BMP、TIF、TIFF）
- **拖拽加载**：将图片文件拖拽到原始图像区域即可替换
- **确认处理**：点击后执行算法，显示处理结果，状态栏显示处理耗时
- **保存结果**：将处理结果保存为 PNG 或 JPG 文件
- **默认示例图**：对话框打开时自动加载内置的 `resources/sample.jpg`
- **固定窗口尺寸**：原图和结果图区域固定为 480×360，图片自动等比缩放适配

---

## 环境要求

### 最终用户（使用 EXE）

| 项目 | 要求 |
|------|------|
| 操作系统 | Windows 10 / 11（64 位） |
| 运行时依赖 | **无** — 双击 `ImageTool.exe` 即可运行 |
| 磁盘空间 | 约 86 MB（单个 EXE 文件） |
| 首次启动 | 约需 5~10 秒解压临时文件，后续启动更快 |

> **注意：** 若启动时弹出缺少 `VCRUNTIME140.dll` 等错误，需安装 [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)（Windows 10/11 通常已自带）。

### 开发者（源码开发与重新打包）

| 项目 | 要求 |
|------|------|
| 操作系统 | Windows 10 / 11（64 位） |
| Python | 3.10 ~ 3.12（推荐 3.10 或 3.11） |

**Python 依赖（requirements.txt）：**

`
pyqt5
opencv-python
numpy
pyinstaller
`

**安装依赖：**

`
pip install -r requirements.txt
`

---

## 使用方式

### 方式一：直接运行 EXE（推荐普通用户）

1. 找到 `D:\AITestProject\test02\dist\ImageTool.exe`
2. 双击运行
3. 选择一个算法开始处理图像

### 方式二：源码运行（开发者调试）

`
cd D:\AITestProject\test02
python main.py
`

### 方式三：重新打包 EXE

**使用一键脚本：**

`
cd D:\AITestProject\test02
build_exe.bat
`

**或手动执行：**

`
pyinstaller --onefile --windowed --add-data "resources;resources" --name "ImageTool" --clean main.py
`

打包完成后，EXE 位于 `dist/ImageTool.exe`。

---

## 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| 编程语言 | Python 3.12 | 开发快速，库生态丰富 |
| GUI 框架 | PyQt5 | 跨平台界面，布局灵活，打包成熟 |
| 图像处理 | OpenCV-Python | 色彩空间转换、阈值分割、图像IO |
| 数值计算 | NumPy | 高效数组运算 |
| 打包工具 | PyInstaller 6.x | --onefile 生成单个独立 EXE |

---

## 扩展新算法

项目采用模块化 MVC 设计，新增算法只需三步：

1. **实现算法函数** — 在 `algorithms.py` 中添加新函数，输入 BGR 图像，输出 BGR 图像
2. **创建对话框** — 新建 `ui_xxx_dialog.py`，继承 `QDialog`，设计该算法的参数控件和布局
3. **主窗口添加按钮** — 在 `ui_mainwindow.py` 中添加按钮并连接到打开新对话框的方法

---

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| EXE 体积较大（~86MB） | 包含了 PyQt5 + Qt5 + OpenCV 全部依赖，属正常范围 |
| 首次启动慢（5~10秒） | PyInstaller 打包的程序首次运行需解压到临时目录，后续会更快 |
| 缺少 VCRUNTIME140.dll | 安装 Microsoft Visual C++ Redistributable |
| 滑块参数较多，布局紧凑 | 参数区域使用 QGroupBox + QGridLayout 组织，界面整洁 |

---

## 打包信息

| 项目 | 值 |
|------|-----|
| 打包日期 | 2026-05-07 |
| PyInstaller 版本 | 6.20.0 |
| Python 版本 | 3.12.10 (conda) |
| EXE 文件大小 | ~86 MB |
| EXE 位置 | `dist/ImageTool.exe` |
| 打包模式 | --onefile --windowed（单文件、无控制台窗口） |
