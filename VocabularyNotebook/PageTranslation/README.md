# LLM网页翻译器

一个使用LLM将英文网页翻译成中文的工具，保留原始HTML格式和图片显示。

## 功能特点

- 🌐 **智能翻译**: 使用LLM进行高质量翻译
- 🖼️ **图片保留**: 自动下载并显示页面中的图片
- 📄 **格式保持**: 保留原始HTML布局和样式
- 📁 **批量处理**: 支持翻译多个网页
- 🎨 **中文优化**: 针对中文显示优化字体和样式

## 安装依赖

```bash
cd PageTranslation
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
python llm_translator.py "https://example.com"
```

### 指定输出文件名

```bash
python llm_translator.py "https://example.com" -o "my_page"
```

### 指定输出目录

```bash
python llm_translator.py "https://example.com" -d "my_translations"
```

## 命令行参数

- `url`: 要翻译的网页URL（必需）
- `-o, --output`: 输出文件名（可选）
- `-d, --dir`: 输出目录（默认：translated_pages）

## 输出结构

翻译完成后，会生成以下结构：

```
translated_pages/
├── page_20240208_143022/
│   ├── page_20240208_143022.html
│   └── images/
│       ├── logo.png
│       ├── banner.jpg
│       └── ...
```

## 翻译质量

当前版本使用简单的词汇替换翻译。要获得更好的翻译质量，可以：

### 1. 集成OpenAI API

在 `translate_with_llm` 方法中添加：

```python
import openai

def translate_with_llm(self, text):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一个专业的英译中翻译器。请将以下英文文本翻译成自然流畅的中文。"},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content
```

### 2. 集成其他LLM服务

- Claude API
- 百度文心一言
- 阿里通义千问
- 本地LLM模型

## 示例用法

### 翻译新闻网站

```bash
python llm_translator.py "https://www.bbc.com/news"
```

### 翻译技术文档

```bash
python llm_translator.py "https://docs.python.org/3/" -o "python_docs"
```

### 批量翻译

创建一个shell脚本进行批量翻译：

```bash
#!/bin/bash
urls=(
    "https://example.com/page1"
    "https://example.com/page2"
    "https://example.com/page3"
)

for url in "${urls[@]}"; do
    python llm_translator.py "$url"
done
```

## 注意事项

1. **网络连接**: 需要稳定的网络连接来获取网页内容
2. **图片下载**: 大图片可能需要较长时间下载
3. **翻译限制**: 当前版本有翻译长度限制
4. **编码问题**: 确保目标网页使用UTF-8编码

## 故障排除

### 常见问题

**Q: 翻译后显示乱码**
A: 检查目标网页的编码，确保是UTF-8

**Q: 图片无法显示**
A: 检查网络连接和图片URL是否可访问

**Q: 翻译质量不佳**
A: 集成更好的LLM服务或API

**Q: 程序运行缓慢**
A: 大型网页需要更多时间，请耐心等待

## 扩展功能

### 待实现功能

- [ ] 支持更多翻译引擎
- [ ] 批量URL处理
- [ ] 翻译质量评估
- [ ] 多语言支持
- [ ] GUI界面
- [ ] 浏览器插件

## 贡献

欢迎提交Issue和Pull Request来改进这个工具！

## 许可证

MIT License