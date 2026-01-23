# Jarvis Voice System - Claude Code Configuration

This project uses the [everything-claude-code](https://github.com/affaan-m/everything-claude-code) plugin for enhanced development workflows.

## Plugin Setup

To use the everything-claude-code configurations, add this to your `~/.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "everything-claude-code": {
      "source": {
        "source": "github",
        "repo": "affaan-m/everything-claude-code"
      }
    }
  },
  "enabledPlugins": {
    "everything-claude-code@everything-claude-code": true
  }
}
```

Or install via command:
```
/plugin marketplace add affaan-m/everything-claude-code
/plugin install everything-claude-code@everything-claude-code
```

## Project-Specific Configuration

### Context Window Management

This project is a Python-based voice system with multiple modules. Keep MCP servers to a minimum to preserve context window:

- Recommended: Keep under 10 MCPs enabled
- Under 80 tools active total
- Use `disabledMcpServers` for unused integrations

### Project Structure

- **Python modules**: `agents/`, `ai/`, `voice/`, `features/`, etc.
- **Web components**: `web/`, `vscode-extension/`
- **Documentation**: `docs/`
- **Testing**: `testing/`

### Coding Standards

- Follow Python PEP 8 style guidelines
- Use type hints where applicable
- Maintain 80%+ test coverage
- Security-first approach (see `security/` directory)

### Available Commands

- `/tdd` - Test-driven development workflow
- `/plan` - Implementation planning
- `/code-review` - Quality and security review
- `/build-fix` - Fix build errors
- `/refactor-clean` - Dead code removal

### Agents

Specialized agents available for:
- Planning and architecture
- Code review and security
- TDD workflow
- Build error resolution
- E2E testing
- Documentation updates

## Resources

- **Shorthand Guide**: [The Shorthand Guide to Everything Claude Code](https://affaanmustafa.com/claude-code-shorthand)
- **Longform Guide**: [The Longform Guide to Everything Claude Code](https://affaanmustafa.com/claude-code-longform)
- **Repository**: https://github.com/affaan-m/everything-claude-code
