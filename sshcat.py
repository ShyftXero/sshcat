# shyft
# 20230807
# see this for more ideas to improve... https://stackoverflow.com/a/68801952
import os
import select
import socket
import struct
import threading
import subprocess
import time
import paramiko
import typer
import pty
import signal
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
    ssh_channel = transport.accept(20)
    if ssh_channel is None:
        print("*** No channel.")
        return
    
    ssh_channel.resize_pty(width=200, height=110)

    # return 
    server_fd, client_fd = pty.openpty()
    
    proc = subprocess.Popen(
        f"/bin/bash -c '{command}'",
        shell=True,
        stdin=client_fd,
        stdout=client_fd,
        stderr=client_fd,
        close_fds=True,
    )

    # channel.sendall(b"Executing: " + command.encode("utf-8") + b"\n")
    interrupted = False
    while proc.poll() is None and interrupted == False:
        read_list, _, _ = select.select([server_fd, ssh_channel], [], [], 0.1)
        for read_item in read_list:
            if read_item == server_fd:
                data = os.read(server_fd, 1024)
                
                if bytes('^C'.encode())  in data:
                    print('User interrupted via ctrl-c; disconnecting:',client_socket.getpeername(), data)
                    proc.send_signal(signal.SIGINT) # send sigint to program. 
                    proc.terminate()
                    ssh_channel.send(f'\033[{1024}A') # move cursor up
                    ssh_channel.send(b'\n'*1024)     # overwrite what was there.  
                    
                    # time.sleep(1)
                    interrupted = True
                    break

                ssh_channel.sendall(data)
            elif read_item == ssh_channel:
                data = ssh_channel.recv(1024)
                if len(data) == 0:
                    break
                os.write(server_fd, data)
    
    
    try:
        
        ssh_channel.send_exit_status(proc.returncode)

    except struct.error as e: 
        print(e) 
    finally:
        ssh_channel.close()
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
