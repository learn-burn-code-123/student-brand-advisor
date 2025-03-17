#!/bin/bash

# 确保脚本在错误时退出
set -e

echo "===== 学生个人品牌顾问应用启动脚本 ====="

# 检查是否已安装Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python。请安装Python 3.8或更高版本。"
    exit 1
fi

# 检查是否已存在虚拟环境
if [ ! -d "venv" ]; then
    echo "正在创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "正在激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "正在安装依赖..."
pip install -r requirements.txt

# 运行应用
echo "正在启动应用..."
echo "应用将在 http://localhost:5000 运行"
python app.py

# 退出虚拟环境
deactivate
