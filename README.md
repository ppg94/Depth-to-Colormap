# Depth-to-Colormap

> 深度图转伪彩色图像工具

## 📝 简介

Depth-to-Colormap 是一个简单高效的工具，用于将16位TIFF深度图转换为纯净的伪彩色图像和灰度深度图。此工具可用于可视化深度图，便于直观地理解和分析深度信息。

## ✨ 功能特点

- 将TIFF深度图转换为伪彩色图像
- 同时生成灰度深度图
- 支持多种颜色映射方案（如jet、plasma、viridis等）
- 可自定义深度范围
- 支持批量处理整个目录中的深度图
- 无边界，无颜色条的纯净输出图像

## 🔧 安装

### 依赖项

- Python 3.6+
- NumPy
- Matplotlib
- Pillow (PIL)

### 安装依赖

```bash
pip install numpy matplotlib pillow
```

## 📖 使用方法

### 命令行参数

```
python depth_to_colormap.py 输入路径 [选项]
```

#### 必选参数

- `input_path`: 输入的深度图路径或包含深度图的目录

#### 可选参数

- `--output_path`, `-o`: 输出的伪彩图路径或目录
- `--depth_output_path`, `-d`: 输出的灰度深度图路径或目录
- `--colormap`, `-c`: 使用的颜色映射，如jet、plasma、viridis等（默认：jet）
- `--min_depth`, `-min`: 深度最小值（默认：使用图像的最小值）
- `--max_depth`, `-max`: 深度最大值（默认：使用图像的最大值）

### 示例

#### 处理单个文件

```bash
python depth_to_colormap.py depth_image.tiff -o colormap_output.png -c plasma
```

#### 处理整个目录

```bash
python depth_to_colormap.py depth_images_directory -o output_directory -c viridis
```

#### 指定深度范围

```bash
python depth_to_colormap.py depth_image.tiff -min 10 -max 1000 -c jet
```

## 🌟 示例结果

输入深度图经过处理后，将生成两个输出文件：
1. 伪彩色图像：直观显示深度信息，使用所选颜色映射
2. 灰度深度图：深度信息的灰度表示

## 📝 代码示例

核心函数使用示例：

```python
from depth_to_colormap import depth_to_colormap

# 转换单个文件
colormap_path, grayscale_path = depth_to_colormap(
    'input_depth.tiff',          # 输入深度图路径
    'output_colormap.png',       # 输出伪彩图路径
    'output_grayscale.png',      # 输出灰度图路径
    colormap='plasma',           # 颜色映射方案
    min_depth=50,                # 深度最小值
    max_depth=1000               # 深度最大值
)
```

## 💻 使用OpenCV的简化版本

如果你想要单独地将深度图转换为伪彩图，项目还提供了一个基于OpenCV的简化版本`convert.py`。这个脚本特别适合快速批量处理深度图，且仅依赖OpenCV库。

### 功能特点
- 使用OpenCV的`applyColorMap`函数快速转换
- 默认使用PLASMA颜色映射
- 简单直接的批量处理功能

### 依赖项
- Python 3.6+
- OpenCV

### 安装依赖
```bash
pip install opencv-python
```

### 使用方法
1. 修改脚本中的`scr_dir`和`out_dir`变量来指定输入和输出目录
2. 运行脚本进行批处理
```bash
python convert.py
```

### 代码示例
```python
import cv2
import os

# 设置输入和输出目录
scr_dir = '输入目录路径'
out_dir = '输出目录路径'

# 确保输出目录存在
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

def convertdep():
    for idx, pic in enumerate(os.listdir(scr_dir)): 
        src_path = os.path.join(scr_dir, pic) 
        depth = cv2.imread(src_path, cv2.IMREAD_GRAYSCALE)  
        color_img = cv2.applyColorMap(depth, cv2.COLORMAP_PLASMA)
        cv2.imwrite(os.path.join(out_dir, f"{idx}.png"), color_img)

convertdep()
```

## 👨‍💻 作者

**ppg94**
- GitHub: [ppg94](https://github.com/ppg94)
- Bilibili: [做一名code_pro](https://space.bilibili.com/629403768?spm_id_from=333.1007.0.0)
