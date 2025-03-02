# Image-Splitter
一个基于 Flask 的网页应用，提供简单直观的图片分割功能。用户可以通过多种方式分割图片，预览效果并下载分割结果。

## 功能特点

### 1. 多样化分割方式
- **垂直分割**：将图片垂直切分为左右两部分
- **水平分割**：将图片水平切分为上下两部分
- **自定义分割**：通过拖拽分割线，将图片分割成多个部分
  - 支持多条垂直和水平分割线
  - 可自由调整分割位置

### 2. 实时预览
- 上传图片后即时显示原图预览
- 分割后立即显示所有分割部分的预览
- 点击预览图片可放大查看细节
- 支持模态框展示大图预览

### 3. 便捷下载
- 一键下载所有分割结果
- 自动打包为ZIP文件
- 包含原图和所有分割后的图片
- 清晰的文件命名规则

## 技术栈

- **前端**：
  - HTML5
  - CSS3
  - JavaScript (原生)
  - 响应式设计

- **后端**：
  - Python 3.x
  - Flask 框架
  - Pillow (PIL) 图像处理库

## 安装说明

1. 克隆仓库
bash
git clone [repository-url]
cd image-splitter

2. 创建虚拟环境（推荐）
```bash
python -m venv venv
source venv/bin/activate # Linux/Mac
.\venv\Scripts\activate # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 运行应用

基本运行（默认端口5000）：
```bash
python App.py
```

指定端口运行：
```bash
# 方法1：通过环境变量设置端口
export FLASK_RUN_PORT=8080  # Linux/Mac
set FLASK_RUN_PORT=8080    # Windows
python App.py

# 方法2：直接在命令行指定端口
python App.py --port 8080
```

5. 访问应用
- 默认端口访问：`http://localhost:5000`
- 自定义端口访问：`http://localhost:<port>` (例如：`http://localhost:8080`)

## 使用指南

1. **上传图片**
   - 点击上传区域或拖拽图片到指定区域
   - 支持常见图片格式（PNG, JPG, JPEG）

2. **选择分割方式**
   - 垂直分割：选择"垂直分割"，调整分割线位置
   - 水平分割：选择"水平分割"，调整分割线位置
   - 自定义分割：选择"自定义分割"，添加多条分割线

3. **预览和下载**
   - 分割完成后自动显示预览
   - 点击预览图片可查看大图
   - 点击"下载所有图片"按钮获取ZIP包

## 项目结构

```
image-splitter/
│
├── App.py                 # 主应用程序文件
├── requirements.txt       # 项目依赖
├── static/               # 静态资源目录
│   └── splits/           # 分割图片存储目录
│
└── templates/            # HTML模板
    └── index.html        # 主页面
```

## 注意事项

- 建议上传图片大小不超过 10MB
- 支持的图片格式：PNG, JPG, JPEG
- 临时文件会自动清理
- 建议使用现代浏览器以获得最佳体验

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件至 [vi20230203@gmail.com]

## 更新日志

### v1.0.0 (2024-03-02)
- 初始版本发布
- 支持基本的图片分割功能
- 添加图片预览和下载功能



