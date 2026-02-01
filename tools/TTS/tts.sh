#!/bin/bash
# TTS一键式傻瓜脚本 - 最终版
# 完全自动化的文本转语音工具

set -e

# 颜色和表情符号
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

EMOJI_MUSIC="🎵"
EMOJI_INFO="ℹ️"
EMOJI_CHECK="✅"
EMOJI_CROSS="❌"
EMOJI_ROCKET="🚀"

print_header() {
    echo -e "\n${PURPLE}${EMOJI_MUSIC} TTS一键式傻瓜脚本 ${EMOJI_MUSIC}${NC}"
    echo -e "${CYAN}完全自动化的文本转语音工具${NC}"
}

print_step() {
    echo -e "${YELLOW}${EMOJI_INFO} [步骤]${NC} $1"
}

print_success() {
    echo -e "${GREEN}${EMOJI_CHECK} 成功:${NC} $1"
}

print_error() {
    echo -e "${RED}${EMOJI_CROSS} 错误:${NC} $1"
}

# 检查Python
check_python() {
    print_step "检查Python安装..."
    
    PYTHON_CMD=""
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
        PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')
        
        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
            print_success "Python $PYTHON_VERSION 检测通过"
            PYTHON_CMD="python3"
        else
            print_error "Python版本过低 ($PYTHON_VERSION)，需要 3.8+"
            return 1
        fi
    elif command -v python >/dev/null 2>&1; then
        PYTHON_VERSION=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        PYTHON_MAJOR=$(python -c 'import sys; print(sys.version_info.major)')
        PYTHON_MINOR=$(python -c 'import sys; print(sys.version_info.minor)')
        
        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
            print_success "Python $PYTHON_VERSION 检测通过"
            PYTHON_CMD="python"
        else
            print_error "Python版本过低 ($PYTHON_VERSION)，需要 3.8+"
            return 1
        fi
    else
        print_error "未找到Python，请先安装Python 3.8+"
        return 1
    fi
    
    return 0
}

# 修复兼容性问题
fix_compatibility() {
    if [ -d "tts_venv" ] && [ -f "tts_venv/lib/python3.9/site-packages/bangla/__init__.py" ]; then
        print_step "修复", "Python 3.9兼容性问题..."
        sed -i '' 's/ordinal: bool | None = False/ordinal = False/' tts_venv/lib/python3.9/site-packages/bangla/__init__.py 2>/dev/null || true
        print_success "兼容性修复完成"
    fi
}

# 设置虚拟环境
setup_venv() {
    print_step "设置虚拟环境..."
    
    if [ ! -d "tts_venv" ]; then
        print_step "创建虚拟环境..."
        $PYTHON_CMD -m venv tts_venv
        print_success "虚拟环境创建完成"
    else
        print_success "虚拟环境已存在"
    fi
    
    # 激活虚拟环境
    source tts_venv/bin/activate
    
    # 检查依赖
    print_step "检查TTS依赖..."
    if python -c "import TTS, torch; print('依赖检查通过')" 2>/dev/null; then
        print_success "TTS依赖已就绪"
        return 0
    fi
    
    # 安装依赖
    print_step "安装TTS依赖（这可能需要几分钟）..."
    pip install --upgrade pip
    pip install 'TTS>=0.21.0,<0.22.0' 'numpy<2.0.0' 'torch>=2.0.0,<2.3.0' 'urllib3<2.0.0' torchaudio
    
    if [ $? -ne 0 ]; then
        print_error "依赖安装失败"
        return 1
    fi
    
    # 修复兼容性问题
    fix_compatibility
    
    print_success "依赖安装完成"
    return 0
}

# 运行TTS
run_tts() {
    local text="$1"
    local output_file="$2"
    local model_name="$3"
    
    print_step "生成语音: '$text'"
    
    # 构建命令
    cmd="source tts_venv/bin/activate && python tts_cli.py \"$text\""
    
    if [ -n "$output_file" ]; then
        cmd="$cmd -o \"$output_file\""
    fi
    
    if [ -n "$model_name" ]; then
        cmd="$cmd --model-name \"$model_name\""
    fi
    
    # 执行命令
    eval "$cmd"
    
    if [ $? -eq 0 ]; then
        print_success "语音生成成功！"
        
        # 显示生成的文件
        if [ -n "$output_file" ]; then
            print_info "生成文件: 📁 $output_file"
        else
            latest_wav=$(ls -t *.wav 2>/dev/null | head -n 1)
            if [ -n "$latest_wav" ]; then
                print_info "生成文件: 📁 $latest_wav"
            fi
        fi
        
        return 0
    else
        print_error "语音生成失败"
        return 1
    fi
}

print_info() {
    echo -e "${BLUE}${EMOJI_INFO} 信息:${NC} $1"
}

# 显示帮助
show_help() {
    echo -e "${CYAN}使用方法:${NC}"
    echo "  $0 \"你的文本\"                    # 基本使用"
    echo "  $0 \"Hello world\" -o output.wav   # 指定输出文件"
    echo "  $0 \"你好世界\"                    # 中文文本"
    echo ""
    echo -e "${CYAN}示例:${NC}"
    echo "  $0 \"Hello, how are you today?\""
    echo "  $0 \"Welcome to TTS tool\" -o welcome.wav"
}

# 主函数
main() {
    print_header
    
    # 检查参数
    if [ $# -eq 0 ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        show_help
        exit 0
    fi
    
    local text="$1"
    local output_file=""
    local model_name="tts_models/en/ljspeech/vits"
    
    # 解析参数
    shift
    while [ $# -gt 0 ]; do
        case $1 in
            -o|--output)
                output_file="$2"
                shift 2
                ;;
            --model-name)
                model_name="$2"
                shift 2
                ;;
            *)
                print_error "未知参数: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 1. 检查Python
    if ! check_python; then
        exit 1
    fi
    
    # 2. 设置环境和依赖
    if ! setup_venv; then
        exit 1
    fi
    
    # 3. 运行TTS
    echo ""
    echo -e "${PURPLE}${EMOJI_ROCKET} 开始语音生成...${NC}"
    echo ""
    
    if run_tts "$text" "$output_file" "$model_name"; then
        echo ""
        echo -e "${GREEN}${EMOJI_CHECK} 任务完成！享受你的语音文件吧！${NC}"
    else
        echo ""
        echo -e "${RED}${EMOJI_CROSS} 任务失败${NC}"
        exit 1
    fi
}

# 运行主函数
main "$@"