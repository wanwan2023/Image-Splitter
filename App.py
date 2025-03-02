from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image
import io
import os
import base64
from datetime import datetime
import zipfile
from urllib.parse import unquote
import re
import argparse
import json
from io import BytesIO

app = Flask(__name__)

# 配置上传文件夹
UPLOAD_FOLDER = 'static/splits'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

def split_image(image, split_positions, direction='vertical'):
    """
    优化的图片分割函数，保持原始比例，只改变分割方向的尺寸
    """
    width, height = image.size
    parts = []
    
    # 将百分比转换为实际像素位置并排序
    pixel_positions = [0]  # 添加起始位置
    for pos in sorted(split_positions):
        if direction == 'vertical':
            pixel_pos = int(width * (pos / 100))
        else:
            pixel_pos = int(height * (pos / 100))
        if pixel_pos > 0:  # 避免重复的0位置
            pixel_positions.append(pixel_pos)
    
    # 添加终点位置
    pixel_positions.append(width if direction == 'vertical' else height)
    
    # 分割图片
    for i in range(len(pixel_positions) - 1):
        start = pixel_positions[i]
        end = pixel_positions[i + 1]
        
        # 确保至少有1像素的间距
        if end <= start:
            end = start + 1
            
        # 创建分割区域，保持另一个方向的尺寸不变
        if direction == 'vertical':
            bbox = (start, 0, end, height)  # 只改变宽度，高度保持不变
        else:
            bbox = (0, start, width, end)   # 只改变高度，宽度保持不变
            
        # 直接裁剪，不进行缩放
        part = image.crop(bbox)
        parts.append(part)
    
    return parts

@app.route('/split', methods=['POST'])
def split():
    try:
        file = request.files['image']
        positions_data = json.loads(request.form.get('split_positions', '{}'))
        
        # 读取图片
        image = Image.open(file)
        if image.mode == 'RGBA':
            image = image.convert('RGB')
            
        # 获取分割位置
        vertical_positions = sorted([float(pos) for pos in positions_data.get('vertical', [])])
        horizontal_positions = sorted([float(pos) for pos in positions_data.get('horizontal', [])])
        
        # 进行分割
        final_parts = []
        if vertical_positions:
            # 垂直分割
            vertical_parts = split_image(image, vertical_positions, 'vertical')
            # 对每个垂直分割的部分进行水平分割
            for v_part in vertical_parts:
                if horizontal_positions:
                    h_parts = split_image(v_part, horizontal_positions, 'horizontal')
                    final_parts.extend(h_parts)
                else:
                    final_parts.append(v_part)
        elif horizontal_positions:
            # 只有水平分割
            final_parts = split_image(image, horizontal_positions, 'horizontal')
        else:
            final_parts = [image]
        
        # 保存结果
        result_paths = []
        for part in final_parts:
            output = BytesIO()
            part.save(output, format='PNG', quality=95, optimize=True)
            output.seek(0)
            result_paths.append('data:image/png;base64,' + base64.b64encode(output.getvalue()).decode())
        
        return jsonify({'parts': result_paths})
        
    except Exception as e:
        print(f"Error in split route: {str(e)}")
        return jsonify({'error': str(e)}), 400

def get_image_data(img):
    """将图片转换为base64编码"""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f'data:image/png;base64,{img_str}'

@app.route('/download', methods=['POST'])
def download_images():
    try:
        data = request.json
        original_image = data.get('original')
        parts = data.get('parts')
        
        # 创建临时zip文件
        zip_path = os.path.join(UPLOAD_FOLDER, 'temp.zip')
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            # 保存原图
            if original_image:
                # 从base64字符串提取图片数据
                img_data = base64.b64decode(original_image.split(',')[1])
                zipf.writestr('original.png', img_data)
            
            # 保存分割后的图片
            for i, part in enumerate(parts):
                img_data = base64.b64decode(part.split(',')[1])
                zipf.writestr(f'split_{i+1}.png', img_data)
        
        # 发送zip文件
        return send_file(
            zip_path,
            mimetype='application/zip',
            as_attachment=True,
            download_name='split_images.zip'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # 清理临时zip文件
        if os.path.exists(zip_path):
            try:
                os.remove(zip_path)
            except:
                pass

if __name__ == '__main__':
    # 添加命令行参数解析
    parser = argparse.ArgumentParser(description='Image Splitter Web Application')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the application on')
    args = parser.parse_args()
    
    # 使用指定的端口运行应用
    app.run(host='0.0.0.0', port=args.port, debug=True)
