
# Configuration Management the implementation supports `.env` files

Yes, the implementation supports `.env` files. Here’s a brief explanation of how it works and how you can use it:

### `.env` File Support

In the `Settings` class, the `Config` inner class includes the `env_file` configuration, which specifies that `.env` files should be used to load environment variables.

### How It Works

1. **Environment Variable Loading**: The `env_file = ".env"` setting in the `Config` class instructs Pydantic to read the environment variables from a `.env` file if it exists. This is done automatically when the `Settings` class is initialized.
  
2. **Overriding with `.env` Variables**: Environment variables from the `.env` file will override any values defined in the `config.yaml` file or the default values in the `Settings` class.

### Example `.env` File

Create a `.env` file in the same directory as `settings.py` with the following content:

```env
APP__HOST=127.0.0.1
APP__PORT=5000
APP__DEBUG=True
APP__DATABASE_URL=postgres://user:pass@localhost/db
APP__CAPTURE_FASTAPI_LOGS=False
```

### Using `.env` with the Existing Implementation

Here's how the `Settings` class will incorporate `.env` values:

1. **Load `.env` Values**: When the `Settings` class is instantiated, it will automatically read from the `.env` file, thanks to the `env_file` setting.

2. **Override Values**: The environment variables from the `.env` file will override any corresponding values in the `config.yaml` file or the default values specified in the class.

### Example Usage

Here’s a snippet from `main.py` showing how to use the settings:

```python
from base.settings.config import settings

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

### Summary

The `.env` file support is integrated through Pydantic’s `BaseSettings`, making it straightforward to manage environment-specific settings and easily override default or YAML configuration values.

---
> This is a demo, feel free to use and contribute!

[Niels Weistra] @ [ITlusions]

   [ITlusions]: <https://github.com/ITlusions>
   [Niels Weistra]: <mailto:n.weistra@itlusions.com>