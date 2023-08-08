# sshcat

sshcat is a custom SSH server in Python that accepts client connections and executes a specified command. This server is designed to handle interactive programs and provides seamless interaction over the SSH protocol.

It is meant to be used to somewhat protect CTF challenges on shared infrastructure. 

It's a bit like sshd's ForceCommand http://man.openbsd.org/OpenBSD-current/man5/sshd_config.5#ForceCommand

No users to configure on the system. 

Just specify the username and password (default user:pass), port (default 2222), and command you want the SSH server to run when conencted to.
 

## Usage

Start the server with a specific command:

```bash
sshcat --port 2222 --command "cat /tmp/coolfile.txt" --username "user" --password "pass" # this will run as the user running sshcat on the server. if that's root, then you've given them a root shell...
```

Connect to the server with your SSH client:

```bash
ssh -p 2222 user@localhost
```
### More Usage
```bash
sshcat --help
Usage: sshcat [OPTIONS]

Options:
  --port INTEGER        [default: 2222]
  --command TEXT        [default: echo helloworld]
  --username TEXT       [default: user]
  --password TEXT       [default: pass]
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.

  --help                Show this message and exit.
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
   cd sshcat
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
