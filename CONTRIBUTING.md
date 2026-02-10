# Contributing to Commpay

Thank you for your interest in contributing to Commpay! This document provides guidelines and instructions for contributing.

## Development Agreement

All contributors must follow the [Developer Agreement](https://github.com/eribichesu/commpay/blob/main/DEVELOPER_AGREEMENT.md) which covers:

- Pull Request execution
- Code review process
- Software Development Life Cycle (SDLC)
- Incident tracking and revision
- Architecture guidelines

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/commpay.git`
3. Create a feature branch: `git checkout -b feat/your-feature-name`
4. Make your changes
5. Run tests and linting
6. Commit your changes using conventional commits
7. Push to your fork and submit a pull request

## Branching Convention

- `feat/description` - New features
- `fix/issue-number` - Bug fixes
- `hotfix/description` - Urgent fixes
- `chore/description` - Maintenance tasks

## Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test additions or changes
- `chore`: Build process or auxiliary tool changes

## Code Quality Requirements

Before submitting a PR:

1. **Format your code:**
   ```bash
   black src/ tests/
   ```

2. **Run linting:**
   ```bash
   flake8 src/ tests/
   ```

3. **Run type checking:**
   ```bash
   mypy src/
   ```

4. **Run tests:**
   ```bash
   pytest tests/
   ```

5. **Ensure all tests pass and coverage is maintained**

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update documentation for any modified APIs
3. Add or update tests for your changes
4. Ensure the PR description clearly describes the problem and solution
5. Reference any related issues
6. Request review from appropriate team members
7. Address review feedback
8. Ensure all CI checks pass

## Code Review Guidelines

When reviewing code:

- Be constructive and respectful
- Focus on the code, not the person
- Explain reasoning for suggestions
- Approve when standards are met or request changes with clear explanations

## Questions?

If you have questions about contributing, please open an issue for discussion.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
