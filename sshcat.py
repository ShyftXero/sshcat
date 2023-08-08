# shyft
# 20230807

import os
import select
import socket
import threading
import subprocess
import paramiko
import typer
import pty
from rich import print

app = typer.Typer()

KEY_FILENAME =  os.path.expanduser('~/.sshcat/sshcat.key')


def generate_key(filename):
    private_key = paramiko.RSAKey.generate(2048)
    private_key.write_private_key_file(filename)


class SSHServer(paramiko.ServerInterface):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_auth_password(self, username, password):
        if username == self.username and password == self.password:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_pty_request(
        self, channel, term, width, height, pixelwidth, pixelheight, modes
    ):
        return True

    def check_channel_shell_request(self, channel):
        return True


def handle_client(client_socket:socket.socket, command, username, password):
    print(f'Connection from {client_socket.getpeername()} ')
    transport = paramiko.Transport(client_socket)
    
    private_key_file = KEY_FILENAME
    if not os.path.exists(private_key_file):
        os.mkdir(os.path.dirname(KEY_FILENAME))
        
        generate_key(private_key_file)

    host_key = paramiko.RSAKey(filename=private_key_file)
    transport.add_server_key(host_key)

    server = SSHServer(username, password)
    try:
        transport.start_server(server=server)
    except EOFError as e:
        print(e)
        return 
    channel = transport.accept(20)
    if channel is None:
        print("*** No channel.")
        return

    master_fd, slave_fd = pty.openpty()
    proc = subprocess.Popen(
        command,
        shell=True,
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        close_fds=True,
    )

    # channel.sendall(b"Executing: " + command.encode("utf-8") + b"\n")
    
    while proc.poll() is None:
        rlist, _, _ = select.select([master_fd, channel], [], [], 0.1)
        for r in rlist:
            if r == master_fd:
                data = os.read(master_fd, 1024)
                channel.sendall(data)
            elif r == channel:
                data = channel.recv(1024)
                if len(data) == 0:
                    break
                os.write(master_fd, data)

    channel.send_exit_status(proc.returncode)
    channel.close()
    transport.close()

@app.command()
def main(
    port: int = 2222,
    command: str = "echo helloworld",
    username: str = "user",
    password: str = "pass",
):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)

    print(f"Listening for connection on port {port} and running '{command}'")

    try:
        while True:
            client_socket, _ = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client, args=(client_socket, command, username, password)
            )
            client_thread.start()

    except KeyboardInterrupt:
        print("Server shutting down.")
        server_socket.close()


if __name__ == "__main__":
    app()
