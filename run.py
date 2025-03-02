import webview
import sys
import os
from App import app
import threading
import socket

def get_free_port():
    """获取一个可用的端口号"""
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

def run_flask():
    """运行Flask应用"""
    port = get_free_port()
    app.run(port=port)
    return port

def main():
    # 启动Flask服务
    port = get_free_port()
    flask_thread = threading.Thread(target=lambda: app.run(port=port))
    flask_thread.daemon = True
    flask_thread.start()

    # 创建窗口
    webview.create_window(
        title='图片分割工具', 
        url=f'http://127.0.0.1:{port}',
        width=1200,
        height=800,
        resizable=True,
        min_size=(800, 600)
    )
    webview.start()

if __name__ == '__main__':
    main() 