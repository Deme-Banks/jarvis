# Claude Code Setup Guide for Jarvis Voice System

This guide explains how to set up and use the [everything-claude-code](https://github.com/affaan-m/everything-claude-code) configurations in this project.

## What is Everything Claude Code?

A complete collection of Claude Code configurations including:
- **Agents**: Specialized subagents for planning, code review, security, TDD, etc.
- **Skills**: Workflow definitions and domain knowledge
- **Commands**: Slash commands like `/tdd`, `/plan`, `/code-review`
- **Rules**: Always-follow guidelines for security, coding style, testing
- **Hooks**: Trigger-based automations
- **MCPs**: Model Context Protocol server configurations

## Quick Setup

### Option 1: Install as Plugin (Recommended)

1. Open Claude Code settings: `~/.claude/settings.json`

2. Add the marketplace and enable the plugin:

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

3. Or use commands in Claude Code:
```
/plugin marketplace add affaan-m/everything-claude-code
/plugin install everything-claude-code@everything-claude-code
```

### Option 2: Manual Installation

If you prefer manual control:

1. Clone the repository:
```bash
git clone https://github.com/affaan-m/everything-claude-code.git
```

2. Copy components to your Claude config:
```bash
# Copy agents
cp everything-claude-code/agents/*.md ~/.claude/agents/

# Copy rules
cp everything-claude-code/rules/*.md ~/.claude/rules/

# Copy commands
cp everything-claude-code/commands/*.md ~/.claude/commands/

# Copy skills
cp -r everything-claude-code/skills/* ~/.claude/skills/
```

3. Add hooks to `~/.claude/settings.json` (copy from `hooks/hooks.json`)

4. Configure MCPs in `~/.claude.json` (copy from `mcp-configs/mcp-servers.json`)

## Available Features

### Commands

- `/tdd` - Test-driven development workflow
- `/plan` - Implementation planning with structured approach
- `/e2e` - End-to-end test generation
- `/code-review` - Quality and security code review
- `/build-fix` - Fix build errors automatically
- `/refactor-clean` - Remove dead code and refactor

### Agents

- **planner.md** - Feature implementation planning
- **architect.md** - System design decisions
- **code-reviewer.md** - Quality and security review
- **security-reviewer.md** - Vulnerability analysis
- **tdd-guide.md** - Test-driven development
- **build-error-resolver.md** - Fix build errors
- **e2e-runner.md** - Playwright E2E testing
- **refactor-cleaner.md** - Dead code cleanup
- **doc-updater.md** - Documentation sync

### Rules

- **security.md** - Mandatory security checks
- **coding-style.md** - Immutability, file organization
- **testing.md** - TDD, 80% coverage requirement
- **git-workflow.md** - Commit format, PR process
- **agents.md** - When to delegate to subagents
- **performance.md** - Model selection, context management

## Project-Specific Notes

### Context Window Management

**Important**: Don't enable all MCPs at once. Your 200k context window can shrink to 70k with too many tools enabled.

Best practices:
- Have 20-30 MCPs configured
- Keep under 10 enabled per project
- Under 80 tools active total
- Use `disabledMcpServers` in project config to disable unused ones

### Python Project Considerations

This is a Python-based voice system. The configurations work well with:
- Python PEP 8 style guidelines
- Type hints
- Test coverage requirements
- Security-first approach

## Usage Examples

### Using TDD Workflow

```
/tdd Add voice command recognition feature
```

This will:
1. Define interfaces first
2. Write failing tests (RED)
3. Implement minimal code (GREEN)
4. Refactor (IMPROVE)
5. Verify 80%+ coverage

### Planning a Feature

```
/plan Implement multi-language support
```

The planner agent will:
- Break down the feature into tasks
- Identify dependencies
- Suggest implementation approach
- Create a structured plan

### Code Review

```
/code-review
```

The code reviewer will:
- Check for quality issues
- Security vulnerabilities
- Maintainability concerns
- Suggest improvements

## Resources

- **Repository**: https://github.com/affaan-m/everything-claude-code
- **Shorthand Guide**: [The Shorthand Guide to Everything Claude Code](https://affaanmustafa.com/claude-code-shorthand) - Start here!
- **Longform Guide**: [The Longform Guide to Everything Claude Code](https://affaanmustafa.com/claude-code-longform) - Advanced techniques

## Customization

These configs are battle-tested but should be customized for your workflow:

1. Start with what resonates
2. Modify for your stack (Python voice system)
3. Remove what you don't use
4. Add your own patterns

## Contributing

If you improve these configurations for this project, consider:
- Documenting custom patterns
- Sharing useful hooks
- Contributing back to the main repository

---

**Note**: Read both guides (Shorthand and Longform) to get the most out of these configurations!
