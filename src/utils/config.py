# CONFIGURATION MANAGEMENT
import os
import yaml
from pathlib import Path
from typing import Any, Dict


class Config:
    """
    Configuration manager for the application
    Loads from YAML files and environment variables
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize configuration
        
        Args:
            config_path: Path to YAML configuration file
        """
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self):
        """Load configuration from YAML file"""
        pass
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Supports nested keys with dot notation: 'database.url'
        Environment variables override file config
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        pass
    
    @property
    def database_url(self) -> str:
        """Get database connection string"""
        pass
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        pass
