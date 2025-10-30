"""
Configuration loader for the Appointment Reminder system.
Handles loading and parsing of YAML config files and environment variables.
"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any


class ConfigLoader:
    """Loads and manages application configuration."""
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        """Initialize config loader with path to settings file.
        
        Args:
            config_path: Path to the YAML configuration file
        """
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self._load_config()
        self._load_env()
    
    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f) or {}
    
    def _load_env(self) -> None:
        """Load environment variables from .env file."""
        load_dotenv()
        
        # Override config with environment variables if they exist
        env_config = {
            'twilio_account_sid': os.getenv('TWILIO_ACCOUNT_SID'),
            'twilio_auth_token': os.getenv('TWILIO_AUTH_TOKEN'),
            'twilio_phone_number': os.getenv('TWILIO_PHONE_NUMBER'),
            'google_voice_email': os.getenv('GOOGLE_VOICE_EMAIL'),
            'google_voice_password': os.getenv('GOOGLE_VOICE_PASSWORD'),
            'debug': os.getenv('DEBUG', 'false').lower() == 'true'
        }
        
        # Store in config under 'env' key
        if 'env' not in self.config:
            self.config['env'] = {}
        self.config['env'].update(env_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key path (e.g., 'scheduling.reminder_hours_before').
        
        Args:
            key: Dot-separated key path
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-style access."""
        return self.config[key]
    
    def __contains__(self, key: str) -> bool:
        """Check if key exists in config."""
        return key in self.config

