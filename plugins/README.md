# JARVIS Plugin System

## Overview

Extensible plugin system for adding custom functionality to JARVIS.

## Creating a Plugin

### 1. Create Plugin File

Create a file in the `plugins/` directory:

```python
# plugins/my_plugin.py
from plugins.plugin_system import PluginBase

class MyPlugin(PluginBase):
    def __init__(self):
        super().__init__("my_plugin", "My Custom Plugin")
    
    def initialize(self):
        return self
    
    def execute(self, command: str, args: Dict) -> Any:
        if command == "hello":
            return {"message": "Hello from my plugin!"}
        return {"error": "Unknown command"}

def initialize():
    return MyPlugin()
```

### 2. Register Plugin

```python
from plugins.plugin_system import PluginSystem

plugin_system = PluginSystem()
plugin_system.register_plugin(
    plugin_id="my_plugin",
    name="My Custom Plugin",
    version="1.0.0",
    author="Your Name",
    description="A custom plugin for JARVIS",
    entry_point="plugins.my_plugin",
    commands=["hello", "process"]
)
```

### 3. Load and Use

```python
# Load plugin
plugin_system.load_plugin("my_plugin")

# Execute command
result = plugin_system.execute_plugin_command("my_plugin", "hello")
```

## Plugin Structure

- **PluginBase**: Base class for all plugins
- **initialize()**: Called when plugin is loaded
- **execute()**: Called when plugin command is executed
- **get_info()**: Returns plugin information

## Example Plugins

See `plugins/example_plugin.py` for a complete example.

## Plugin Marketplace (Future)

- Plugin discovery
- Installation system
- Rating and reviews
- Version management
- Automatic updates
