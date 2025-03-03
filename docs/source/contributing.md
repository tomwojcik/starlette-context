# Contributing to starlette-context

Thank you for considering contributing to starlette-context! This project is open to contributions from anyone in the community.

## Getting Started

### Prerequisites

- Python 3.9+
- [Poetry](https://python-poetry.org/) for dependency management

### Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/starlette-context.git
   cd starlette-context
   ```

3. Set up the development environment using Poetry:
   ```bash
   poetry install
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

### Running Tests

Run the entire test suite:
```bash
poetry run pytest
```

Run tests with coverage report:
```bash
poetry run pytest --cov=starlette_context
```

### Code Style

This project uses several tools to ensure code quality:

- [Black](https://github.com/psf/black) for code formatting
- [ruff](https://github.com/astral-sh/ruff) for linting
- [mypy](https://github.com/python/mypy) for type checking

You can run all checks with:
```bash
make run-hooks
```

### Adding Features

1. Create a branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Implement your changes
3. Add tests for your changes
4. Update documentation as needed
5. Run tests and linting to ensure everything passes
6. Commit your changes

### Pull Requests

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Open a pull request against the `master` branch of the main repository
3. Ensure the PR description clearly describes the problem and solution
4. Include the relevant issue number if applicable

## Guidelines

### Testing

- All new features should include tests
- Maintain or improve test coverage
- Both unit and integration tests are welcome

### Documentation

- Update documentation for any new features or changes to existing ones
- Make sure your code is well-documented with docstrings
- Include examples where appropriate

### Versioning

This project follows [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for new functionality in a backwards compatible manner
- PATCH version for backwards compatible bug fixes

### Commit Messages

Use clear and meaningful commit messages:
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Reference issues and pull requests where appropriate

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## Questions?

If you have any questions or need help, please open an issue on GitHub.