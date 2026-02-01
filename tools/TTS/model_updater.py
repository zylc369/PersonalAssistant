#!/usr/bin/env python3
"""
Enhanced model update checker for TTS CLI Tool.

This module provides functionality to check for TTS model updates
by comparing local versions with remote repository information.
"""

import os
import json
import requests
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class ModelUpdateChecker:
    """Check for TTS model updates."""
    
    def __init__(self, model_path: str):
        """Initialize update checker.
        
        Args:
            model_path: Path where models are stored
        """
        self.model_path = Path(model_path)
        self.cache_file = self.model_path / ".model_cache.json"
        
    def load_cache(self) -> Dict[str, Any]:
        """Load cached model information."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load cache: {e}")
        return {}
    
    def save_cache(self, data: Dict[str, Any]) -> None:
        """Save model information to cache."""
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save cache: {e}")
    
    def get_local_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get information about local model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Dictionary with model info or None if not found
        """
        # Convert model name to directory name
        model_dir_name = model_name.replace('/', '--')
        model_dir = self.model_path / model_dir_name
        
        if not model_dir.exists():
            return None
            
        info = {
            'name': model_name,
            'path': str(model_dir),
            'exists': True
        }
        
        # Check for model files
        model_files = []
        for pattern in ['*.pth', '*.pt', '*.json', '*.ckpt']:
            model_files.extend(model_dir.glob(pattern))
        
        if model_files:
            # Get the most recently modified file as reference
            latest_file = max(model_files, key=lambda f: f.stat().st_mtime)
            info['last_modified'] = latest_file.stat().st_mtime
            info['last_modified_date'] = datetime.fromtimestamp(
                latest_file.stat().st_mtime
            ).strftime('%Y-%m-%d %H:%M:%S')
            info['files'] = [f.name for f in model_files]
        
        return info
    
    def check_remote_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Check remote model information.
        
        Args:
            model_name: Name of the model to check
            
        Returns:
            Dictionary with remote model info or None if unavailable
        """
        # This is a placeholder implementation
        # In a real scenario, you would:
        # 1. Check Coqui TTS GitHub releases
        # 2. Check Hugging Face model repository
        # 3. Compare version numbers or file hashes
        
        try:
            # For demonstration, we'll simulate a remote check
            # In practice, you might use requests to check GitHub API or Hugging Face API
            
            # Example GitHub API check (commented out as this requires internet):
            # url = f"https://api.github.com/repos/coqui-ai/TTS/releases"
            # response = requests.get(url, timeout=10)
            # if response.status_code == 200:
            #     releases = response.json()
            #     # Process releases to find model info
            
            # For now, return None to indicate no update info available
            return None
            
        except Exception as e:
            logger.warning(f"Failed to check remote model info: {e}")
            return None
    
    def check_for_updates(self, model_name: str, force_check: bool = False) -> bool:
        """
        Check if model updates are available.
        
        Args:
            model_name: Name of the model to check
            force_check: Force remote check regardless of cache
            
        Returns:
            True if updates available, False otherwise
        """
        cache = self.load_cache()
        cache_key = f"update_check_{model_name}"
        
        # Check if we recently checked (avoid too frequent checks)
        if not force_check and cache_key in cache:
            last_check = cache[cache_key].get('timestamp', 0)
            time_diff = datetime.now().timestamp() - last_check
            if time_diff < 3600:  # Don't check more than once per hour
                logger.info("Recently checked for updates, skipping")
                return cache[cache_key].get('updates_available', False)
        
        # Get local model info
        local_info = self.get_local_model_info(model_name)
        if not local_info:
            logger.info(f"Model {model_name} not found locally")
            return False
        
        # Get remote model info
        remote_info = self.check_remote_model_info(model_name)
        
        updates_available = False
        
        if remote_info:
            # Compare versions or timestamps
            # This is where you'd implement actual update logic
            # For now, we'll just compare modification times
            local_time = local_info.get('last_modified', 0)
            remote_time = remote_info.get('last_modified', 0)
            
            if remote_time > local_time:
                updates_available = True
                logger.info(f"Updates available for {model_name}")
            else:
                logger.info(f"Model {model_name} is up to date")
        else:
            logger.info("Could not check for updates (offline or API unavailable)")
        
        # Update cache
        cache[cache_key] = {
            'timestamp': datetime.now().timestamp(),
            'updates_available': updates_available
        }
        self.save_cache(cache)
        
        return updates_available
    
    def list_local_models(self) -> list:
        """List all locally available models."""
        models = []
        
        if not self.model_path.exists():
            return models
        
        for item in self.model_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                # Convert directory name back to model name
                model_name = item.name.replace('--', '/')
                info = self.get_local_model_info(model_name)
                if info:
                    models.append(info)
        
        return sorted(models, key=lambda x: x.get('name', ''))
    
    def cleanup_cache(self) -> None:
        """Clean up old cache entries."""
        try:
            if self.cache_file.exists():
                cache = self.load_cache()
                current_time = datetime.now().timestamp()
                
                # Remove entries older than 7 days
                keys_to_remove = []
                for key, value in cache.items():
                    if isinstance(value, dict) and 'timestamp' in value:
                        if current_time - value['timestamp'] > 7 * 24 * 3600:
                            keys_to_remove.append(key)
                
                for key in keys_to_remove:
                    del cache[key]
                
                self.save_cache(cache)
                logger.info(f"Cleaned up {len(keys_to_remove)} old cache entries")
                
        except Exception as e:
            logger.warning(f"Failed to cleanup cache: {e}")


if __name__ == "__main__":
    # Simple test
    logging.basicConfig(level=logging.INFO)
    
    # Create checker with default path
    default_path = Path.home() / '.local' / 'share' / 'tts'
    checker = ModelUpdateChecker(str(default_path))
    
    # List local models
    models = checker.list_local_models()
    print(f"Found {len(models)} local models:")
    for model in models:
        print(f"  - {model['name']}")
        if 'last_modified_date' in model:
            print(f"    Last modified: {model['last_modified_date']}")
        print(f"    Files: {', '.join(model.get('files', []))}")
    
    # Check for updates for first model
    if models:
        print(f"\nChecking updates for {models[0]['name']}...")
        updates = checker.check_for_updates(models[0]['name'])
        print(f"Updates available: {updates}")