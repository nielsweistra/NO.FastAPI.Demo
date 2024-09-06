# Configuration Management with Pydantic and YAML

This project demonstrates how to manage configuration settings using Pydantic and YAML files, with environment variable support.

## Overview

The `Settings` class uses Pydantic to define configuration settings. It supports loading configuration from a YAML file and overriding values with environment variables. Additionally, it handles extra fields dynamically.

## Key Features

- **Default Values**: Provides default values for configuration settings.
- **YAML Configuration**: Loads settings from a `config.yaml` file.
- **Environment Variables**: Allows settings to be overridden by environment variables with a specified prefix.
- **Dynamic Extra Fields**: Handles additional configuration fields not predefined in the `Settings` class.

## Directory Structure
```bash
/project-root
│
├── /base
│   ├── /settings
│   │   ├── config.py          # Contains Settings class with .env and YAML support
│   │   ├── config.yaml        # YAML configuration file
│   │   └── __init__.py        # Package initialization
│   │
│
├── .env                       # Environment variables file
├── main.py                    # Example script demonstrating the use of Settings
└── requirements.txt           # Python dependencies
```

## Code Structure

### `settings.py`

This file contains the `Settings` class which handles configuration:

```python
from pydantic_settings import BaseSettings
from pydantic import Extra, BaseModel
import yaml
from pathlib import Path
import os

class ExtraFieldsModel(BaseModel):
    """Model to store extra fields dynamically."""
    class Config:
        extra = 'allow'

class Settings(BaseSettings):
    host: str = "0.0.0.0"  # Default value
    port: int = 8000        # Default value
    debug: bool = False
    database_url: str = ""
    capture_fastapi_logs: bool = True  # Option to capture FastAPI logs
    extra_fields: ExtraFieldsModel = ExtraFieldsModel()  # Initialize extra fields container

    class Config:
        env_file = ".env"  # Optional: support .env file
        env_file_encoding = 'utf-8'
        extra = 'allow'  # Allow extra fields

    @classmethod
    def from_yaml(cls, file_path: str):
        # Load data from YAML file
        with open(file_path, 'r') as f:
            config_data = yaml.safe_load(f) or {}

        # Fetch environment variables with the prefix APP__
        env_prefix = "APP__"
        env_vars = {
            "host": os.getenv(f"{env_prefix}HOST", config_data.get("host", cls.host)),
            "port": int(os.getenv(f"{env_prefix}PORT", config_data.get("port", cls.port))),
            "debug": os.getenv(f"{env_prefix}DEBUG", str(config_data.get("debug", cls.debug))).lower() in ['true', '1', 't'],
            "database_url": os.getenv(f"{env_prefix}DATABASE_URL", config_data.get("database_url", cls.database_url)),
            "capture_fastapi_logs": os.getenv(f"{env_prefix}CAPTURE_FASTAPI_LOGS", str(config_data.get("capture_fastapi_logs", cls.capture_fastapi_logs))).lower() in ['true', '1', 't']
        }

        # Update config_data with environment variables
        config_data.update(env_vars)

        # Separate known fields and extra fields
        known_fields = {k: config_data[k] for k in cls.__annotations__.keys() if k in config_data}
        extra_fields = {k: v for k, v in config_data.items() if k not in cls.__annotations__}

        # Create an instance of Settings with known fields
        settings_instance = cls(**known_fields)

        # Assign extra fields dynamically to the extra_fields model
        if extra_fields:
            settings_instance.extra_fields = ExtraFieldsModel(**extra_fields)
        return settings_instance

    def print_extra_fields(self):
        """Method to return extra fields found in the configuration as a comma-separated string."""
        extra_fields_dict = self.extra_fields.dict()  # Use dict() method to access extra fields
        
        # If there are no extra fields, return an empty string
        if not extra_fields_dict:
            return ""

        # Convert extra fields to a comma-separated string
        extra_fields_str = ", ".join(f"{field_name}: {field_value}" for field_name, field_value in extra_fields_dict.items())
        
        return f"Extra fields found: {extra_fields_str}"

# Load settings from the YAML file
yaml_path = Path(__file__).parent / "config.yaml"
settings = Settings.from_yaml(yaml_path)
```

### `main.py`

A basic script to demonstrate usage:

```python
from base.settings.settings import settings

# Print configuration details
print(f"Host: {settings.host}")
print(f"Port: {settings.port}")
print(f"Debug: {settings.debug}")
print(f"Database URL: {settings.database_url}")
print(f"Capture FastAPI Logs: {settings.capture_fastapi_logs}")

# Print extra fields if available
extra_fields_message = settings.print_extra_fields()
if extra_fields_message:
    print(extra_fields_message)
```

## Environment Variables

To override settings using environment variables, use the `APP__` prefix. For example:

- `APP__HOST=127.0.0.1`
- `APP__PORT=5000`
- `APP__DEBUG=True`
- `APP__DATABASE_URL=postgres://user:pass@localhost/db`
- `APP__CAPTURE_FASTAPI_LOGS=False`

## YAML Configuration File (`config.yaml`)

Example `config.yaml`:

```yaml
host: "localhost"
port: 8080
debug: true
database_url: "sqlite:///example.db"
capture_fastapi_logs: true
extra_field_1: "value1"
extra_field_2: "value2"
```

## Summary

This configuration management setup allows you to dynamically handle application settings with Pydantic and YAML, while also supporting environment variable overrides. Use the provided `Settings` class to load, manage, and access your configuration efficiently.

---

> This is a demo, feel free to use and contribute!

[Niels Weistra] @ [ITlusions]

   [ITlusions]: <https://github.com/ITlusions>
   [Niels Weistra]: <mailto:n.weistra@itlusions.com>