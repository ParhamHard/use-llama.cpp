# Legacy Code

This directory contains the original AI Room project files that were restructured for publication.

## What's Here

- **Original Python files**: The original implementation files
- **Old project structure**: The previous organization of the project
- **Development scripts**: Original setup and testing scripts

## Migration Notes

The original code has been refactored and moved to the new structure:

- Core functionality → `src/use_llama_cpp/core/`
- CLI interface → `src/use_llama_cpp/cli/`
- Utilities → `src/use_llama_cpp/utils/`
- Examples → `examples/`
- Tests → `tests/`

## New Structure

The project has been restructured with:

- Modern Python packaging (`pyproject.toml`)
- Proper package structure (`src/use_llama_cpp/`)
- Comprehensive documentation
- Docker support
- Development tools and testing
- Professional project organization

## Using Legacy Code

If you need to reference the original implementation:

1. Check the new structure first
2. Look for equivalent functionality in the new modules
3. The new code maintains the same core functionality but with better organization

## Migration Guide

To migrate from the old structure:

1. Use `from use_llama_cpp import ModelLoader, AIChat` instead of direct imports
2. Use the new CLI: `use-llama-cpp model.gguf --interactive`
3. Check the examples in the `examples/` directory
4. Use the new Docker setup for containerized deployment
