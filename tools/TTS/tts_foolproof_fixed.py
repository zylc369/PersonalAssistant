#!/usr/bin/env python3
"""
TTS傻瓜式一键脚本 - 完全自动化的文本转语音工具 (自动修复版)
自动创建虚拟环境、安装依赖、修复兼容性问题、运行TTS
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_msg(text, color=Colors.GREEN):
    print(f"{color}{text}{Colors.ENDC}")

def print_header(title):
    print(f"\n{Colors.BLUE}{Colors.BOLD}🎵 {title} 🎵{Colors.ENDC}")

def print_step(step, description):
    print(f"{Colors.YELLOW}📌 [{step}] {Colors.ENDC}{description}")

def run_cmd(cmd, shell=True):
    """运行命令并返回结果"""
    try:
        print_step("执行", cmd)
        result = subprocess.run(cmd, shell=shell, capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            if result.stdout.strip():
                print_msg("✅ " + result.stdout.strip(), Colors.GREEN)
            return True, result.stdout
        else:
            print_msg("❌ 错误: " + result.stderr.strip(), Colors.RED)
            return False, result.stderr
    except subprocess.TimeoutExpired:
        print_msg("❌ 命令执行超时", Colors.RED)
        return False, "Timeout"
    except Exception as e:
        print_msg(f"❌ 异常: {str(e)}", Colors.RED)
        return False, str(e)

def check_python():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_msg(f"❌ Python {version.major}.{version.minor} 不支持，需要 Python 3.8+", Colors.RED)
        return False
    
    print_msg(f"✅ Python {version.major}.{version.minor} 检测通过", Colors.GREEN)
    return True

def fix_bangla_compatibility():
    """修复bangla包的Python 3.9兼容性问题"""
    bangla_file = Path("tts_venv/lib/python3.9/site-packages/bangla/__init__.py")
    if bangla_file.exists():
        try:
            content = bangla_file.read_text()
            # 修复Python 3.9不支持的类型提示语法
            if "ordinal: bool | None = False" in content:
                content = content.replace("ordinal: bool | None = False", "ordinal = False")
                bangla_file.write_text(content)
                print_msg("✅ 已修复bangla包兼容性问题", Colors.GREEN)
                return True
        except Exception as e:
            print_msg(f"⚠️ 修复bangla兼容性问题失败: {e}", Colors.YELLOW)
    return False

def setup_venv():
    """设置虚拟环境"""
    venv_path = Path("tts_venv")
    
    # 检查虚拟环境是否存在
    if not venv_path.exists():
        print_step("创建", "虚拟环境 tts_venv...")
        success, _ = run_cmd("python3 -m venv tts_venv")
        if not success:
            print_msg("❌ 虚拟环境创建失败", Colors.RED)
            return False
    else:
        print_msg("✅ 虚拟环境已存在", Colors.GREEN)
    
    # 确定pip路径
    if os.name == 'nt':  # Windows
        pip_cmd = "tts_venv\\Scripts\\pip"
        python_cmd = "tts_venv\\Scripts\\python"
    else:  # Unix-like
        pip_cmd = "./tts_venv/bin/pip"
        python_cmd = "./tts_venv/bin/python"
    
    # 检查依赖是否已安装
    print_step("检查", "依赖项...")
    check_cmd = f'{python_cmd} -c "import TTS, torch; print(\'依赖OK\')"'
    success, _ = run_cmd(check_cmd)
    
    if not success:
        print_step("安装", "TTS和依赖项（这可能需要几分钟）...")
        
        # 升级pip
        run_cmd(f"{pip_cmd} install --upgrade pip")
        
        # 安装依赖
        install_cmd = f"{pip_cmd} install 'TTS>=0.21.0,<0.22.0' 'numpy<2.0.0' 'torch>=2.0.0,<2.3.0' 'urllib3<2.0.0' torchaudio"
        success, output = run_cmd(install_cmd)
        
        if not success:
            print_msg("❌ 依赖安装失败", Colors.RED)
            print_msg("💡 提示: 请确保网络连接正常", Colors.YELLOW)
            return False
        
        # 修复兼容性问题
        print_step("修复", "Python 3.9兼容性问题...")
        fix_bangla_compatibility()
    
    print_msg("✅ 虚拟环境和依赖就绪", Colors.GREEN)
    return True

def run_tts(text, output_file=None, model_name=None):
    """运行TTS转换"""
    # 构建命令
    if os.name == 'nt':  # Windows
        activate_cmd = "tts_venv\\Scripts\\activate &&"
    else:  # Unix-like
        activate_cmd = "source tts_venv/bin/activate &&"
    
    # 基础命令
    cmd = f"{activate_cmd} python tts_cli.py \"{text}\""
    
    # 添加参数
    if output_file:
        cmd += f" -o \"{output_file}\""
    if model_name:
        cmd += f" --model-name \"{model_name}\""
    
    print_step("生成语音", f"'{text}'")
    success, _ = run_cmd(cmd)
    
    if success:
        print_msg("🎉 语音生成成功！", Colors.GREEN)
        
        # 查找生成的文件
        if not output_file:
            # 自动查找生成的wav文件
            wav_files = list(Path(".").glob("*.wav"))
            if wav_files:
                latest_file = max(wav_files, key=os.path.getctime)
                print_msg(f"📁 生成文件: {latest_file}", Colors.BLUE)
    else:
        print_msg("❌ 语音生成失败", Colors.RED)
    
    return success

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="TTS傻瓜式一键脚本 - 自动化文本转语音 (自动修复版)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python tts_foolproof_fixed.py "Hello world"
  python tts_foolproof_fixed.py "你好世界" -o my_audio.wav
  python tts_foolproof_fixed.py "How are you" --model-name tts_models/en/ljspeech/vits
        """
    )
    
    parser.add_argument("text", help="要转换的文本")
    parser.add_argument("-o", "--output", help="输出音频文件路径（可选）")
    parser.add_argument("--model-name", default="tts_models/en/ljspeech/vits", 
                       help="TTS模型名称（默认: tts_models/en/ljspeech/vits）")
    
    args = parser.parse_args()
    
    print_header("TTS傻瓜式一键脚本 (自动修复版)")
    print_msg("🎤 自动化文本转语音工具", Colors.BLUE)
    
    # 1. 检查Python
    if not check_python():
        sys.exit(1)
    
    # 2. 设置虚拟环境和依赖
    if not setup_venv():
        print_msg("❌ 环境设置失败，程序退出", Colors.RED)
        sys.exit(1)
    
    # 3. 运行TTS
    if run_tts(args.text, args.output, args.model_name):
        print_msg("🎊 任务完成！", Colors.GREEN)
    else:
        print_msg("💔 任务失败", Colors.RED)
        sys.exit(1)

if __name__ == "__main__":
    main()