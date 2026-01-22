# AI Coding Guide

## Overview

JARVIS now includes AI-powered coding capabilities: code generation, reading/analysis, and building/compilation.

## Features

### 1. AI Code Generator
- Generate code from natural language
- Support for multiple languages
- Create functions and classes
- Voice command integration

### 2. AI Code Reader
- Read and analyze code files
- Explain what code does
- Find bugs and issues
- Suggest improvements
- Refactor code

### 3. AI Code Builder
- Build/compile code
- Syntax checking
- Create executables
- Run code
- Support for multiple languages

## Voice Commands

### Code Generation

```
"Generate code for a calculator in Python"
"Write a function to sort a list"
"Create a class for handling HTTP requests"
"Make code for a REST API in JavaScript"
"Generate Python code for file encryption"
```

### Code Reading/Analysis

```
"Read code in script.py"
"Analyze code in main.js"
"Explain what this code does"
"Review code in app.py"
"Find bugs in test.py"
"Suggest improvements for utils.py"
```

### Code Building

```
"Build script.py"
"Compile main.cpp"
"Build and run test.js"
"Create executable from app.py"
```

## Usage Examples

### Generate Code

```python
from ai_coding import AICodeGenerator

generator = AICodeGenerator()

# Generate from description
result = generator.generate_code(
    "Create a function to calculate fibonacci numbers",
    language="python"
)

# Generate from voice command
result = generator.generate_from_voice(
    "Generate code for a web scraper in Python"
)
```

### Read Code

```python
from ai_coding import AICodeReader

reader = AICodeReader()

# Read and analyze
result = reader.read_code("script.py")

# Explain code
explanation = reader.explain_code(code, language="python")

# Find bugs
bugs = reader.find_bugs(code, language="python")

# Suggest improvements
suggestions = reader.suggest_improvements(code, language="python")

# Refactor
refactored = reader.refactor_code(code, language="python")
```

### Build Code

```python
from ai_coding import AICodeBuilder

builder = AICodeBuilder()

# Build code
result = builder.build_code("script.py", language="python")

# Build with options
result = builder.build_code(
    "app.cpp",
    language="cpp",
    output_name="app",
    options={"optimize": True}
)

# Run code
result = builder.run_code("script.py", language="python")
```

## Supported Languages

### Code Generation
- Python
- JavaScript
- Java
- C/C++
- Go
- Rust
- Ruby
- PHP
- Swift
- Kotlin

### Code Building
- Python (syntax check, PyInstaller)
- JavaScript (Node.js)
- Java (javac)
- C/C++ (gcc/g++)
- Go (go build)
- Rust (rustc)

## Advanced Features

### Generate Function

```python
result = generator.generate_function(
    function_name="calculate_fibonacci",
    description="Calculate nth fibonacci number",
    parameters=["n"],
    return_type="int",
    language="python"
)
```

### Generate Class

```python
result = generator.generate_class(
    class_name="HTTPClient",
    description="HTTP client for making requests",
    methods=["get", "post", "put", "delete"],
    language="python"
)
```

### Custom Requirements

```python
result = generator.generate_code(
    "Create a REST API",
    language="python",
    requirements=[
        "Use Flask",
        "Include error handling",
        "Add authentication"
    ],
    style="clean"
)
```

## Integration

All features are integrated into JARVIS voice commands. Just speak naturally:

```
"Jarvis, generate code for a calculator"
"Jarvis, analyze code in script.py"
"Jarvis, build main.cpp"
```

## Best Practices

1. **Be specific** in code generation requests
2. **Review generated code** before using
3. **Test thoroughly** after building
4. **Use appropriate language** for your needs
5. **Check for bugs** before deployment

## Troubleshooting

### "Error generating code"
- Check LLM availability (OpenAI/Gemini or local)
- Be more specific in description
- Check API keys if using cloud LLMs

### "Build error"
- Ensure compiler is installed
- Check file path is correct
- Review error messages

### "File not found"
- Verify file path
- Check file exists
- Use absolute paths if needed

---

**Enjoy AI-powered coding with JARVIS!**
