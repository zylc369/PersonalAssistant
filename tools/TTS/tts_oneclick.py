#!/usr/bin/env python3
"""
One-click TTS CLI Runner
A simplified, foolproof interface for the TTS CLI tool.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# ANSI colors for better output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_color(text, color=Colors.GREEN):
    """Print colored text."""
    print(f"{color}{text}{Colors.ENDC}")

def print_header(title):
    """Print section header."""
    print(f"\n{Colors.BLUE}{Colors.BOLD}=== {title} ==={Colors.ENDC}")

def print_step(step, description):
    """Print step information."""
    print(f"{Colors.YELLOW}[{step}] {Colors.ENDC}{description}")

def run_command(cmd, description=""):
    """Run command and return success."""
    try:
        print_step("RUNNING", description)
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        if result.stdout:
            print_color(result.stdout.strip(), Colors.GREEN)
        return True, ""
    except subprocess.CalledProcessError as e:
        error_msg = f"Command failed: {e}"
        if e.stderr:
            error_msg += f"\nError output: {e.stderr}"
        print_color(error_msg, Colors.RED)
        return False, error_msg

def check_python_version():
    """Check if Python version is supported."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_color(f"Python {version.major}.{version.minor} is not supported. Please use Python 3.8+", Colors.RED)
        print_color("Recommended: Python 3.10+ for best compatibility", Colors.YELLOW)
        return False
    
    print_step("✓", f"Python {version.major}.{version.minor} detected")
    if version.minor < 10:
        print_color("⚠  Warning: Python 3.8-3.9 detected. Some features may work better with Python 3.10+", Colors.YELLOW)
    return True

def setup_venv():
    """Setup or check virtual environment."""
    venv_path = Path("tts_venv")
    activate_script = None
    
    # Determine activation script based on platform
    if os.name == 'nt':  # Windows
        activate_script = venv_path / "Scripts" / "activate.bat"
    else:  # Unix-like
        activate_script = venv_path / "bin" / "activate"
    
    if not venv_path.exists():
        print_step("CREATING", "Virtual environment...")
        success, error = run_command(f"python3 -m venv tts_venv")
        if not success:
            return False, error
        
        # Always install dependencies in new environment
        print_step("INSTALLING", "Required dependencies...")
        if os.name == 'nt':  # Windows
            install_cmd = f"tts_venv\\Scripts\\pip install -r requirements.txt"
        else:  # Unix-like
            install_cmd = "source tts_venv/bin/activate && pip install -r requirements.txt"
        
        success, error = run_command(install_cmd)
        if not success:
            return False, error
        
        print_step("ACTIVATING", "Virtual environment...")
    else:
        print_step("FOUND", "Virtual environment exists")
        
        # Check if dependencies are installed, install if missing
        check_cmd = ""
        if os.name == 'nt':  # Windows
            check_cmd = f"tts_venv\\Scripts\\python -c \"import TTS; import torch; print('Dependencies OK')\""
        else:  # Unix-like
            check_cmd = "source tts_venv/bin/activate && python -c 'import TTS; import torch; print(\"Dependencies OK\")'"
        
        success, error = run_command(check_cmd, "Checking dependencies...")
        if not success:
            print_step("INSTALLING", "Required dependencies...")
            if os.name == 'nt':  # Windows
                install_cmd = f"tts_venv\\Scripts\\pip install -r requirements.txt"
            else:  # Unix-like
                install_cmd = "source tts_venv/bin/activate && pip install -r requirements.txt"
            
            success, error = run_command(install_cmd)
            if not success:
                return False, error
    
    return True, activate_script

def generate_command(args, activate_script):
    """Generate the actual TTS command."""
    if not args.text:
        return False, "No text provided"
    
    # Build command parts
    cmd_parts = []
    
    # Activation part
    if os.name == 'nt':  # Windows
        cmd_parts.append(f"cmd /c \"{activate_script} &&\"")
    else:  # Unix-like
        cmd_parts.append(f"source {activate_script} &&")
    
    # Python script part
    python_cmd = f"python tts_cli.py \"{args.text}\""
    
    # Add optional arguments
    if args.output:
        python_cmd += f" -o \"{args.output}\""
    if args.model_name:
        python_cmd += f" --model-name \"{args.model_name}\""
    if args.check_updates:
        python_cmd += " --check-updates"
    if args.cpu:
        python_cmd += " --cpu"
    if args.max_filename_length:
        python_cmd += f" --max-filename-length {args.max_filename_length}"
    if args.info:
        # For info, remove the text argument
        python_cmd = "python tts_cli.py --info"
    
    cmd_parts.append(python_cmd)
    
    if os.name == 'nt':  # Windows
        cmd_parts.append("\"")
    
    return True, " ".join(cmd_parts)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="One-click TTS CLI Runner - Text to Speech for English Learning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  tts_oneclick.py "Hello world"
  tts_oneclick.py "Hello world" -o custom.wav
  tts_oneclick.py --info
  tts_oneclick.py "How are you today" --max-filename-length 25
        """
    )
    
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to convert to speech (required unless using --info)"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output audio file path (auto-generated if not specified)"
    )
    
    parser.add_argument(
        "--model-name",
        default="tts_models/en/ljspeech/vits",
        help="TTS model to use (default: tts_models/en/ljspeech/vits)"
    )
    
    parser.add_argument(
        "--check-updates",
        action="store_true",
        help="Check for model updates before processing"
    )
    
    parser.add_argument(
        "--info",
        action="store_true",
        help="Display model information and exit"
    )
    
    parser.add_argument(
        "--cpu",
        action="store_true",
        help="Force CPU usage instead of GPU"
    )
    
    parser.add_argument(
        "--max-filename-length",
        type=int,
        default=20,
        help="Maximum length for auto-generated filename (default: 20)"
    )
    
    args = parser.parse_args()
    
    print_header("TTS One-Click Runner")
    print_color("Text-to-Speech CLI for English Learning", Colors.BLUE)
    
    # Check requirements
    if not check_python_version():
        sys.exit(1)
    
    # Setup virtual environment
    success, activate_script = setup_venv()
    if not success:
        print_color(f"Setup failed: {activate_script}", Colors.RED)
        sys.exit(1)
    
    if activate_script and not args.info and not args.text:
        print_color("Error: Text is required unless using --info", Colors.RED)
        parser.print_help()
        sys.exit(1)
    
    # Generate and run command
    if args.info or args.text:
        success, command = generate_command(args, activate_script)
        if success:
            print_header("Running TTS CLI")
            print_step("COMMAND", command)
            
            # Execute the final command
            try:
                if os.name == 'nt':  # Windows
                    os.system(f"cmd /c \"{command}\"")
                else:  # Unix-like
                    os.system(command)
            except KeyboardInterrupt:
                print_color("\nOperation cancelled by user", Colors.YELLOW)
                sys.exit(0)
            except Exception as e:
                print_color(f"Error executing command: {e}", Colors.RED)
                sys.exit(1)
        else:
            print_color(f"Command generation failed: {command}", Colors.RED)
            sys.exit(1)

if __name__ == "__main__":
    main()