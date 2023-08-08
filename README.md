# SSHcat

SSHcat is a custom SSH server written in Python that accepts client connections and executes a specified command. This server is designed to handle interactive programs and provides a seamless interaction over the SSH protocol.

## Features

- Customizable command execution
- Username and password authentication
- Interactive shell support
- Dynamic key generation

## Dependencies

- paramiko
- typer

## Installation

You can clone this repository to your local machine and run it using Python.

```bash
git clone https://github.com/yourusername/SSHcat.git
cd SSHcat
pip install -r requirements.txt
python sshcat.py
```

Replace `yourusername` with your GitHub username, and update the URL if you've named the repository differently.

## Usage

You can run SSHcat using the following command:

```bash
python sshcat.py --port 2222 --command "/bin/bash" --username "user" --password "pass"
```

- `--port` specifies the port number (default is 8022)
- `--command` specifies the command to execute (default is "echo helloworld")
- `--username` specifies the username for authentication (default is "user")
- `--password` specifies the password for authentication (default is "pass")

## Contributing

Feel free to fork this project, submit a pull request, or open an issue if you have any enhancements or find any bugs.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- paramiko library for SSH support
- typer library for command-line interface handling
