import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import argparse
import glob
import matplotlib

def depth_to_colormap(input_path, output_path=None, depth_output_path=None, colormap='jet', min_depth=None, max_depth=None):
    """
    参数:
        input_path: 输入的深度图路径
        output_path: 输出的伪彩图路径，如果为None则自动生成
        depth_output_path: 输出的灰度深度图路径，如果为None则与output_path相同
        colormap: 使用的颜色映射，默认为'jet'
        min_depth: 深度最小值，如果为None则使用图像的最小值
        max_depth: 深度最大值，如果为None则使用图像的最大值
    """
    # 读取深度图
    depth_img = np.array(Image.open(input_path))
    
    # 如果未指定深度范围，使用图像的最小/最大值
    if min_depth is None:
        min_depth = np.min(depth_img)
    if max_depth is None:
        max_depth = np.max(depth_img)
    
    # 将深度值归一化到0-1范围
    depth_normalized = np.clip((depth_img - min_depth) / (max_depth - min_depth), 0, 1)
    
    # 获取颜色映射对象
    cmap = plt.get_cmap(colormap)
    
    # 直接应用颜色映射
    colored_img = cmap(depth_normalized)
    
    # 转换为uint8 RGB图像（移除alpha通道）
    rgb_img = (colored_img[:, :, :3] * 255).astype(np.uint8)
    
    # 创建PIL图像
    pil_img = Image.fromarray(rgb_img)
    
    # 创建灰度深度图
    gray_img = (depth_normalized * 255).astype(np.uint8)
    pil_gray_img = Image.fromarray(gray_img, mode='L')
    
    # 确定输出路径
    base_name = os.path.basename(input_path)  # 获取文件名而不是路径
    name_no_ext = os.path.splitext(base_name)[0]
    
    if output_path is None:
        colormap_path = f"{name_no_ext}_colormap.png"
    else:
        # 如果output_path是目录，在该目录下创建文件
        if os.path.isdir(output_path):
            colormap_path = os.path.join(output_path, f"{name_no_ext}_colormap.png")
        else:
            colormap_path = output_path
    
    if depth_output_path is None:
        if output_path is None:
            grayscale_path = f"{name_no_ext}_grayscale.png"
        else:
            grayscale_path = os.path.splitext(colormap_path)[0] + "_grayscale.png"
    else:
        # 如果depth_output_path是目录，在该目录下创建文件
        if os.path.isdir(depth_output_path):
            grayscale_path = os.path.join(depth_output_path, f"{name_no_ext}_grayscale.png")
        else:
            grayscale_path = depth_output_path
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(colormap_path) if os.path.dirname(colormap_path) else '.', exist_ok=True)
    os.makedirs(os.path.dirname(grayscale_path) if os.path.dirname(grayscale_path) else '.', exist_ok=True)
    
    # 保存图像
    pil_img.save(colormap_path)
    pil_gray_img.save(grayscale_path)
    
    print(f"伪彩图已保存到: {colormap_path}")
    print(f"灰度深度图已保存到: {grayscale_path}")
    
    return colormap_path, grayscale_path

def process_directory(input_dir, output_dir, depth_output_dir=None, colormap='jet', min_depth=None, max_depth=None):
    """
    处理目录中的所有TIFF文件
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    if depth_output_dir:
        os.makedirs(depth_output_dir, exist_ok=True)
    
    # 获取所有TIFF文件
    tiff_files = glob.glob(os.path.join(input_dir, "*.tif")) + glob.glob(os.path.join(input_dir, "*.tiff"))
    
    if not tiff_files:
        print(f"在 {input_dir} 中没有找到TIFF文件")
        return
    
    print(f"找到 {len(tiff_files)} 个TIFF文件，开始处理...")
    
    for tiff_file in tiff_files:
        depth_to_colormap(
            tiff_file,
            output_dir,
            depth_output_dir,
            colormap,
            min_depth,
            max_depth
        )
    
    print(f"所有 {len(tiff_files)} 个文件处理完成")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='将16位TIFF深度图转换为纯净的伪彩图和灰度深度图')
    parser.add_argument('input_path', help='输入的深度图路径或目录')
    parser.add_argument('--output_path', '-o', help='输出的伪彩图路径或目录')
    parser.add_argument('--depth_output_path', '-d', help='输出的灰度深度图路径或目录')
    parser.add_argument('--colormap', '-c', default='jet', help='使用的颜色映射，如jet, plasma, viridis等')
    parser.add_argument('--min_depth', '-min', type=float, help='深度最小值')
    parser.add_argument('--max_depth', '-max', type=float, help='深度最大值')
    
    args = parser.parse_args()
    
    # 判断输入是文件还是目录
    if os.path.isdir(args.input_path):
        # 处理目录
        output_dir = args.output_path if args.output_path else os.path.join(args.input_path, "colormap_output")
        depth_output_dir = args.depth_output_path if args.depth_output_path else output_dir
        process_directory(
            args.input_path,
            output_dir,
            depth_output_dir,
            args.colormap,
            args.min_depth,
            args.max_depth
        )
    else:
        # 处理单个文件
        depth_to_colormap(
            args.input_path,
            args.output_path,
            args.depth_output_path,
            args.colormap,
            args.min_depth,
            args.max_depth
        )