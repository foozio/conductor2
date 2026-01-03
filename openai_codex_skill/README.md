# OpenAI Codex Conductor Skill

A Python implementation of the Conductor skill system that uses OpenAI's API (including Codex models) instead of relying on specific AI coding agents like Claude Code or Gemini CLI.

## Features

- **Context-Driven Development**: Same philosophy as the original Conductor - "Measure twice, code once"
- **OpenAI Integration**: Uses OpenAI's GPT models for code generation, analysis, and planning
- **Flexible Setup**: Works for both new (greenfield) and existing (brownfield) projects
- **Track Management**: Create and manage development tracks with specs and implementation plans
- **TDD Workflow**: Follows test-driven development principles
- **CLI Interface**: Command-line interface for all operations

## Installation

1. Clone or download this skill
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

## Usage

### Initialize a Project

```bash
python cli.py setup
```

This will:
- Detect if it's a new or existing project
- Analyze the codebase (for existing projects)
- Generate project context files (product.md, tech-stack.md, etc.)
- Set up code style guides and workflow
- Create an initial development track

### Create a New Track

```bash
python cli.py new-track "Add user authentication"
```

This generates:
- A detailed specification (spec.md)
- An implementation plan (plan.md) with phases and tasks

### Implement Tasks

```bash
python cli.py implement
```

This will:
- Find the next pending task in the current track
- Use OpenAI to generate implementation suggestions
- Allow you to review and apply changes
- Mark tasks as complete

### Check Status

```bash
python cli.py status
```

Shows the current state of all tracks and their progress.

### Revert Changes

```bash
python cli.py revert --track <track_id> --target track
```

Provides guidance for git-aware rollback of tracks, phases, or tasks.

## Directory Structure

After setup, your project will have:

```
conductor/
├── product.md              # Product vision and goals
├── product-guidelines.md   # UX/brand guidelines
├── tech-stack.md           # Technology choices
├── workflow.md             # Development workflow
├── tracks.md               # Master list of tracks
├── code_styleguides/       # Style guides (general, python, javascript, etc.)
├── tracks/                 # Individual tracks
│   └── <track_id>/
│       ├── metadata.json
│       ├── spec.md
│       └── plan.md
└── setup_state.json        # Setup progress tracking
```

## Configuration

- **API Key**: Set `OPENAI_API_KEY` environment variable or pass `--api-key`
- **Model**: Use `--model` to specify the OpenAI model (default: gpt-4)
  - Options: gpt-4, gpt-3.5-turbo, or Codex models if available

## Workflow

1. **Setup**: Initialize project context
2. **New Track**: Define features/bugs to implement
3. **Implement**: Execute tasks following TDD principles
4. **Verify**: Manual verification at phase completion
5. **Repeat**: Create new tracks as needed

## Differences from Agent-Based Conductor

- **Interactive**: Uses command-line prompts instead of agent chat
- **API-Driven**: All AI operations go through OpenAI API
- **Stateless**: Each command is independent (no persistent agent session)
- **Configurable**: Easy to switch models or adjust parameters

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for API calls