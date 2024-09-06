# /base/settings/settings.py
from pydantic_settings import BaseSettings
from pydantic import Extra, BaseModel
import yaml
from pathlib import Path

class ExtraFieldsModel(BaseModel):
    """Model to store extra fields dynamically."""
    class Config:
        extra = 'allow'

class Settings(BaseSettings):
    host: str
    port: int
    debug: bool
    database_url: str
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
            config_data = yaml.safe_load(f)

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
        extra_fields_dict = self.extra_fields.model_dump()  # Use dict() method to access extra fields
        
        # If there are no extra fields, return an empty string
        if not extra_fields_dict:
            return ""

        # Convert extra fields to a comma-separated string
        extra_fields_str = ", ".join(f"{field_name}: {field_value}" for field_name, field_value in extra_fields_dict.items())
        
        return f"Extra fields found: {extra_fields_str}"

# Load settings from the YAML file
yaml_path = Path(__file__).parent / "config.yaml"
settings = Settings.from_yaml(yaml_path)
