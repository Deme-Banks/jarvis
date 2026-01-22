# JARVIS VS Code Extension

## Installation

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "JARVIS AI Assistant"
4. Click Install

Or install from command line:
```bash
code --install-extension jarvis-ai-assistant
```

## Features

### Commands

- **Generate Code** (Ctrl+Shift+J): Generate code from description
- **Explain Code** (Ctrl+Shift+E): Explain selected code
- **Fix Bugs**: Automatically fix bugs in code
- **Refactor**: Refactor code with AI assistance
- **Ask Question**: Ask JARVIS any coding question

### Usage

1. **Generate Code**:
   - Press `Ctrl+Shift+J` (or `Cmd+Shift+J` on Mac)
   - Describe what code you want
   - Code is inserted at cursor

2. **Explain Code**:
   - Select code
   - Right-click → "JARVIS: Explain Code"
   - Or press `Ctrl+Shift+E`

3. **Fix Bugs**:
   - Select code with bugs
   - Right-click → "JARVIS: Fix Bugs"
   - Bugs are automatically fixed

4. **Refactor**:
   - Select code to refactor
   - Right-click → "JARVIS: Refactor"
   - Choose refactoring type

## Configuration

Set JARVIS API URL in VS Code settings:
```json
{
  "jarvis.apiUrl": "http://localhost:5000",
  "jarvis.autoExplain": false
}
```

## Requirements

- JARVIS server running (default: http://localhost:5000)
- VS Code 1.74.0 or higher
