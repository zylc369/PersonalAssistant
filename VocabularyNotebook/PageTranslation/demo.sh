#!/bin/bash

# LLM网页翻译器示例脚本

echo "🌐 LLM网页翻译器示例"
echo "==================="

# 示例URL列表
urls=(
    "https://www.example.com"
    "https://httpbin.org/html"
    "https://www.w3.org/"
)

echo "📋 可用的示例URL："
for i in "${!urls[@]}"; do
    echo "  $((i+1)). ${urls[$i]}"
done

echo ""
echo "🔤 请选择要翻译的URL (输入数字 1-${#urls[@]}) 或输入自定义URL："
read -p "> " choice

# 检查用户输入
if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le ${#urls[@]} ]; then
    # 选择预设URL
    selected_url="${urls[$((choice-1))]}"
    echo "🎯 已选择: $selected_url"
elif [[ "$choice" =~ ^https?:// ]]; then
    # 自定义URL
    selected_url="$choice"
    echo "🎯 自定义URL: $selected_url"
else
    echo "❌ 无效选择"
    exit 1
fi

echo ""
echo "🚀 开始翻译..."
echo "================"

# 运行翻译器
python3 llm_translator.py "$selected_url" -o "demo_page"

echo ""
echo "✨ 翻译完成！"
echo "📁 查看翻译结果: translated_pages/demo_page/"
echo "🌐 在浏览器中打开翻译后的页面"