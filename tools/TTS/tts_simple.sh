#!/bin/bash
# TTS Simple Shell Script - TRUE One-Click Experience
# Zero dependencies, no virtual environments, no manual steps required

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}=== TTS Simple One-Click ===${NC}"
    echo -e "${BLUE}Text-to-Speech for English Learning${NC}"
}

print_step() {
    echo -e "${YELLOW}[STEP]${NC} ${2}"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} ${2}"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} ${2}"
}

# Check for Python in common locations
find_python() {
    for cmd in python3 python; do
        if command -v "$cmd" >/dev/null 2>&1; then
            echo "$cmd"
            return 0
        fi
    done
    return 1
}

# Install TTS globally using pip
install_global_tts() {
    print_step "INSTALLING" "TTS globally (one-time setup)..."
    
    # Check if pip is available
    PIP_CMD=""
    if command -v pip3 >/dev/null 2>&1; then
        PIP_CMD="pip3"
    elif command -v pip >/dev/null 2>&1; then
        PIP_CMD="pip"
    else
        print_error "Neither pip nor pip3 found. Please install Python pip first."
        exit 1
    fi
    
    # Install TTS with user-level packages
    print_step "INSTALLING" "TTS with user permissions..."
    
    if [ "$PIP_CMD" = "pip3" ]; then
        install_cmd="pip3 install --user"
    elif [ "$PIP_CMD" = "pip" ]; then
        install_cmd="pip install"
    else
        print_error "Unknown pip version: $PIP_CMD"
        exit 1
    fi
    
    print_step "INSTALLING" "Core dependencies (this may take a few minutes)..."
    $install_cmd "TTS>=0.21.0,<0.23.0" "numpy<2.0.0" "torch>=2.0.0,<2.9.0" 2>/dev/null
    
    if [ $? -ne 0 ]; then
        print_error "Failed to install TTS. Please try:"
        echo "  $install_cmd --upgrade pip"
        echo "  $install_cmd TTS numpy torch"
        exit 1
    fi
    
    print_success "TTS installed globally"
}

# Run TTS with global installation
run_tts() {
    local text="$1"
    shift
    local args=("$@")
    
    print_step "GENERATING" "Speech from: '$text'"
    
    # Create temporary Python script with error handling
    temp_script="/tmp/tts_temp_script_$$"
    cat > "$temp_script" << 'SCRIPT'
import sys
import argparse
import subprocess
import os

def safe_tts_call(text, model_name, output_file, check_updates, use_cpu, args_list):
    """Safely call TTS with error handling."""
    try:
        # Build command
        cmd = [sys.executable, "python3"] + args_list
        
        # Run the command and capture output
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"[SUCCESS] {text}")
            if result.stdout:
                print(result.stdout.strip())
            if result.stderr:
                    print(f"Warning: {result.stderr.strip()}")
            return True
        
        print_error(f"TTS conversion failed. Exit code: {result.returncode}")
        return False
    except Exception as e:
        print_error(f"Exception occurred: {e}")
        return False

# Build arguments
build_args_list() {
    args_list=("$@")
    
    # Add model argument
    args_list+=("--model-name")
    args_list+=("$model_name")
    
    # Add output argument if provided
    if [ -n "$1" ]; then
        args_list+=("-o")
        args_list+=("$1")
        args_list+=("$2")
    fi
    
    # Add optional arguments
    if [ "$3" = "--check-updates" ]; then
        args_list+=("$3")
    
    if [ "$4" = "--cpu" ]; then
        args_list+=("$4")
    
    if [ "$5" = "--info" ]; then
        args_list+=("$5")
    
    echo "[INFO] Command: python3 ${args_list[*]}"
}

# Generate filename if not provided
    if [ ! -n "$1" ]; then
        # Generate filename from text
        words=("$1" tr '[:upper:]' '[:lower:]')
        filename=$(echo "$words" | tr ' ' ' '_' | cut -c1-20)
        args_list+=("-o")
        args_list+=("${filename}.wav")
    fi
}

    return "${args_list[@]}"
EOF
    
    # Execute TTS call
    if safe_tts_call "$text" "$model_name" "$output_file" "$check_updates" "$use_cpu" "$build_args_list"); then
        print_success "TTS conversion completed successfully!"
    else
        print_error "TTS conversion failed. Check error messages above."
        exit 1
}

# Main execution
main() {
    print_header
    
    # Check if we need to install TTS
    if ! command -v python3 -c "import TTS" 2>/dev/null; then
        print_step "CHECKING" "Python 3 availability..."
        
        if find_python; then
            print_success "Python 3 found: $(which python3)"
            if ! check_global_tts; then
                install_global_tts
            else
                print_step "FOUND" "TTS already available globally"
        else
            print_error "Python 3 not found. Please install Python 3.8+ first."
            exit 1
        fi
    else
        print_error "Python 3 not found. Please install Python 3.8+ first."
        exit 1
    fi
    
    # Validate input
    if [ $# -eq 0 ]; then
        print_error "No text provided. Usage: $0 \"Your text here\""
        echo ""
        echo "Examples:"
        echo "  $0 \"Hello world\""
        echo "  $0 \"Hello world\" -o output.wav"
        echo "  $0 --info"
        exit 1
    fi
    
    # Run TTS
    run_tts "$@"
    local result=$?
    
    if [ $result -eq 0 ]; then
        exit 0
    else
        exit 1
    fi
}

# Run main function with all arguments
main "$@"