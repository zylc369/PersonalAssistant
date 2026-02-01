# TTS One-Click Runner

A foolproof, one-click interface for the TTS CLI tool.

## Quick Start

### For English Learning (Recommended)

```bash
# Install and run in one command
python3 tts_oneclick.py "Hello world"
```

### For Chinese Learning

```bash
python3 tts_oneclick.py "你好世界"
```

## Features

✅ **Automatic Setup**
- Creates `tts_venv` virtual environment if needed
- Installs all required dependencies automatically
- Checks Python version compatibility

✅ **One-Click Usage**
- Just run with text: `python3 tts_oneclick.py "Your text"`
- No manual setup required
- All configuration handled automatically

✅ **Smart Features**
- Auto-generated filenames (hello_world.wav, how_are_you_today.wav)
- Directory output support (`-o audio/` → audio/hello_world.wav)
- Model information display (`--info`)
- Update checking (`--check-updates`)

✅ **Cross-Platform**
- Works on macOS, Linux, and Windows
- Automatic platform detection
- Smart path handling

## Examples

```bash
# Basic usage
python3 tts_oneclick.py "Hello world"

# Custom output file
python3 tts_oneclick.py "Hello world" -o custom_name.wav

# Output to directory
python3 tts_oneclick.py "Hello world" -o audio/
python3 tts_oneclick.py "Hello world" -o "/path/to/audio/"

# Different models
python3 tts_oneclick.py "Hello world" --model-name "tts_models/en/vctk/vits"

# Model information
python3 tts_oneclick.py --info

# Check for updates
python3 tts_oneclick.py "Hello world" --check-updates

# Force CPU usage
python3 tts_oneclick.py "Hello world" --cpu

# Longer text with custom filename length
python3 tts_oneclick.py "This is a very long sentence" --max-filename-length 15
```

## What Happens Behind the Scenes

1. **Python Check**: Verifies Python 3.8+ compatibility
2. **Virtual Environment**: Creates `tts_venv/` if not exists
3. **Dependencies**: Installs TTS, PyTorch, and all required packages
4. **Model Management**: Uses official Coqui TTS model paths
5. **Smart Output**: Auto-generates meaningful filenames

## File Organization

```
./
├── tts_oneclick.py          # One-click runner
├── tts_cli.py               # Main CLI tool
├── tts_venv/               # Virtual environment
├── audio/                   # Your audio files
├── audio2/                  # More audio files
└── tts_models--en--ljspeech--vits/  # Downloaded models (actual location varies by OS)
```

## Model Storage

Models are automatically downloaded to:
- **macOS**: `~/Library/Application Support/tts/`
- **Linux**: `~/.local/share/tts/`
- **Windows**: `%APPDATA%/tts/`

Use `--info` to see model information and available models.

## Troubleshooting

### First Run
```bash
# Clean start (recommended)
rm -rf tts_venv
python3 tts_oneclick.py "Hello world"
```

### If Dependencies Fail
```bash
# Manual dependency check
source tts_venv/bin/activate
pip install -r requirements.txt
```

### Python Version Issues
```bash
# Check your Python version
python3 --version
# Recommended: Python 3.10+
```

## Color Output

The tool uses colored output:
- 🟢 Green: Success messages
- 🟡 Yellow: Warnings  
- 🔴 Red: Errors
- 🔵 Blue: Section headers

## Advanced Usage

All advanced features from `tts_cli.py` are supported:

```bash
# Development mode with extra tools
python3 setup.sh --dev

# Manual activation for debugging
source tts_venv/bin/activate
python tts_cli.py --help
```

That's it! Just run `python3 tts_oneclick.py "Your text"` and you're ready to go!