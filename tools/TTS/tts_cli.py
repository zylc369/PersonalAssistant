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

try:
    from TTS.api import TTS
    from TTS.utils.manage import ModelManager
    import torch
    from model_updater import ModelUpdateChecker
except ImportError as e:
    print("Error: TTS package not found. Please install with: pip install TTS")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True  # Force basicConfig even if logging is already configured
)
logger = logging.getLogger(__name__)

# Make our logger more verbose to ensure we see the output
logger.setLevel(logging.INFO)


class TTSCLI:
    """Main TTS CLI application class."""
    
    def __init__(self):
        """Initialize TTS CLI."""
        self.tts: Optional[TTS] = None
        self.model_manager = ModelManager()
        model_path = self.get_model_path()
        self.update_checker = ModelUpdateChecker(model_path)
        
    def get_model_path(self) -> str:
        """Get the model storage path."""
        # Check environment variable first
        custom_path = os.environ.get('COQUI_MODEL_PATH')
        if custom_path and os.path.exists(custom_path):
            return custom_path
        
        # Use Coqui TTS ModelManager to get the actual model path
        return str(self.model_manager.output_prefix)
    
    def check_model_updates(self, model_name: str) -> bool:
        """
        Check if model updates are available.
        
        Args:
            model_name: Name of the model to check
            
        Returns:
            True if updates available, False otherwise
        """
        try:
            logger.info("Checking for model updates...")
            return self.update_checker.check_for_updates(model_name)
        except Exception as e:
            logger.warning(f"Could not check for updates: {e}")
            return False
    
    def load_model(self, model_name: str, gpu: bool = True) -> TTS:
        """
        Load TTS model with proper error handling.
        
        Args:
            model_name: Name of the model to load
            gpu: Whether to use GPU acceleration
            
        Returns:
            Loaded TTS model
            
        Raises:
            RuntimeError: If model loading fails
        """
        try:
            device = "cuda" if gpu and torch.cuda.is_available() else "cpu"
            logger.info(f"Loading model: {model_name}")
            logger.info(f"Using device: {device}")
            
            tts = TTS(model_name=model_name).to(device)
            return tts
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            raise RuntimeError(f"Model loading failed: {e}")
    
    def generate_speech(self, text: str, output_path: str, model_name: str, 
                       check_updates: bool = False, gpu: bool = True) -> bool:
        """
        Generate speech from text and save to file.
        
        Args:
            text: Input text to convert to speech
            output_path: Path where audio file will be saved
            model_name: TTS model to use
            check_updates: Whether to check for model updates
            gpu: Whether to use GPU acceleration
            
        Returns:
            True if successful, False otherwise
        """
        if not text.strip():
            logger.error("Text cannot be empty")
            return False
            
        if check_updates:
            self.check_model_updates(model_name)
        
        try:
            # Load model
            self.tts = self.load_model(model_name, gpu)
            
            # Display model location
            model_path = self.get_model_path()
            print(f"[INFO] Model location: {model_path}")
            print(f"[INFO] Model files stored in: {model_path}/{model_name.replace('/', '--')}")
            
            # Generate speech
            print(f"[INFO] Generating speech for: '{text[:50]}{'...' if len(text) > 50 else ''}'")
            print(f"[INFO] Output file: {output_path}")
            
            # Use tts_to_file for direct file output
            if self.tts is not None:
                self.tts.tts_to_file(text=text, file_path=output_path)
            else:
                raise RuntimeError("Failed to load TTS model")
            
            print(f"[INFO] Speech generated successfully: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate speech: {e}")
            return False
    
    def show_model_info(self, model_name: str) -> None:
        """Display model information and paths."""
        model_path = self.get_model_path()
        print(f"TTS Model Information:")
        print(f"  Model name: {model_name}")
        print(f"  Model storage path: {model_path}")
        print(f"  Model directory: {model_path}/{model_name.replace('/', '--')}")
        print(f"  Custom model path (COQUI_MODEL_PATH): {os.environ.get('COQUI_MODEL_PATH', 'Not set')}")
        
        # List local models
        try:
            local_models = self.update_checker.list_local_models()
            if local_models:
                print(f"\nLocal models ({len(local_models)} total):")
                for model in local_models:
                    print(f"  - {model['name']}")
                    if 'last_modified_date' in model:
                        print(f"    Last modified: {model['last_modified_date']}")
            else:
                print("\nNo local models found")
        except Exception as e:
            logger.warning(f"Could not list local models: {e}")
        
        # List available remote models
        try:
            models = TTS().list_models()
            print(f"\nAvailable remote models ({len(models)} total):")
            en_models = [m for m in models if m.startswith('tts_models/en/')]
            for model in en_models[:10]:  # Show first 10 English models
                print(f"  - {model}")
            if len(en_models) > 10:
                print(f"  ... and {len(en_models) - 10} more English models")
        except Exception as e:
            logger.warning(f"Could not list remote models: {e}")


def generate_filename_from_text(text: str, max_length: int = 20) -> str:
    """Generate a filename from text by taking first words and limiting length.
    
    Args:
        text: Input text to convert to filename
        max_length: Maximum filename length (excluding .wav extension)
        
    Returns:
        Generated filename string
    """
    import re
    
    # Remove non-alphanumeric characters except spaces and common punctuation
    cleaned_text = re.sub(r'[^\w\s\-\'"]', '', text)
    
    # Take first few words and limit length
    words = cleaned_text.split()[:5]  # Max 5 words
    base_name = '_'.join(words)
    
    # Truncate if too long
    if len(base_name) > max_length:
        base_name = base_name[:max_length]
    
    # Remove trailing underscores and make lowercase
    base_name = base_name.rstrip('_').lower()
    
    return f"{base_name}.wav"


def process_output_path(output_path: str, text: str, max_filename_length: int = 20) -> str:
    """Process output path - handle directory-only case and generate filename if needed.
    
    Args:
        output_path: User-provided output path
        text: Input text for filename generation
        max_filename_length: Maximum filename length
        
    Returns:
        Final output file path
    """
    from pathlib import Path
    import os
    
    path_obj = Path(output_path)
    
    # Check if path looks like a directory (ends with slash or doesn't have extension)
    if (output_path.endswith('/') or output_path.endswith('\\') or 
        not any(output_path.lower().endswith(ext) for ext in ['.wav', '.mp3', '.ogg'])):
        
        # Directory case: ensure directory exists, then generate filename
        if not path_obj.exists():
            try:
                path_obj.mkdir(parents=True, exist_ok=True)
                print(f"[INFO] Created directory: {path_obj}")
            except OSError as e:
                print(f"[ERROR] Failed to create directory {path_obj}: {e}")
                return output_path
        
        filename = generate_filename_from_text(text, max_filename_length)
        return str(path_obj / filename)
    else:
        # File case: ensure parent directory exists
        parent_dir = path_obj.parent
        if parent_dir and not parent_dir.exists():
            try:
                parent_dir.mkdir(parents=True, exist_ok=True)
                print(f"[INFO] Created parent directory: {parent_dir}")
            except OSError as e:
                print(f"[ERROR] Failed to create parent directory {parent_dir}: {e}")
        
        return output_path


def setup_arg_parser() -> argparse.ArgumentParser:
    """Setup and return argument parser."""
    parser = argparse.ArgumentParser(
        description="Text-to-Speech CLI for English learning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  tts_cli.py "Hello world"                    # Outputs: hello_world.wav
  tts_cli.py "How are you today"              # Outputs: how_are_you_today.wav
  tts_cli.py "This is a very long sentence" --output custom.wav
  tts_cli.py "Hello" --check-updates
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
        help="Output audio file path (if not specified, auto-generated from text)"
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
    
    return parser


def process_args(args) -> None:
    """Process command line arguments."""
    cli = TTSCLI()
    
    if args.info:
        cli.show_model_info(args.model_name)
        return
    
    if not args.text:
        logger.error("Text is required unless using --info flag")
        sys.exit(1)
    
    # Process output path (handle directory case)
    if args.output:
        args.output = process_output_path(args.output, args.text, args.max_filename_length)
    else:
        # Generate filename if not provided
        args.output = generate_filename_from_text(args.text, args.max_filename_length)
    
    # Generate speech
    success = cli.generate_speech(
        text=args.text,
        output_path=args.output,
        model_name=args.model_name,
        check_updates=args.check_updates,
        gpu=not args.cpu
    )
    
    if not success:
        sys.exit(1)


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
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()