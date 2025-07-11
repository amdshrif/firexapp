# FireX App

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

FireX is a general-purpose automation platform that enables users to build complex, traceable, extensible workflows. The Python programming language is used to write tasks, which assemble into workflows. Through Flame, a sophisticated visualization tool, even the most daunting workflows can be understood and extended across multiple teams with different goals.

## Features

- **Workflow Automation**: Build complex workflows using Python microservices
- **Micro-service Architecture**: Distributed task execution using Celery
- **Visual Workflow Tracking**: Flame visualization tool for workflow monitoring
- **Extensible Plugin System**: Load external plugins and microservices
- **Command Line Interface**: Easy-to-use CLI for workflow management
- **Data Aggregation**: Monitor and analyze workflow executions at task level

## Installation

### Prerequisites

FireX requires Redis as a message broker. Install Redis before proceeding:

```bash
# On Ubuntu/Debian
sudo apt-get install redis-server

# On macOS with Homebrew
brew install redis

# Verify installation
which redis-server
```

If Redis is not in your PATH, set the environment variable:
```bash
export redis_bin_dir=<path to redis directory containing the redis binaries>
```

### Install FireX App

```bash
pip install firexapp[flame]
```

### Verify Installation

```bash
firexapp list --microservices
firexapp info sleep  
firexapp version
```

## Quick Start

### Run a Simple Service

Execute the built-in `nop` service to verify your installation:

```bash
firexapp submit --chain nop
```

This will output something like:
```
[11:42:57][HOSTNAME] FireX ID: FireX-username-210122-114257-22938
[11:42:57][HOSTNAME] Logs: /tmp/FireX-username-210122-114257-22938
[11:43:00][HOSTNAME] Flame: http://HOSTNAME:59535
```

Follow the Flame link to visualize your workflow execution.

### Create Your Own Service

Create a file called `hello.py`:

```python
from firexapp.engine.celery import app

@app.task
def hello_world():
    return 'Hello World!'
```

Run your custom service:

```bash
firexapp submit --chain hello_world --plugins hello.py
```

## Usage

### Command Line Interface

FireX App provides several commands:

- **submit**: Execute workflows
- **list**: List available microservices or arguments
- **info**: Get detailed information about a microservice
- **version**: Display version information

### Examples

```bash
# List all available microservices
firexapp list --microservices

# Get information about a specific service
firexapp info <service_name>

# Submit a workflow with custom plugins
firexapp submit --chain <service_name> --plugins <plugin_file>

# View help for any command
firexapp submit --help
```

## Documentation

For comprehensive documentation, including programming guides and API references, visit the [docs](docs/) directory or build the documentation:

```bash
cd docs/
make html
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: Report bugs and request features via [GitHub Issues](https://github.com/FireXStuff/firexapp/issues)
- **Email**: firex-dev@gmail.com
- **Documentation**: [Complete documentation](docs/index.rst)

## Related Projects

- [FireX Kit](https://github.com/FireXStuff/firexkit) - Core FireX utilities and decorators
- [FireX Flame](https://github.com/FireXStuff/firex-flame) - Web-based workflow visualization tool


