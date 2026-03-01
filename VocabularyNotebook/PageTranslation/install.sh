#!/bin/bash

# LLM网页翻译器安装脚本

echo "🚀 LLM网页翻译器安装程序"
echo "=========================="

# 检查Python版本
echo "📋 检查Python版本..."
python_version=$(python3 --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo "✅ $python_version"
else
    echo "❌ 未找到Python3，请先安装Python"
    exit 1
fi

# 检查pip
echo "📋 检查pip..."
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 已安装"
else
    echo "❌ 未找到pip3，请先安装pip"
    exit 1
fi

# 安装依赖
echo "📦 安装依赖包..."
pip3 install -r requirements.txt

if [[ $? -eq 0 ]]; then
    echo "✅ 依赖安装成功"
else
    echo "❌ 依赖安装失败"
    exit 1
fi

# 创建输出目录
echo "📁 创建输出目录..."
mkdir -p translated_pages

# 设置执行权限
echo "🔐 设置执行权限..."
chmod +x llm_translator.py
chmod +x web_translator.py

echo ""
echo "🎉 安装完成！"
echo ""
echo "📖 使用方法："
echo "  python3 llm_translator.py \"https://example.com\""
echo ""
echo "📚 更多信息请查看 README.md"
echo ""
echo "🌐 开始翻译你的第一个网页吧！"