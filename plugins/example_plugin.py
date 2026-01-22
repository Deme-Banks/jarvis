"""
Example Plugin - Template for creating plugins
"""
from plugins.plugin_system import PluginBase


class ExamplePlugin(PluginBase):
    """Example plugin for JARVIS"""
    
    def __init__(self):
        super().__init__("example_plugin", "Example Plugin")
    
    def initialize(self):
        """Initialize plugin"""
        print(f"Initializing {self.name}")
        return self
    
    def execute(self, command: str, args: Dict) -> Any:
        """Execute plugin command"""
        if command == "hello":
            return {"message": f"Hello from {self.name}!"}
        elif command == "process":
            data = args.get("data", "")
            return {"processed": data.upper()}
        else:
            return {"error": f"Unknown command: {command}"}


def initialize():
    """Plugin entry point"""
    return ExamplePlugin()
