# Contributing to AI Room

Thank you for your interest in contributing to AI Room! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Types of Contributions

We welcome various types of contributions:

- 🐛 **Bug Reports**: Report bugs or issues you encounter
- 💡 **Feature Requests**: Suggest new features or improvements
- 📝 **Documentation**: Improve or add documentation
- 🔧 **Code**: Fix bugs, implement features, or improve existing code
- 🧪 **Testing**: Write tests or help improve test coverage
- 🌐 **Localization**: Help translate the project to other languages

### Getting Started

1. **Fork the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/use-llama.cpp.git
cd use-llama.cpp
   ```

2. **Set Up Development Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install development dependencies
   pip install -e ".[dev]"
   
   # Install pre-commit hooks
   pre-commit install
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

## 📝 Development Guidelines

### Code Style

We use several tools to maintain code quality:

- **Black**: Code formatting (line length: 88)
- **Pylint**: Code linting
- **MyPy**: Type checking
- **Pre-commit**: Automated checks

Run these before committing:
```bash
# Format code
black src/ tests/

# Lint code
pylint src/use_llama_cpp/

# Type checking
mypy src/use_llama_cpp/

# Run tests
pytest
```

### Code Standards

- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose
- Write meaningful commit messages

### Testing

- Write tests for new functionality
- Ensure all tests pass before submitting
- Aim for good test coverage
- Use descriptive test names

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=airoom

# Run specific test
pytest tests/test_model_loader.py
```

## 🚀 Submitting Changes

### Pull Request Process

1. **Ensure Quality**
   - All tests pass
   - Code follows style guidelines
   - Documentation is updated
   - No linting errors

2. **Create Pull Request**
   - Use a descriptive title
   - Provide clear description of changes
   - Reference related issues
   - Include screenshots for UI changes

3. **Review Process**
   - Maintainers will review your PR
   - Address any feedback or requested changes
   - PRs require approval before merging

### Commit Message Format

Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Examples:
```
feat(chat): add conversation history reset functionality

fix(model): resolve GPU memory leak issue

docs(readme): update installation instructions
```

## 🐛 Reporting Issues

### Bug Reports

When reporting bugs, please include:

- **Description**: Clear description of the problem
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: OS, Python version, dependencies
- **Screenshots**: If applicable

### Feature Requests

For feature requests:

- **Description**: Clear description of the feature
- **Use Case**: Why this feature would be useful
- **Proposed Solution**: How you think it should work
- **Alternatives**: Any alternatives you've considered

## 📚 Documentation

### Contributing to Docs

- Keep documentation up-to-date with code changes
- Use clear, concise language
- Include code examples where helpful
- Follow the existing documentation style

### Building Documentation

```bash
# Install docs dependencies
pip install -e ".[docs]"

# Build documentation
cd docs
make html

# View locally
open _build/html/index.html
```

## 🏷️ Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Changelog is updated
- [ ] Version is bumped
- [ ] Release notes are prepared
- [ ] GitHub release is created

## 🆘 Getting Help

### Questions and Discussion

- **GitHub Discussions**: For questions and general discussion
- **GitHub Issues**: For bugs and feature requests
- **Email**: For private or sensitive matters

### Communication Guidelines

- Be respectful and inclusive
- Use clear, constructive language
- Provide context for your questions
- Help others when you can

## 📄 License

By contributing to AI Room, you agree that your contributions will be licensed under the same license as the project (MIT License).

## 🙏 Recognition

Contributors will be recognized in:
- Project README
- Release notes
- Contributor hall of fame
- GitHub contributors list

---

Thank you for contributing to AI Room! 🚀
