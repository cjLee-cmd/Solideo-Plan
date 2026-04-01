# AGENTS.md

This file contains guidelines for agentic coding agents working in this repository. It includes build/lint/test commands, code style guidelines, and any applicable Cursor or Copilot rules.

## Build, Lint, and Test Commands

### Current State
This repository is currently focused on planning documents and Notion integration, as per CLAUDE.md. No build, lint, or test commands are defined at this time.

### Future Code Additions
When code is added to this repository, follow these conventions:

#### Python Projects (using UV)
- **Install dependencies**: `uv pip install -e ".[dev]"`
- **Run all tests**: `uv run pytest`
- **Run single test**: `uv run pytest path/to/test_file.py::test_function_name -v`
- **Run tests with coverage**: `uv run pytest --cov=src --cov-report=html`
- **Lint code**: `uv run ruff check .`
- **Format code**: `uv run ruff format .`
- **Type check**: `uv run mypy src/`
- **Run specific test suite**: `uv run pytest -m unit` (assuming markers are defined)

#### TypeScript/JavaScript Projects
- **Install dependencies**: `npm install`
- **Run tests**: `npm test`
- **Run single test**: `npm test -- --testNamePattern="test name"`
- **Lint**: `npm run lint`
- **Format**: `npm run format`
- **Build**: `npm run build`

#### General Commands
- **Run lint and typecheck**: Run the appropriate lint and typecheck commands after code changes.
- **Pre-commit hooks**: If configured, ensure hooks pass before committing.

## Code Style Guidelines

### General Principles
- Follow SOLID principles, DRY, KISS, and YAGNI.
- Write readable, maintainable code.
- Use version control best practices.
- Avoid secrets in code; use environment variables.
- Include comments for complex logic, but prefer self-documenting code.

### Python Style
- **Indentation**: 4 spaces
- **Line length**: 88 characters (Black default)
- **Imports**: 
  - Standard library imports first
  - Third-party imports second
  - Local imports last
  - Use absolute imports
  - Group imports with blank lines
- **Naming conventions**:
  - Modules: snake_case
  - Functions: snake_case
  - Classes: PascalCase
  - Constants: UPPER_SNAKE_CASE
  - Variables: snake_case
- **Type hints**: Use type hints for function parameters and return types
- **Docstrings**: Use Google-style docstrings for modules, classes, and functions
- **Error handling**: Use try-except blocks, log exceptions appropriately
- **Formatting**: Use Ruff for linting and Black for formatting
- **Testing**: Use pytest with descriptive test names

### TypeScript/JavaScript Style
- **Indentation**: 2 spaces
- **Line length**: 100 characters
- **Imports**: Use ES6 imports, group by external/internal
- **Naming conventions**:
  - Files: kebab-case.ts
  - Classes: PascalCase
  - Functions: camelCase
  - Variables: camelCase
  - Constants: UPPER_SNAKE_CASE
- **Types**: Use TypeScript with strict mode
- **Error handling**: Use try-catch, throw meaningful errors
- **Formatting**: Use Prettier
- **Linting**: Use ESLint with TypeScript rules

### Markdown Style
- Use ATX-style headers (# ## ###)
- Use consistent heading levels
- Include table of contents for long documents
- Use code blocks with language specification
- Use descriptive link text
- Follow Korean language conventions for project documents

### File Organization
- Group related files in directories
- Use descriptive filenames
- Separate concerns (models, views, controllers)
- Keep flat directory structure where possible

### Commit Messages
- Follow Conventional Commits: `type(scope): description`
- Types: feat, fix, docs, style, refactor, test, chore
- Keep messages concise but descriptive
- Reference issues: `Closes #123`

### Pull Requests
- Provide clear descriptions
- Include before/after screenshots for UI changes
- Ensure tests pass
- Get reviews from relevant team members

### Security Best Practices
- Never commit secrets or keys
- Use parameterized queries for database operations
- Validate input data
- Implement proper authentication/authorization
- Keep dependencies updated

## Cursor Rules

No Cursor rules files (.cursorrules or .cursor/rules/) were found in this repository.

## Copilot Rules

No Copilot instructions file (.github/copilot-instructions.md) was found in this repository.

## Project-Specific Guidelines

### SolCode_Lab Project
- This repository is for planning documents in the SolCode_Lab project
- Focus on closed-network LLM environment
- Consider internet restrictions in all designs
- Use Notion for project management integration
- Generate documents in Markdown, convert to HWPX as needed

### Workflow Integration
- Follow the 6-stage pipeline: Planning → Analysis → Generation → Modification → Review → Documentation
- Use Speckit for design planning
- Generate design.md and verify.md files
- Maintain synchronization between Notion pages and local documents

### Documentation Standards
- Use Korean for project-specific documentation
- Maintain clear structure with headers and sections
- Include diagrams where helpful (using Excalidraw if needed)
- Update CLAUDE.md with any new guidelines

### Tool Usage
- Use UV for Python operations
- Prefer MCP tools for Notion integration
- Use SuperClaude Framework commands when available
- Follow Git workflow: master ← integration ← feature/fix/docs branches

### Quality Assurance
- Run lint and typecheck after changes
- Test code thoroughly before commits
- Use the /md2hwpx command for document conversion
- Validate Notion page updates

### Error Handling and Logging
- Log errors with appropriate levels
- Provide user-friendly error messages
- Handle network failures gracefully (considering closed network)
- Implement retry logic for unreliable operations

### Performance Considerations
- Optimize for closed network environment
- Minimize external dependencies
- Cache results where appropriate
- Monitor resource usage

### Accessibility and Internationalization
- Ensure UI components are accessible
- Support Korean language interface
- Consider localization needs

### Maintenance
- Keep dependencies updated
- Monitor for security vulnerabilities
- Refactor code regularly to maintain quality
- Document breaking changes

This AGENTS.md file should be updated as the project evolves and more code is added to the repository.