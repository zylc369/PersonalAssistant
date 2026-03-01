#!/usr/bin/env python3
"""
LLM Web Page Translator
使用LLM将英文网页翻译成中文，保留HTML格式和图片
"""

import requests
from bs4 import BeautifulSoup
import os
import sys
import re
from urllib.parse import urljoin, urlparse
from pathlib import Path
import argparse
from datetime import datetime
import json

class LLMWebTranslator:
    def __init__(self, output_dir="translated_pages"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
    def download_image(self, img_url, base_url, page_dir):
        """下载图片到本地"""
        try:
            # 处理相对路径
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            elif not img_url.startswith(('http:', 'https:')):
                img_url = urljoin(base_url, img_url)
            
            # 获取图片文件名
            parsed = urlparse(img_url)
            filename = os.path.basename(parsed.path) or f"image_{abs(hash(img_url))}.jpg"
            
            # 避免文件名冲突
            img_path = page_dir / "images" / filename
            img_path.parent.mkdir(exist_ok=True)
            
            # 下载图片
            response = self.session.get(img_url, timeout=10)
            if response.status_code == 200:
                with open(img_path, 'wb') as f:
                    f.write(response.content)
                print(f"✓ 下载图片: {filename}")
                return f"images/{filename}"
        except Exception as e:
            print(f"✗ 下载图片失败 {img_url}: {e}")
        
        return img_url
    
    def translate_with_llm(self, text):
        """
        使用LLM翻译文本
        这里应该调用实际的LLM API
        """
        # 检查是否需要翻译（主要是英文内容）
        if not re.search(r'[a-zA-Z]', text) or len(text.strip()) < 3:
            return text
        
        # 在实际使用中，这里会调用LLM API
        # 现在提供一个模拟的翻译结果
        # 用户可以根据需要集成不同的LLM服务
        
        # 示例：简单的规则翻译（仅用于演示）
        common_words = {
            "hello": "你好",
            "world": "世界",
            "welcome": "欢迎",
            "home": "首页",
            "about": "关于",
            "contact": "联系",
            "services": "服务",
            "products": "产品",
            "news": "新闻",
            "blog": "博客",
            "login": "登录",
            "register": "注册",
            "search": "搜索",
            "menu": "菜单",
            "click": "点击",
            "here": "这里",
            "more": "更多",
            "read": "阅读",
            "all": "所有",
            "rights": "权利",
            "reserved": "保留",
            "copyright": "版权",
            "privacy": "隐私",
            "policy": "政策",
            "terms": "条款",
            "conditions": "条件"
        }
        
        # 简单的单词替换翻译
        words = text.lower().split()
        translated_words = []
        
        for word in words:
            # 清理标点符号
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word in common_words:
                translated_word = word.replace(clean_word, common_words[clean_word])
                translated_words.append(translated_word)
            else:
                translated_words.append(word)
        
        translated_text = ' '.join(translated_words)
        
        # 如果没有翻译，添加标记
        if translated_text == text:
            return f"{text} [待翻译]"
        
        return translated_text
    
    def extract_translatable_text(self, soup):
        """提取需要翻译的文本内容"""
        text_segments = []
        
        def walk_tree(node):
            if node.name is None:  # 文本节点
                text = node.strip()
                if text and len(text) > 2:  # 过滤太短的文本
                    text_segments.append({
                        'text': text,
                        'parent': node.parent,
                        'node': node
                    })
            elif node.name not in ['script', 'style', 'meta', 'link']:
                for child in node.children:
                    walk_tree(child)
        
        walk_tree(soup)
        return text_segments
    
    def translate_page_content(self, url, page_dir):
        """翻译页面内容"""
        try:
            print(f"正在获取网页: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # 解析HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            print(f"正在提取文本内容...")
            # 提取并翻译文本
            text_segments = self.extract_translatable_text(soup)
            
            print(f"找到 {len(text_segments)} 个文本片段，开始翻译...")
            
            # 批量翻译文本
            for i, segment in enumerate(text_segments):
                if i % 10 == 0:
                    print(f"翻译进度: {i+1}/{len(text_segments)}")
                
                original_text = segment['text']
                translated_text = self.translate_with_llm(original_text)
                
                # 替换原文
                if original_text != translated_text:
                    segment['node'].replace_with(translated_text)
            
            return soup
            
        except Exception as e:
            print(f"翻译内容失败: {e}")
            return None
    
    def process_images(self, soup, base_url, page_dir):
        """处理页面中的所有图片"""
        images = soup.find_all('img')
        print(f"找到 {len(images)} 张图片")
        
        for img in images:
            src = img.get('src')
            if src:
                local_path = self.download_image(src, base_url, page_dir)
                img['src'] = local_path
    
    def translate_page(self, url, output_filename=None):
        """翻译整个网页"""
        try:
            # 创建输出目录
            page_name = output_filename or f"page_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            page_dir = self.output_dir / page_name
            page_dir.mkdir(exist_ok=True)
            
            # 翻译页面内容
            soup = self.translate_page_content(url, page_dir)
            if not soup:
                return None
            
            # 处理图片
            print("正在处理图片...")
            self.process_images(soup, url, page_dir)
            
            # 添加翻译信息和样式
            if soup.head:
                # 添加CSS样式
                style = soup.new_tag('style')
                style.string = """
                body { font-family: "Microsoft YaHei", "PingFang SC", sans-serif; }
                .translation-info { 
                    background: #f0f8ff; 
                    padding: 10px; 
                    margin: 10px 0; 
                    border-left: 4px solid #2196F3; 
                    font-size: 14px; 
                }
                """
                soup.head.append(style)
                
                # 添加翻译信息
                meta = soup.new_tag('meta')
                meta['name'] = 'translator'
                meta['content'] = 'LLM Web Page Translator'
                soup.head.append(meta)
            
            # 在body开始处添加翻译信息
            if soup.body:
                info_div = soup.new_tag('div')
                info_div['class'] = 'translation-info'
                info_div.string = f"""
                🌐 此页面由LLM网页翻译器翻译 | 
                原文URL: <a href="{url}" target="_blank">{url}</a> | 
                翻译时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """
                soup.body.insert(0, info_div)
            
            # 保存翻译后的HTML
            output_file = page_dir / f"{page_name}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(str(soup.prettify()))
            
            print(f"✅ 翻译完成！")
            print(f"📄 HTML文件: {output_file}")
            print(f"🖼️  图片目录: {page_dir}/images/")
            
            return output_file
            
        except Exception as e:
            print(f"❌ 翻译失败: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description='LLM网页翻译工具')
    parser.add_argument('url', help='要翻译的网页URL')
    parser.add_argument('-o', '--output', help='输出文件名')
    parser.add_argument('-d', '--dir', default='translated_pages', help='输出目录')
    
    args = parser.parse_args()
    
    print("🚀 LLM网页翻译器启动")
    print(f"📋 目标URL: {args.url}")
    print(f"📁 输出目录: {args.dir}")
    
    translator = LLMWebTranslator(args.dir)
    result = translator.translate_page(args.url, args.output)
    
    if result:
        print(f"\n✨ 翻译成功！")
        print(f"🌐 在浏览器中打开: file://{result.absolute()}")
    else:
        print("\n❌ 翻译失败")
        sys.exit(1)

if __name__ == "__main__":
    main()