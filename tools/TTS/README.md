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

Run automatic setup script:

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

### System Requirements

- Python 3.8+ (3.10+ recommended)
- espeak or espeak-ng (for some TTS models)
- Sufficient disk space for models (100MB-1GB+)

**Install espeak manually if needed:**
- Linux: `sudo apt install espeak-ng`
- macOS: `brew install espeak-ng` (or `brew install espeak`)
- Windows: Download from https://espeak.sourceforge.io/

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
./tts "Hello world"                    # Outputs: hello_world.wav
./tts "How are you today"           # Outputs: how_are_you_today.wav
./tts "Good morning everyone"         # Outputs: good_morning_everyone.wav
```

Windows:
```cmd
tts.bat "Hello world"                   # Outputs: hello_world.wav
tts.bat "How are you today"            # Outputs: how_are_you_today.wav
```

**Manual usage:**
```bash
python tts_cli.py "Hello world"
python tts_cli.py "How are you today"
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
./tts "This is a test" --max-filename-length 15  # Custom filename length
```

Windows:
```cmd
tts.bat "Hello world" --output my_speech.wav
tts.bat "Hello world" --check-updates
tts.bat "Hello world" --model-name "tts_models/en/ljspeech/vits"
tts.bat --info
tts.bat "Hello world" --cpu
tts.bat "This is a test" --max-filename-length 15
```

**Manual usage:**
```bash
python tts_cli.py "Hello world" --output my_speech.wav
python tts_cli.py "Hello world" --check-updates
python tts_cli.py "Hello world" --model-name "tts_models/en/ljspeech/vits"
python tts_cli.py --info
python tts_cli.py "Hello world" --cpu
python tts_cli.py "This is a test" --max-filename-length 15
```

### Automatic Filename Generation

**Features:**
- **Auto-generated filenames** when output path is not specified
- **Directory support**: When output is a directory, generates filename inside it
- **Automatic directory creation**: Creates directories if they don't exist
- **Word-based naming**: Takes first 5 words, joins with underscores
- **Length control**: Default max 20 characters, customizable with `--max-filename-length`
- **Clean naming**: Removes special characters, converts to lowercase
- **Smart truncation**: Cuts long names at word boundaries

**Examples:**
```bash
./tts "Hello world"                           # → hello_world.wav
./tts "How are you today"                      # → how_are_you_today.wav
./tts "Good morning everyone"                    # → good_morning_everyone.wav
./tts "This is a very long sentence..." --max-filename-length 15  # → this_is_a_very.wav

# Directory output with auto filename
./tts "Compatibility" -o audio/               # → audio/compatibility.wav
./tts "Test multiple words" -o audio/          # → audio/test_multiple_words.wav
./tts "Hello" -o /path/to/audio/             # → /path/to/audio/hello.wav

# Full file path still works
./tts "Hello world" -o audio/custom.wav      # → audio/custom.wav
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

**Manual usage (without setup):**
```bash
python tts_cli.py "Hello world" --output my_speech.wav
python tts_cli.py "Hello world" --check-updates
python tts_cli.py "Hello world" --model-name "tts_models/en/ljspeech/vits"
python tts_cli.py --info
python tts_cli.py "Hello world" --cpu
```

**Manual usage (with virtual environment):**
```bash
# Using virtual environment Python directly
./tts_venv/bin/python tts_cli.py "Hello world" --output my_speech.wav

# Or activate first
source tts_venv/bin/activate
python tts_cli.py "Hello world" --output my_speech.wav
python tts_cli.py "Hello world" --check-updates
python tts_cli.py "Hello world" --model-name "tts_models/en/ljspeech/vits"
python tts_cli.py --info
python tts_cli.py "Hello world" --cpu
```

### Command Line Options

- `text`: Text to convert to speech (optional if using --info)
- `--model-name`: TTS model to use (default: tts_models/en/ljspeech/vits)
- `--output, -o`: Output audio file path (auto-generated if not specified)
- `--check-updates`: Check for model updates before processing
- `--info`: Display model information and exit
- `--cpu`: Force CPU usage instead of GPU
- `--max-filename-length`: Maximum length for auto-generated filename (default: 20)

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

### Using the Virtual Environment

After setup, you can use the virtual environment directly:

**Activate virtual environment:**
```bash
# Linux/macOS
source tts_venv/bin/activate

# Windows
tts_venv\Scripts\activate
```

**Run TTS CLI with virtual environment:**
```bash
# Linux/macOS
source tts_venv/bin/activate && python tts_cli.py "Hello world"

# Windows
tts_venv\Scripts\activate && python tts_cli.py "Hello world"
```

**Direct virtual environment Python:**
```bash
# Linux/macOS
./tts_venv/bin/python tts_cli.py "Hello world"

# Windows
tts_venv\Scripts\python tts_cli.py "Hello world"
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

**Default locations:**
- Linux: `~/.local/share/tts/`
- macOS: `~/Library/Application Support/tts/`
- Windows: `%APPDATA%/tts/`

**Custom location:**
- Set via `COQUI_MODEL_PATH` environment variable
- Example: `export COQUI_MODEL_PATH="/path/to/your/models"`

**Virtual environment models:**
- Models are downloaded independently for each virtual environment
- The actual download location is determined by the Coqui TTS library based on OS

The tool displays the expected model location information on each run to help you track where models are stored.

## License

This project follows the same license as the Coqui TTS library.