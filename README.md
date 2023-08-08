# SSHcat

SSHcat is a custom SSH server in Python that accepts client connections and executes a specified command. This server is designed to handle interactive programs and provides seamless interaction over the SSH protocol.

It is meant to be used to somewhat protect CTF challenges on shared infrastructure. 

## Features


- Easy to use: Just specify the command you want the SSH server to pipe to.
- Based on Paramiko: Makes use of the robust SSH library.
- Customizable: Choose your own username, password, and port.

## Usage

Start the server with a specific command:

```bash
sshcat --port 2222 --command "/bin/bash" --username "user" --password "pass"
```

Connect to the server with your SSH client:

```bash
ssh -p 2222 user@localhost
```

## Installation

### Using Poetry

SSHcat uses Poetry for dependency management. Make sure you have [Poetry installed](https://python-poetry.org/docs/#installation) on your system.

1. Clone the repository:

   ```bash
   git clone https://github.com/ShyftXero/SSHcat.git
   ```

2. Navigate to the project directory:

   ```bash
   cd SSHcat
   ```

3. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

### Building and Installing the Package

To build and install the package, run:

```bash
poetry build
pip install dist/sshcat-<version>.tar.gz
```


## Dependencies

- paramiko
- typer
- poetry