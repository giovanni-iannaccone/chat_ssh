from getpass import getpass

import os
import socket
import sys
import threading

def block(nickname):
    addr = address[nicknames.index(nickname)]
    blocked_users.append(addr[0])
    remove_blocked(addr)
    print(blocked_users)

def broadcast(message):
    for client in clients:
        client.send(message)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def exiting():
    message = "[-] The room gets closed by the host".encode('ascii')
    print("[-] Closing chat ...")
    for client in clients:
        client.send(message)
        remove(nicknames[clients.index(client)])
    sys.exit()

def handle(client):
    while True:
        try:
            message = client.recv(2048)
            if client in clients:
                broadcast(message)
        except:
            try:
                index = clients.index(client)
                nickname = nicknames[index]
                remove(nickname)
                broadcast("{} left!".format(nickname).encode('ascii'))
            except ValueError:
                pass

def receive():
    while True:
        client, addr = server.accept()
        address.append(addr)
        clients.append(client)

        if addr[0] in blocked_users:
            remove_blocked(addr)
            continue

        while client.recv(2048).decode('ascii') != password:
            client.send("[-] Wrong password".encode('ascii'))
            
        client.send("True".encode('ascii'))

        print("[+] Connected with {}".format(str(addr)))

        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)

        print("[+] Nickname is {}".format(nickname))
        broadcast("[+] {} joined!".format(nickname).encode('ascii'))
        client.send("[+] Connected to server!".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

        write_thread = threading.Thread(target=write)
        write_thread.start()

def remove(connection):
    index = nicknames.index(connection)
    clients[index].close()
    clients.pop(index)
    address.pop(index)
    nicknames.remove(connection)

def remove_blocked(connection):
    index = address.index(connection)
    address.remove(connection)

    clients[index].close()
    clients.pop(index)

def show_info(nickname):
    ip, port = address[nicknames.index(nickname)]
    print(f"[+] Ip: {ip}")
    print(f"[+] Port: {port}")
    print(f"[+] Nickname: {nickname}")

def write():
    while True:
        cmd = input("> ")
        cmd = list(cmd.split())
        if cmd[0] in  ("-h", "--help"):
            print("[+] Servers's host has special 'powers', type:")
            print("\t-block 'nickname' \tto don't allow him to enter to this session")
            print("\t-clear \t\t\tto clear the screen")
            print("\t-exit \t\t\tto close the room for everybody")
            print("\t-info 'nickname' \tto have information on a nickname (his ip & port )")
            print("\t-ls \t\t\tto show all connected user")
            print("\t-remove 'nickname' \tto remove an user")

        elif cmd[0] == "block":
            block(cmd[1])
            print(f"Blocked users: {blocked_users}")
            
        elif cmd[0] == "clear":
            clear_screen()

        elif cmd[0] == "exit":
            exiting()

        elif cmd[0] == "info":
            show_info(cmd[1]) 

        elif cmd[0] == "ls":
            print(f"[+] Connected: {[nickname for nickname in nicknames]}")
            print(f"[+] Connected: {[addr[0] for addr in address]}")

        elif cmd[0] == "remove":
            remove(cmd[1])
    
        else:
            print("[-] Invalid syntax, type -h or --help for more informations")

if __name__ == "__main__":
    try:
        host = str(socket.gethostbyname(socket.gethostname()))
        answer, cmd = None, None
        while answer not in ("Y", "y", "N", "n"):
            answer = input(f"[+] Your ip is {host}, do you want to use this for the server ? y/n ")

        if answer in ("N", "n"):
            host = input("[+] Type here the ip you want to use: ")

        while True:
            try:        
                port = int(input("[+] Type the port: "))
            except:
                print("Invalid input")
                port = int(input("[+] Type the port: "))
            else:
                break

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen()

        address = []
        blocked_users = []
        clients = []
        nicknames = []
        password = getpass()
        print("[+] Server is listening ...")
        receive()

    except KeyboardInterrupt:
        exiting()