# Python Project: Structure and Automation with Makefile
This project is designed to provide a robust and standard structure for Python projects, utilizing a Makefile to automate common tasks such as testing, dependency installation, code validation, and documentation generation.

## Requirements

## Requirements

This project leverages several tools and libraries to maintain code quality, enforce standards, and simplify the development process. Below are the key tools used in this project:

- **[Python](https://www.python.org/downloads/)**: The programming language used for this project.
- **[Poetry](https://python-poetry.org/docs/#installation)**: Manages dependencies and virtual environments, ensuring consistency across different development setups.
- **[Make](https://www.gnu.org/software/make/)**: Automates tasks defined in the Makefile.
- **[Tox](https://tox.readthedocs.io/en/latest/)**: Automates testing in multiple environments, making it easy to ensure your code works across different Python versions.
- **[Pytest](https://docs.pytest.org/en/stable/)**: A robust testing framework that simplifies writing and running tests.
- **[Pytest-Sugar](https://pypi.org/project/pytest-sugar/)**: Enhances the pytest output for better readability, making it easier to see what tests are running and their results.
- **[Pytest-Cov](https://pypi.org/project/pytest-cov/)**: Measures code coverage, helping ensure that your tests cover all aspects of your code.
- **[Black](https://black.readthedocs.io/en/stable/)**: An uncompromising code formatter that enforces a consistent code style throughout the project.
- **[Mypy](http://mypy-lang.org/)**: A static type checker for Python that ensures type correctness, helping catch errors early in the development process.
- **[Isort](https://pycqa.github.io/isort/)**: Automatically sorts your imports to maintain a consistent order, which improves code readability.
- **[Flake8](https://flake8.pycqa.org/en/latest/)**: Combines multiple linting tools to enforce coding standards and detect potential issues in your code.
- **[Ruff](https://beta.ruff.rs/docs/)**: A fast Python linter that provides an alternative to Flake8, focusing on speed and efficiency.
- **[Pylint](https://pylint.pycqa.org/en/latest/)**: A comprehensive linter that checks for errors, enforces a coding standard, and looks for code smells.



## Project Structure

```bash 
.
├── src/                     # Project source code
├── tests/                   # Unit and integration tests
├── docs/                    # Documentation source files
│   ├── source/              # Sphinx source files
│   └── build/               # Generated documentation output
├── pyproject.toml           # Poetry configuration file
├── Makefile                 # Makefile for task automation
└── README.md                # Project documentation
```

## Using the Makefile
    The Makefile in this project is configured to handle various common tasks. Below is a description of each 
    available task:

### Available Tasks

- **`test`**: Run tests using `pytest`.
- **`cov`**: Run tests and generate a coverage report using `pytest-cov`.
- **`install`**: Install dependencies and the package into a `poetry`-managed virtual environment.
- **`lint`**: Run `mypy`, `flake8`, `ruff`, and `pylint` to check code quality.
- **`fmt`**: Format code using `black`.
- **`pylint`**: Run `pylint` to check code quality and style.
- **`test_envs`**: Run tests across multiple environments using `tox`.
- **`docs`**: Generate HTML documentation using Sphinx.

### Running Tasks
        To run any of the tasks defined in the Makefile, simply use the make command followed by the task name.
        For example, to run the tests, you can use:

```bash
make test
```

## Generating Documentation
  To generate the project documentation, use the docs target:

```bash
make docs
```
    This will build the HTML documentation using Sphinx, placing the output in the docs/build/html directory.

## Help
    You can view a list of all available tasks with a brief description by using the command:

```bash
make help
```

### Installation
To set up the project and its dependencies, follow these steps:

Clone the repository:

```bash
git clone <repository_url>
cd <repository_name>
```

### Install the dependencies using poetry:

```bash
make install
```

### Contributing
If you wish to contribute to this project, please ensure that you follow best practices for clean code and utilize the
provided linting, formatting, and documentation tools.

## Follow Me

Stay connected and follow me on these platforms:

- **GitHub**: [macurandb](https://github.com/macurandb/)
- **LinkedIn**: [duany-baro-menendez](https://www.linkedin.com/in/duany-baro-menendez/)


Feel free to reach out for collaborations, questions, or just to connect!