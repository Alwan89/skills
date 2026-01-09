# CLAUDE.md

This file provides guidance for AI assistants working with this repository.

## Repository Overview

This repository contains **Anthropic's official implementation of Skills for Claude** - modular packages that extend Claude's capabilities with specialized knowledge, workflows, and tool integrations. Skills teach Claude how to complete specific tasks in a repeatable way.

For the Agent Skills specification, see [agentskills.io](https://agentskills.io/specification).

## Repository Structure

```
skills/
├── skills/                    # All skill implementations
│   ├── docx/                  # Document creation/editing (proprietary)
│   ├── pdf/                   # PDF manipulation (proprietary)
│   ├── pptx/                  # PowerPoint creation (proprietary)
│   ├── xlsx/                  # Spreadsheet operations (proprietary)
│   ├── skill-creator/         # Guide for creating new skills
│   ├── mcp-builder/           # MCP server development guide
│   ├── webapp-testing/        # Playwright-based web testing
│   ├── canvas-design/         # Visual design toolkit
│   ├── algorithmic-art/       # Generative art creation
│   ├── brand-guidelines/      # Brand asset management
│   ├── doc-coauthoring/       # Collaborative document editing
│   ├── frontend-design/       # Frontend UI/UX design
│   ├── internal-comms/        # Internal communications
│   ├── slack-gif-creator/     # Animated GIF creation
│   ├── theme-factory/         # Theme/styling generation
│   └── web-artifacts-builder/ # Web artifact creation
├── spec/                      # Agent Skills specification (links to agentskills.io)
├── template/                  # Skill template for new skills
├── .claude-plugin/            # Claude Code plugin marketplace config
├── README.md                  # Project documentation
└── THIRD_PARTY_NOTICES.md     # Third-party license notices
```

## Skill Anatomy

Every skill follows this structure:

```
skill-name/
├── SKILL.md                   # Required - instructions and metadata
├── scripts/                   # Optional - executable code (Python/Bash)
├── references/                # Optional - documentation for context
└── assets/                    # Optional - templates, images, fonts, etc.
```

### SKILL.md Structure

```markdown
---
name: skill-name
description: What the skill does and when to use it
license: License information (optional)
---

# Skill Title

Instructions for using the skill...
```

**Critical**: The `description` field in frontmatter is the primary triggering mechanism - it determines when Claude uses the skill.

## Key Conventions

### Skill Design Principles

1. **Concise is key** - Only include information Claude doesn't already have
2. **Progressive disclosure** - Keep SKILL.md under 500 lines; split content into reference files
3. **Set appropriate freedom** - Match specificity to task fragility (narrow bridge = guardrails, open field = flexibility)

### File Organization

- **scripts/**: Reusable code for deterministic, repeatable operations
- **references/**: Documentation loaded as-needed (domain knowledge, schemas, APIs)
- **assets/**: Output resources (templates, images, fonts) - not loaded into context

### What NOT to Include

- README.md, INSTALLATION_GUIDE.md, CHANGELOG.md
- User-facing documentation
- Setup/testing procedures
- Process documentation

## Development Workflows

### Creating a New Skill

1. Use the skill-creator skill: Read `skills/skill-creator/SKILL.md`
2. Or use the template: Copy `template/SKILL.md` and customize
3. Initialize with: `python skills/skill-creator/scripts/init_skill.py <name> --path <dir>`
4. Package with: `python skills/skill-creator/scripts/package_skill.py <path>`

### Modifying Existing Skills

1. Read the existing SKILL.md completely
2. Check for reference files that may need updates
3. Test any scripts after modification
4. Ensure frontmatter description remains accurate

### Testing Skills

- Run bundled scripts to verify they work
- Use representative samples for bulk operations
- Validate outputs match expected formats

## Plugin Marketplace

This repository serves as a Claude Code plugin marketplace with two plugin bundles:

1. **document-skills**: xlsx, docx, pptx, pdf
2. **example-skills**: algorithmic-art, brand-guidelines, canvas-design, doc-coauthoring, frontend-design, internal-comms, mcp-builder, skill-creator, slack-gif-creator, theme-factory, web-artifacts-builder, webapp-testing

Install via Claude Code:
```
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

## Licensing

- **Open source (Apache 2.0)**: Most example skills
- **Proprietary (source-available)**: Document skills (docx, pdf, pptx, xlsx) - see LICENSE.txt in each

## Code Style Guidelines

- Write minimal, concise code without unnecessary comments
- Avoid verbose variable names and redundant operations
- Avoid unnecessary print statements
- Use imperative/infinitive form in skill instructions

## Common Patterns

### Reference File Pattern

Keep SKILL.md lean; link to detailed references:
```markdown
## Advanced Features
- **Form filling**: See [forms.md](forms.md) for complete guide
- **API reference**: See [reference.md](reference.md) for all methods
```

### Script Pattern

Bundle reusable scripts that can be executed as black boxes:
```bash
python scripts/helper.py --help  # Always check usage first
```

### Conditional Loading Pattern

Load references only when needed:
```markdown
If you need to fill out a PDF form, read forms.md and follow its instructions.
```

## Important Resources

- [Agent Skills Specification](https://agentskills.io/specification)
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [Creating custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
