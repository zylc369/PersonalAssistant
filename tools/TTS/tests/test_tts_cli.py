#!/usr/bin/env python3
"""
Test suite for TTS CLI functionality.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from tts_cli import TTSCLI
from model_updater import ModelUpdateChecker


class TestTTSCLI:
    """Test cases for TTS CLI functionality."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.test_text = "Hello world"
        self.test_output = "test_output.wav"
        self.test_model = "tts_models/en/ljspeech/vits"
    
    def test_init(self):
        """Test TTS CLI initialization."""
        cli = TTSCLI()
        assert cli.model_manager is not None
        assert cli.update_checker is not None
    
    def test_get_model_path_default(self):
        """Test default model path detection."""
        cli = TTSCLI()
        path = cli.get_model_path()
        expected = str(Path.home() / '.local' / 'share' / 'tts')
        assert path == expected
    
    @patch.dict(os.environ, {'COQUI_MODEL_PATH': '/custom/path'})
    def test_get_model_path_custom(self):
        """Test custom model path from environment."""
        cli = TTSCLI()
        path = cli.get_model_path()
        assert path == '/custom/path'
    
    @patch('tts_cli.logger')
    def test_check_model_updates(self, mock_logger):
        """Test model update checking."""
        cli = TTSCLI()
        
        # Mock the update checker
        with patch.object(cli.update_checker, 'check_for_updates', return_value=True):
            result = cli.check_model_updates("test_model")
            assert result is True
        
        with patch.object(cli.update_checker, 'check_for_updates', return_value=False):
            result = cli.check_model_updates("test_model")
            assert result is False
    
    @patch('tts_cli.logger')
    def test_generate_speech_empty_text(self, mock_logger):
        """Test speech generation with empty text."""
        cli = TTSCLI()
        result = cli.generate_speech("", self.test_output, self.test_model)
        assert result is False
    
    @patch('tts_cli.logger')
    def test_generate_speech_success(self, mock_logger):
        """Test successful speech generation."""
        cli = TTSCLI()
        
        # Mock model loading and TTS generation
        mock_tts = Mock()
        mock_tts.tts_to_file = Mock()
        
        with patch.object(cli, 'load_model', return_value=mock_tts):
            with patch.object(cli, 'get_model_path', return_value='/mock/path'):
                with patch.object(cli, 'check_model_updates', return_value=False):
                    result = cli.generate_speech(
                        self.test_text, self.test_output, self.test_model
                    )
                    assert result is True
                    mock_tts.tts_to_file.assert_called_once_with(
                        text=self.test_text, file_path=self.test_output
                    )
    
    @patch('tts_cli.logger')
    def test_generate_speech_with_updates(self, mock_logger):
        """Test speech generation with update check."""
        cli = TTSCLI()
        
        mock_tts = Mock()
        mock_tts.tts_to_file = Mock()
        
        with patch.object(cli, 'load_model', return_value=mock_tts):
            with patch.object(cli, 'get_model_path', return_value='/mock/path'):
                with patch.object(cli, 'check_model_updates', return_value=True) as mock_check:
                    result = cli.generate_speech(
                        self.test_text, self.test_output, self.test_model, 
                        check_updates=True
                    )
                    assert result is True
                    mock_check.assert_called_once_with(self.test_model)
    
    @patch('tts_cli.logger')
    def test_load_model_success(self, mock_logger):
        """Test successful model loading."""
        cli = TTSCLI()
        
        mock_tts = Mock()
        with patch('tts_cli.TTS', return_value=mock_tts):
            with patch('tts_cli.torch.cuda.is_available', return_value=False):
                result = cli.load_model(self.test_model, gpu=False)
                assert result == mock_tts
    
    @patch('tts_cli.logger')
    def test_load_model_failure(self, mock_logger):
        """Test model loading failure."""
        cli = TTSCLI()
        
        with patch('tts_cli.TTS', side_effect=Exception("Model not found")):
            with pytest.raises(RuntimeError, match="Model loading failed"):
                cli.load_model(self.test_model)
    
    @patch('builtins.print')
    def test_show_model_info(self, mock_print):
        """Test model information display."""
        cli = TTSCLI()
        
        # Mock update checker
        mock_models = [
            {'name': 'model1', 'last_modified_date': '2023-01-01'},
            {'name': 'model2', 'last_modified_date': '2023-01-02'}
        ]
        
        with patch.object(cli.update_checker, 'list_local_models', return_value=mock_models):
            with patch.object(cli, 'get_model_path', return_value='/mock/path'):
                with patch('tts_cli.TTS') as mock_tts_class:
                    mock_tts = Mock()
                    mock_tts.list_models.return_value = ['model1', 'model2', 'model3']
                    mock_tts_class.return_value = mock_tts
                    
                    cli.show_model_info(self.test_model)
                    
                    # Check that print was called
                    mock_print.assert_called()


class TestModelUpdateChecker:
    """Test cases for ModelUpdateChecker."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.checker = ModelUpdateChecker(self.temp_dir)
    
    def teardown_method(self):
        """Cleanup after each test method."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_init(self):
        """Test ModelUpdateChecker initialization."""
        assert self.checker.model_path == Path(self.temp_dir)
        assert self.checker.cache_file == Path(self.temp_dir) / ".model_cache.json"
    
    def test_load_cache_empty(self):
        """Test loading empty cache."""
        cache = self.checker.load_cache()
        assert cache == {}
    
    def test_save_and_load_cache(self):
        """Test saving and loading cache."""
        test_data = {'key': 'value', 'timestamp': 1234567890}
        self.checker.save_cache(test_data)
        
        loaded = self.checker.load_cache()
        assert loaded == test_data
    
    def test_get_local_model_info_not_found(self):
        """Test getting info for non-existent local model."""
        info = self.checker.get_local_model_info('nonexistent/model')
        assert info is None
    
    def test_get_local_model_info_exists(self):
        """Test getting info for existing local model."""
        # Create mock model directory and files
        model_dir = Path(self.temp_dir) / "tts_models--en--ljspeech--vits"
        model_dir.mkdir(parents=True)
        
        # Create mock files
        (model_dir / "model.pth").touch()
        (model_dir / "config.json").touch()
        
        info = self.checker.get_local_model_info('tts_models/en/ljspeech/vits')
        
        assert info is not None
        assert info['name'] == 'tts_models/en/ljspeech/vits'
        assert info['exists'] is True
        assert 'last_modified' in info
        assert 'files' in info
        assert len(info['files']) == 2
    
    def test_check_remote_model_info(self):
        """Test remote model info checking."""
        # This method returns None by default (no internet)
        info = self.checker.check_remote_model_info('test/model')
        assert info is None
    
    def test_check_for_updates_no_model(self):
        """Test update check for non-existent model."""
        result = self.checker.check_for_updates('nonexistent/model')
        assert result is False
    
    def test_check_for_updates_with_model(self):
        """Test update check for existing model."""
        # Create mock model
        model_dir = Path(self.temp_dir) / "tts_models--en--ljspeech--vits"
        model_dir.mkdir(parents=True)
        (model_dir / "model.pth").touch()
        
        result = self.checker.check_for_updates('tts_models/en/ljspeech/vits')
        assert result is False  # No remote info, so False
    
    def test_list_local_models_empty(self):
        """Test listing models when none exist."""
        models = self.checker.list_local_models()
        assert models == []
    
    def test_list_local_models_with_models(self):
        """Test listing existing local models."""
        # Create mock model directories
        model1_dir = Path(self.temp_dir) / "tts_models--en--ljspeech--vits"
        model2_dir = Path(self.temp_dir) / "tts_models--en--vctk--vits"
        model1_dir.mkdir(parents=True)
        model2_dir.mkdir(parents=True)
        
        # Create model files
        (model1_dir / "model.pth").touch()
        (model2_dir / "model.pth").touch()
        
        models = self.checker.list_local_models()
        assert len(models) == 2
        
        model_names = [m['name'] for m in models]
        assert 'tts_models/en/ljspeech/vits' in model_names
        assert 'tts_models/en/vctk/vits' in model_names
    
    def test_cleanup_cache(self):
        """Test cache cleanup."""
        # Create old cache entry
        old_data = {
            'old_key': {
                'timestamp': 1234567890,  # Very old timestamp
                'data': 'test'
            }
        }
        self.checker.save_cache(old_data)
        
        # Add recent entry
        recent_data = self.checker.load_cache()
        recent_data['recent_key'] = {
            'timestamp': 9999999999,  # Future timestamp
            'data': 'recent'
        }
        self.checker.save_cache(recent_data)
        
        # Clean up
        self.checker.cleanup_cache()
        
        # Check old entry is removed, recent remains
        cache = self.checker.load_cache()
        assert 'old_key' not in cache
        assert 'recent_key' in cache


if __name__ == "__main__":
    pytest.main([__file__])