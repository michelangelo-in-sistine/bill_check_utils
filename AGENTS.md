# AGENTS.md - Guidelines for AI Coding Agents

## Build/Lint/Test Commands
- **Run main script**: `python main.py <input_file.txt>`
- **No dedicated test framework** - manually test by running main.py with sample files
- **No linting configured** - use basic Python syntax checking
- **Single test run**: Execute `python main.py ./xls/minsheng_202510.txt` to test parsing

## Code Style Guidelines

### File Structure
- Use UTF-8 encoding: `# -*- coding: utf-8 -*-`
- Include creation date and author in docstrings
- Keep utility functions in separate modules (e.g., `bill_category_variables.py`)

### Naming Conventions
- **Classes**: CamelCase (e.g., `BillParser`, `SuiEntry`)
- **Functions/Methods**: snake_case (e.g., `read_credit_card_bill_file`)
- **Variables**: snake_case (e.g., `bill_year`, `entry_text`)
- **Constants**: UPPER_CASE with underscores (e.g., `pattern_cmb`)

### Imports & Dependencies
- Standard library imports first (e.g., `import re`, `import datetime`)
- Local imports second (e.g., `from sui_xls_writer import SuiEntry`)
- Use wildcard imports sparingly: `from bill_category_variables import *`

### Code Style
- **Docstrings**: Use triple quotes with Chinese descriptions when appropriate
- **Error Handling**: Use `assert` statements for critical validation
- **Comments**: Chinese comments for domain-specific logic
- **Line Length**: No strict limit, but keep readable
- **Indentation**: 4 spaces (standard Python)

### Best Practices
- Validate input files before processing
- Use regex patterns for parsing structured text data
- Handle date parsing carefully (year boundaries, different formats)
- Process amounts by removing commas and spaces before float conversion</content>
<parameter name="filePath">e:\work\bill_check_utils\AGENTS.md