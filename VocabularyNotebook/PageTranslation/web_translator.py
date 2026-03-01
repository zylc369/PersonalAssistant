#!/usr/bin/env python3
"""
Web Page Translator
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

class WebTranslator:
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
            filename = os.path.basename(parsed.path) or f"image_{hash(img_url)}.jpg"
            
            # 避免文件名冲突
            img_path = page_dir / "images" / filename
            img_path.parent.mkdir(exist_ok=True)
            
            # 下载图片
            response = self.session.get(img_url, timeout=10)
            if response.status_code == 200:
                with open(img_path, 'wb') as f:
                    f.write(response.content)
                return f"images/{filename}"
        except Exception as e:
            print(f"下载图片失败 {img_url}: {e}")
        
        return img_url
    
    def translate_text(self, text):
        """这里应该调用LLM进行翻译，现在返回原文作为占位"""
        # 在实际使用中，这里会调用LLM API
        # 现在我们先返回原文，用户可以手动替换或集成LLM
        return f"[待翻译] {text}"
    
    def process_node(self, node, base_url, page_dir):
        """递归处理HTML节点"""
        if node.name is None:  # 文本节点
            if node.strip():
                translated = self.translate_text(node.strip())
                node.replace_with(translated)
            return
        
        # 处理图片
        if node.name == 'img':
            src = node.get('src')
            if src:
                local_path = self.download_image(src, base_url, page_dir)
                node['src'] = local_path
            return
        
        # 跳过脚本和样式
        if node.name in ['script', 'style']:
            return
        
        # 递归处理子节点
        for child in list(node.children):
            self.process_node(child, base_url, page_dir)
    
    def translate_page(self, url, output_filename=None):
        """翻译整个网页"""
        try:
            print(f"正在获取网页: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # 解析HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 创建输出目录
            page_name = output_filename or f"page_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            page_dir = self.output_dir / page_name
            page_dir.mkdir(exist_ok=True)
            
            print(f"正在翻译内容...")
            # 处理HTML内容
            self.process_node(soup, url, page_dir)
            
            # 添加翻译标识
            if soup.head:
                meta = soup.new_tag('meta')
                meta['name'] = 'translator'
                meta['content'] = 'Web Page Translator'
                soup.head.append(meta)
            
            # 保存翻译后的HTML
            output_file = page_dir / f"{page_name}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            print(f"翻译完成！文件保存到: {output_file}")
            print(f"图片保存在: {page_dir}/images/")
            
            return output_file
            
        except Exception as e:
            print(f"翻译失败: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description='网页翻译工具')
    parser.add_argument('url', help='要翻译的网页URL')
    parser.add_argument('-o', '--output', help='输出文件名')
    parser.add_argument('-d', '--dir', default='translated_pages', help='输出目录')
    
    args = parser.parse_args()
    
    translator = WebTranslator(args.dir)
    result = translator.translate_page(args.url, args.output)
    
    if result:
        print(f"✅ 翻译成功！打开文件: {result}")
    else:
        print("❌ 翻译失败")
        sys.exit(1)

if __name__ == "__main__":
    main()