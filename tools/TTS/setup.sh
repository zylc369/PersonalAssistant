#!/bin/bash
# setup.sh - TTS CLI Setup Script
# This script sets up the TTS CLI tool by checking Python, creating virtual environment, and installing dependencies

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get Python version
get_python_version() {
    if command_exists python3; then
        python3 --version 2>&1 | awk '{print $2}'
    else
        echo ""
    fi
}

# Function to validate Python version
validate_python_version() {
    local version=$1
    local major=$(echo "$version" | cut -d. -f1)
    local minor=$(echo "$version" | cut -d. -f2)
    
    # Check if Python 3.8 or higher
    if [[ "$major" -ge 3 && "$minor" -ge 8 ]]; then
        return 0
    else
        return 1
    fi
}

# Function to create virtual environment
create_venv() {
    local venv_path="$1"
    
    print_status "Creating virtual environment at $venv_path..."
    
    if [[ -d "$venv_path" ]]; then
        print_warning "Virtual environment already exists. Recreating..."
        rm -rf "$venv_path"
    fi
    
    python3 -m venv "$venv_path"
    
    if [[ $? -eq 0 ]]; then
        print_success "Virtual environment created successfully"
        return 0
    else
        print_error "Failed to create virtual environment"
        return 1
    fi
}

# Function to activate virtual environment and install dependencies
install_dependencies() {
    local venv_path="$1"
    local os_type="$2"
    
    print_status "Installing dependencies..."
    
    # Source virtual environment
    source "$venv_path/bin/activate"
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install requirements
    if [[ -f "requirements.txt" ]]; then
        print_status "Installing core dependencies from requirements.txt..."
        pip install -r requirements.txt
        
        if [[ $? -eq 0 ]]; then
            print_success "Core dependencies installed successfully"
        else
            print_error "Failed to install core dependencies"
            return 1
        fi
    else
        print_error "requirements.txt not found"
        return 1
    fi
    
    # Install development dependencies if requested
    if [[ "$INSTALL_DEV" == "true" ]] && [[ -f "requirements-dev.txt" ]]; then
        print_status "Installing development dependencies from requirements-dev.txt..."
        pip install -r requirements-dev.txt
        
        if [[ $? -eq 0 ]]; then
            print_success "Development dependencies installed successfully"
        else
            print_warning "Failed to install development dependencies (optional)"
        fi
    fi
    
    # OS-specific dependencies
    if [[ "$os_type" == "linux" ]]; then
        print_status "Checking for Linux audio dependencies..."
        
        # Check for pulseaudio or alsa
        if command_exists pulseaudio; then
            print_success "PulseAudio found"
        elif command_exists alsamixer; then
            print_success "ALSA found"
        else
            print_warning "No audio system detected. You may need to install pulseaudio or alsa-utils"
        fi
        
    elif [[ "$os_type" == "macos" ]]; then
        print_status "macOS detected. Audio should work with CoreAudio"
        
    elif [[ "$os_type" == "windows" ]]; then
        print_status "Windows detected. Checking for additional dependencies..."
        
        # Check for Visual C++ Redistributable
        if command_exists where; then
            if where vcruntime140.dll >/dev/null 2>&1; then
                print_success "Visual C++ Runtime found"
            else
                print_warning "Visual C++ Runtime may be required for some TTS models"
                print_warning "Install Microsoft Visual C++ Redistributable if you encounter issues"
            fi
        fi
    fi
    
    return 0
}

# Function to test the installation
test_installation() {
    local venv_path="$1"
    
    print_status "Testing TTS CLI installation..."
    
    # Source virtual environment
    source "$venv_path/bin/activate"
    
    # Test TTS import
    python3 -c "
try:
    from TTS.api import TTS
    print('✓ TTS import successful')
except ImportError as e:
    print('✗ TTS import failed:', e)
    exit(1)

try:
    import torch
    print('✓ PyTorch import successful')
    print('✓ CUDA available:', torch.cuda.is_available())
except ImportError as e:
    print('✗ PyTorch import failed:', e)
    exit(1)
"
    
    if [[ $? -eq 0 ]]; then
        print_success "TTS CLI test passed"
        return 0
    else
        print_error "TTS CLI test failed"
        return 1
    fi
}

# Function to create launcher script
create_launcher() {
    local venv_path="$1"
    local launcher_path="$2"
    
    print_status "Creating launcher script at $launcher_path..."
    
    cat > "$launcher_path" << 'EOF'
#!/bin/bash
# TTS CLI Launcher
# This script activates the virtual environment and runs tts_cli.py

# Get directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/tts_venv"

# Check if virtual environment exists
if [[ ! -d "$VENV_PATH" ]]; then
    echo "Error: Virtual environment not found at $VENV_PATH"
    echo "Please run setup.sh first"
    exit 1
fi

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Run tts_cli.py with all arguments
python3 "$SCRIPT_DIR/tts_cli.py" "$@"
EOF

    chmod +x "$launcher_path"
    
    if [[ $? -eq 0 ]]; then
        print_success "Launcher script created successfully"
        return 0
    else
        print_error "Failed to create launcher script"
        return 1
    fi
}

# Function to show usage instructions
show_usage() {
    local venv_path="$1"
    local launcher_path="$2"
    
    echo
    print_success "Setup completed successfully!"
    echo
    echo -e "${GREEN}=== Usage Instructions ===${NC}"
    echo
    echo "1. Using the launcher script (recommended):"
    echo "   $launcher_path \"Hello world\""
    echo
    echo "2. Manual usage:"
    echo "   source $venv_path/bin/activate"
    echo "   python3 tts_cli.py \"Hello world\""
    echo
    echo "3. To see all options:"
    echo "   $launcher_path --help"
    echo
    echo "4. First time usage:"
    echo "   $launcher_path \"Hello world\"  # This will download the TTS model"
    echo
    echo "5. To check model information:"
    echo "   $launcher_path --info"
    echo
    echo -e "${BLUE}Notes:${NC}"
    echo "- Models are downloaded automatically on first use"
    echo "- Model location is displayed on each run"
    echo "- For update checking, use: $launcher_path \"Hello world\" --check-updates"
    echo
}

# Main setup function
main() {
    echo
    echo "==================================="
    echo "TTS CLI Setup Script"
    echo "==================================="
    echo
    
    # Check if we're in the right directory
    if [[ ! -f "tts_cli.py" ]]; then
        print_error "tts_cli.py not found in current directory"
        print_error "Please run this script from the TTS tool directory"
        exit 1
    fi
    
    # Detect OS
    os_type=$(detect_os)
    print_status "Detected OS: $os_type"
    
    # Check Python 3
    print_status "Checking Python 3 installation..."
    if ! command_exists python3; then
        print_error "Python 3 is not installed or not in PATH"
        
        case $os_type in
            "linux")
                echo "Please install Python 3.8+ using:"
                echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip python3-venv"
                echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
                echo "  Fedora: sudo dnf install python3 python3-pip"
                ;;
            "macos")
                echo "Please install Python 3.8+ using:"
                echo "  Homebrew: brew install python3"
                echo "  Or download from https://www.python.org/"
                ;;
            "windows")
                echo "Please install Python 3.8+ from https://www.python.org/"
                echo "  Make sure to check 'Add Python to PATH' during installation"
                ;;
        esac
        exit 1
    fi
    
    # Get and validate Python version
    python_version=$(get_python_version)
    print_status "Found Python version: $python_version"
    
    if ! validate_python_version "$python_version"; then
        print_error "Python 3.8 or higher is required"
        print_error "Current version: $python_version"
        exit 1
    fi
    
    print_success "Python version check passed"
    
    # Check if pip is available
    if ! python3 -c "import pip" 2>/dev/null; then
        print_error "pip is not available for Python 3"
        echo "Please install pip:"
        case $os_type in
            "linux")
                echo "  Ubuntu/Debian: sudo apt install python3-pip"
                echo "  CentOS/RHEL: sudo yum install python3-pip"
                echo "  Fedora: sudo dnf install python3-pip"
                ;;
            "macos")
                echo "  python3 -m ensurepip --upgrade"
                ;;
            "windows")
                echo "  pip should be included with Python installation"
                ;;
        esac
        exit 1
    fi
    
    # Check for development dependencies
    INSTALL_DEV="false"
    if [[ "$1" == "--dev" ]] || [[ "$1" == "-d" ]]; then
        INSTALL_DEV="true"
        print_status "Will install development dependencies"
    fi
    
    # Virtual environment path
    VENV_PATH="./tts_venv"
    
    # Create virtual environment
    if ! create_venv "$VENV_PATH"; then
        exit 1
    fi
    
    # Install dependencies
    if ! install_dependencies "$VENV_PATH" "$os_type"; then
        exit 1
    fi
    
    # Test installation
    if ! test_installation "$VENV_PATH"; then
        exit 1
    fi
    
    # Create launcher script
    LAUNCHER_PATH="./tts"
    if ! create_launcher "$VENV_PATH" "$LAUNCHER_PATH"; then
        exit 1
    fi
    
    # Show usage instructions
    show_usage "$VENV_PATH" "$LAUNCHER_PATH"
}

# Parse command line arguments
case "$1" in
    --help|-h)
        echo "TTS CLI Setup Script"
        echo
        echo "Usage: $0 [OPTIONS]"
        echo
        echo "Options:"
        echo "  --help, -h       Show this help message"
        echo "  --dev, -d        Install development dependencies"
        echo
        echo "This script will:"
        echo "  - Check Python 3.8+ installation"
        echo "  - Create a virtual environment"
        echo "  - Install required dependencies"
        echo "  - Create a launcher script"
        echo
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac