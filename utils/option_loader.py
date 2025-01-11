from dataclasses import dataclass
from typing import Dict, Any
import json
from pathlib import Path

class OptionLoader:
    def __init__(self, config_path: str = "configs.json"):
        """Initialize TestConfig by reading the config file.
        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config file is not valid JSON
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load and parse the config file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found at: {self.config_path}")
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_module_options(self, module_name: str) -> Dict[str, Any]:
        """Get configuration for a specific module.
        Args:
            module_name: Name of the test module (e.g., "test_login.py")
        """
        try:
            return self.config["modules"][module_name]["options"]
        except KeyError:
            raise KeyError(f"No configuration found for module: {module_name}")
        
    def get_module_metadata(self, module_name: str) -> Dict[str, Any]:
        """Get a value from the metadata of a specific module.
        """
        return self.config["modules"][module_name]["metadata"]
    
    def get_module_all(self, module_name=None) -> Dict[str, Any]:
        if not module_name:
            return self.config["modules"]
        else:
            return self.config["modules"][module_name]

    def get_basic_setting(self) -> Dict[str, Any]:
        """Get values from the basic settings section.
        Raises:
            KeyError: If setting is not found
        """
        return self.config["basic"]
    
        
    def should_run_module(self, module_name: str) -> bool:
        """Check if a module should be run based on configuration.
        """
        try:
            return self.get_module_options(module_name).get('run', True)
        except KeyError:
            return True  # Default to True if module not found in config
    
if __name__ == "__main__":
    loader = OptionLoader("../configs.json")
    for cf in loader.config.items():
        print(cf)
