# AGENTS.md - TTS CLI Tool Guidelines

## Project Overview
This is a Text-to-Speech CLI tool using Coqui TTS for English learning. The tool converts words and sentences to speech, displays model locations, and supports model update checks.

## Commands

### Development Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run the CLI tool
python tts_cli.py "Hello world"

# Run with model update check
python tts_cli.py "Hello world" --check-updates

# Run with specific model
python tts_cli.py "Hello world" --model-name "tts_models/en/ljspeech/vits"

# Run with custom output path
python tts_cli.py "Hello world" --output "custom_output.wav"

# Check model information only
python tts_cli.py --info

# Run tests
python -m pytest tests/

# Run single test
python -m pytest tests/test_tts_cli.py::test_function_name

# Code formatting
black *.py

# Type checking
mypy *.py

# Linting
pylint *.py

# Install development dependencies
pip install -r requirements-dev.txt
```

## Code Style Guidelines

### Import Organization
```python
# Standard library imports first
import os
import sys
from pathlib import Path

# Third-party imports
import torch
from TTS.api import TTS
import argparse

# Local imports (if any)
from .utils import helper_function
```

### Type Annotations
```python
from typing import Optional, Dict, List, Union
from pathlib import Path

def generate_speech(
    text: str,
    model_name: str,
    output_path: Optional[Union[str, Path]] = None,
    check_updates: bool = False
) -> Path:
    """Generate speech from text using TTS."""
    pass
```

### Naming Conventions
- **Variables and functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private members**: `_leading_underscore`
- **Files**: `snake_case.py`

### Error Handling
```python
import logging
from TTS.utils.manage import ModelManager

def load_model(model_name: str) -> TTS:
    """Load TTS model with proper error handling."""
    try:
        tts = TTS(model_name=model_name)
        return tts
    except Exception as e:
        logging.error(f"Failed to load model {model_name}: {e}")
        raise RuntimeError(f"Model loading failed: {e}")
```

### Function Documentation
```python
def generate_speech(text: str, output_path: Path) -> bool:
    """
    Generate speech from text and save to file.
    
    Args:
        text: Input text to convert to speech
        output_path: Path where audio file will be saved
        
    Returns:
        True if successful, False otherwise
        
    Raises:
        ValueError: If text is empty
        RuntimeError: If TTS generation fails
    """
    pass
```

### Code Structure
```python
#!/usr/bin/env python3
"""
TTS CLI Tool - Text to Speech conversion for English learning.

This module provides command-line interface for converting English text
to speech using Coqui TTS models.
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the CLI tool."""
    parser = setup_arg_parser()
    args = parser.parse_args()
    
    try:
        process_args(args)
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

## Model Management

### Model Paths
- **Default location**: `~/.local/share/tts/`
- **Custom path**: Set `COQUI_MODEL_PATH` environment variable
- **Check location**: Use `--info` flag to display current model paths

### Model Update Check
```python
def check_model_updates(model_name: str) -> bool:
    """
    Check if model updates are available.
    
    Args:
        model_name: Name of the model to check
        
    Returns:
        True if updates available, False otherwise
    """
    try:
        manager = ModelManager()
        # Implementation depends on Coqui TTS API
        return False  # Placeholder
    except Exception as e:
        logger.warning(f"Could not check for updates: {e}")
        return False
```

## Testing Guidelines

### Test Structure
```python
import pytest
from unittest.mock import Mock, patch
from pathlib import Path

class TestTTSCLI:
    """Test cases for TTS CLI functionality."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.test_text = "Hello world"
        self.test_output = Path("test_output.wav")
    
    def test_generate_speech_success(self):
        """Test successful speech generation."""
        pass
    
    @patch('tts_cli.TTS')
    def test_model_loading_error(self, mock_tts):
        """Test error handling for model loading."""
        mock_tts.side_effect = Exception("Model not found")
        # Test implementation
```

### Test Coverage Requirements
- All public functions must have tests
- Error handling paths must be tested
- Command-line argument parsing tests
- Model management functionality tests

## Environment Setup

### Requirements Files
```txt
# requirements.txt
TTS>=0.22.0
torch>=2.0.0
numpy>=1.21.0

# requirements-dev.txt
pytest>=7.0.0
black>=23.0.0
mypy>=1.0.0
pylint>=2.17.0
```

### Virtual Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## CLI Interface Standards

### Argument Parsing
```python
def setup_arg_parser() -> argparse.ArgumentParser:
    """Setup and return argument parser."""
    parser = argparse.ArgumentParser(
        description="Text-to-Speech CLI for English learning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  tts_cli.py "Hello world"
  tts_cli.py "Hello world" --output custom.wav --check-updates
  tts_cli.py --info
        """
    )
    
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to convert to speech"
    )
    
    parser.add_argument(
        "--model-name",
        default="tts_models/en/ljspeech/vits",
        help="TTS model to use (default: tts_models/en/ljspeech/vits)"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output audio file path"
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
    
    return parser
```

## Performance Considerations

### Memory Management
- Clear model cache when switching models
- Use lazy loading for large models
- Implement proper cleanup in error scenarios

### GPU Support
- Detect CUDA availability automatically
- Fallback to CPU if GPU unavailable
- Provide clear messages about device usage

## Security Guidelines

### Input Validation
- Sanitize text inputs to prevent injection
- Validate file paths for directory traversal
- Limit text length to prevent resource exhaustion

### Model Security
- Only use models from trusted sources
- Verify model checksums if available
- Avoid downloading models from untrusted URLs