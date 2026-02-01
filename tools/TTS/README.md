# TTS CLI Tool

A command-line tool for converting English text to speech using Coqui TTS, designed for English learning applications.

## Features

- Convert English words and sentences to speech
- Display model storage locations
- Check for model updates
- Support for GPU/CPU processing
- Model information display
- Offline operation after initial model download

## Installation

### Easy Setup (Recommended)

Run the automatic setup script:

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

The setup script will:
- Check Python 3.8+ installation
- Create a virtual environment
- Install all required dependencies
- Create a launcher script

### Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. For development:
```bash
pip install -r requirements-dev.txt
```

## Usage

### Basic Usage

**Using launcher script (after setup):**

Linux/macOS:
```bash
./tts "Hello world"
```

Windows:
```cmd
tts.bat "Hello world"
```

**Manual usage:**
```bash
python tts_cli.py "Hello world"
```

### Advanced Usage

**Using launcher script:**

Linux/macOS:
```bash
./tts "Hello world" --output my_speech.wav
./tts "Hello world" --check-updates
./tts "Hello world" --model-name "tts_models/en/ljspeech/vits"
./tts --info
./tts "Hello world" --cpu
```

Windows:
```cmd
tts.bat "Hello world" --output my_speech.wav
tts.bat "Hello world" --check-updates
tts.bat "Hello world" --model-name "tts_models/en/ljspeech/vits"
tts.bat --info
tts.bat "Hello world" --cpu
```

**Manual usage:**
```bash
python tts_cli.py "Hello world" --output my_speech.wav
python tts_cli.py "Hello world" --check-updates
python tts_cli.py "Hello world" --model-name "tts_models/en/ljspeech/vits"
python tts_cli.py --info
python tts_cli.py "Hello world" --cpu
```

### Command Line Options

- `text`: Text to convert to speech (optional if using --info)
- `--model-name`: TTS model to use (default: tts_models/en/ljspeech/vits)
- `--output, -o`: Output audio file path (default: output.wav)
- `--check-updates`: Check for model updates before processing
- `--info`: Display model information and exit
- `--cpu`: Force CPU usage instead of GPU

### Environment Variables

- `COQUI_MODEL_PATH`: Custom path for model storage (default: ~/.local/share/tts/)

## Development

### Setup Development Environment

For development setup with extra tools:

**Linux/macOS:**
```bash
./setup.sh --dev
```

**Windows:**
```cmd
setup.bat --dev
```

### Running Tests

Run all tests:
```bash
./tts_venv/bin/python -m pytest tests/
```

Run single test:
```bash
./tts_venv/bin/python -m pytest tests/test_tts_cli.py::TestTTSCLI::test_init
```

### Code Quality

Format code:
```bash
./tts_venv/bin/black *.py
```

Type checking:
```bash
./tts_venv/bin/mypy *.py
```

Linting:
```bash
./tts_venv/bin/pylint *.py
```

## Model Information

Models are downloaded automatically on first use and stored in:
- Default: `~/.local/share/tts/`
- Custom: Set via `COQUI_MODEL_PATH` environment variable

The tool displays model location information on each run to help you track where models are stored.

## License

This project follows the same license as the Coqui TTS library.