import os
import subprocess
import socket
import sys
import threading

from getpass import getpass

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def search_room():
    answer = None
    while answer not in ("Y", "y", "N", "n"):
            answer = input("[+] The scanning can take a lot of time, are you sure you want to continue ? y/n ")
    if answer in ("Y", "y"):
        output = subprocess.run(("arp -a"), capture_output=True, text=True)
        output = list((output.stdout).split())
        ip_list = []
        for ip in output:
            if bool(ip.count(".")):
                ip_list.append(ip)
                clear_screen()

        for ip in ip_list:
            for port in range(65535):
                try:
                    print(f"[+] Now scanning {ip}:{port}")     
                except:
                    continue
                else:
                    return True
    else:
        return 1
                
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == "NICK":
                client.send(nickname.encode('ascii'))
            elif message == "[-] The room gets closed by the host":
                print(message)
                client.close()
            else:
                print(message)
        except:
            continue

def write():
    while True:
        try:
            message = f"{nickname}: {input('')}"
            client.send(message.encode('ascii'))
        except KeyboardInterrupt:
            print("[+] Closing chat ...")
            client.close()
        except OSError:
            sys.exit()

if __name__ == "__main__":
    clear_screen()
    nickname = input("[+] Choose a nickname: ")
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clear_screen()
    answer = int(input("\t-1 if you are searching a particular room\n\t-2 if you want to search for a random room\n[+] Type: "))

    clear_screen()
    if answer == 1:
        ip = str(input("[+] Type the ip of the room's server: "))
        port = int(input("[+] Type the port of the room's server: "))
    else:
        answer = search_room()
        if answer == 1:
            ip = str(input("[+] Type the ip of the room's server: "))
            port = int(input("[+] Type the port of the room's server: "))

    try:
        client.connect((ip, port))
    except ConnectionAbortedError:
        print("[-] You probably are blocked in this session")
        sys.exit()

    while True:
        acceptation = None
        password = getpass()
        client.send(password.encode('ascii'))
        acceptation = client.recv(2048).decode()
        if acceptation == "True":
            break
        else:
            print(acceptation)

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()