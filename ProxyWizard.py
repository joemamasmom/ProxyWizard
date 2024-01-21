import urllib3
import requests
import threading
import concurrent.futures
from sys import argv
from colorama import Fore
from os import system as terminal
from toolUsage import usage

URL = "http://google.com"
TIMEOUT = (3, 27)
CMD_CLEAR_TERM = 'clear'
lock = threading.Lock()

#help screen
def printHelp():
    terminal(CMD_CLEAR_TERM)
    print(usage)

# Proxy check with no threads
def threadlessCheckProxy(proxy):
    goods = 0
    bads = 0
    try:
        session = requests.Session()
        session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36.'
        session.max_redirects = 300

        proxy = proxy.strip()

        print(f"({Fore.BLUE}!{Fore.RESET})-({Fore.YELLOW}Wizarding{Fore.RESET}-{Fore.YELLOW}Proxy{Fore.RESET})-({Fore.LIGHTCYAN_EX}{proxy}{Fore.RESET}")

        response = session.get(URL, proxies={'http': 'http://' + proxy}, timeout=TIMEOUT, allow_redirects=True)

        # Check if the response status code indicates success
        if response.status_code == 200:
            print(f"({Fore.LIGHTGREEN_EX}✔{Fore.RESET})-({Fore.LIGHTGREEN_EX}GOOD{Fore.RESET}-{Fore.LIGHTGREEN_EX}PROXY{Fore.RESET})-({Fore.LIGHTGREEN_EX}{proxy}{Fore.RESET}", end='')
            with open('good.txt', 'a') as fileWithGoods:
                fileWithGoods.write(proxy)
            goods += 1
        else:
            print(f"({Fore.RED}✘{Fore.RESET})-({Fore.RED}BAD{Fore.RESET}-{Fore.RED}PROXY{Fore.RESET})-({Fore.RED}{proxy}{Fore.RESET}", end='')
            with open('bad.txt', 'a') as fileWithBads:
                fileWithBads.write(proxy)
            bads += 1

    except requests.exceptions.ConnectionError as e:
        print(f"({Fore.RED}✘{Fore.RESET})-({Fore.RED}Error{Fore.RESET})-({Fore.RED}Connection Error{Fore.RESET}")
        return e
    except requests.exceptions.HTTPError as e:
        print(f"({Fore.RED}✘{Fore.RESET})-({Fore.RED}Error{Fore.RESET})-({Fore.RED}HTTP Error{Fore.RESET}")
        return e
    except requests.exceptions.Timeout as e:
        print(f"({Fore.RED}✘{Fore.RESET})-({Fore.RED}Error{Fore.RESET})-({Fore.RED}Timeout{Fore.RESET}")
        return e
    except urllib3.exceptions.ProxySchemeUnknown as e:
        print(f"({Fore.RED}✘{Fore.RESET})-({Fore.RED}Error{Fore.RESET})-({Fore.RED}Proxy Scheme Unknown{Fore.RESET}")
        return e
    except requests.exceptions.TooManyRedirects as e:
        print(f"({Fore.RED}✘{Fore.RESET})-({Fore.RED}Error{Fore.RESET})-({Fore.RED}Too Many Redirects{Fore.RESET}")
        return e
    
    print("")
    print("")
    print(f"{Fore.LIGHTGREEN_EX} {goods} PROXIES REPLIED ")
    print(f"{Fore.LIGHTRED_EX} {bads} PROXIES DIDN'T REPLY ")

# Proxy check with threads
def checkProxies(proxies, num_threads):
    goods = 0
    bads = 0

    def checkProxy(proxy):
        try:
            session = requests.Session()
            session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36.'
            session.max_redirects = 300

            proxy = proxy.strip()

            print(f"({Fore.BLUE}!{Fore.RESET})-({Fore.YELLOW}Wizarding{Fore.RESET}-{Fore.YELLOW}Proxy{Fore.RESET})-({Fore.LIGHTCYAN_EX}{proxy}{Fore.RESET}")

            session.get(URL, proxies={'http': 'http://' + proxy}, timeout=TIMEOUT, allow_redirects=True)
            return None
        except requests.exceptions.ConnectionError as e:
            print(f"({Fore.RED}✘{Fore.RESET})-({Fore.RED}Error{Fore.RESET})-({Fore.RED}Connection Error{Fore.RESET}")
            return e
        except requests.exceptions.HTTPError as e:
            print(f"({Fore.RED}✘{Fore.RESET})-({Fore.RED}Error{Fore.RESET})-({Fore.RED}HTTP Error{Fore.RESET}")
            return e
        except requests.exceptions.Timeout as e:
            print(f"({Fore.RED}✘{Fore.RESET})-({Fore.RED}Error{Fore.RESET})-({Fore.RED}Timeout{Fore.RESET}")
            return e
        except urllib3.exceptions.ProxySchemeUnknown as e:
            print(f"({Fore.RED}✘{Fore.RESET})-({Fore.RED}Error{Fore.RESET})-({Fore.RED}Proxy Scheme Unknown{Fore.RESET}")
            return e
        except requests.exceptions.TooManyRedirects as e:
            print(f"({Fore.RED}✘{Fore.RESET})-({Fore.RED}Error{Fore.RESET})-({Fore.RED}Too Many Redirects{Fore.RESET}")
            return e

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(checkProxy, proxy) for proxy in proxies]

        for future, proxy in zip(futures, proxies):
            result = future.result()
            if result:
                print(f"({Fore.RED}✘{Fore.RESET})-({Fore.RED}BAD{Fore.RESET}-{Fore.RED}PROXY{Fore.RESET})-({Fore.RED}{proxy}{Fore.RESET}", end='')
                with open('bad.txt', 'a') as fileWithBads:
                    fileWithBads.write(proxy)
                bads += 1
            else:
                print(f"({Fore.LIGHTGREEN_EX}✔{Fore.RESET})-({Fore.LIGHTGREEN_EX}GOOD{Fore.RESET}-{Fore.LIGHTGREEN_EX}PROXY{Fore.RESET})-({Fore.LIGHTGREEN_EX}{proxy}{Fore.RESET}", end='')
                with open('good.txt', 'a') as fileWithGoods:
                    fileWithGoods.write(proxy)
                goods += 1

    print("")
    print("")
    print(f"{Fore.LIGHTGREEN_EX} {goods} PROXIES REPLIED ")
    print(f"{Fore.LIGHTRED_EX} {bads} PROXIES DIDN'T REPLY ")

# Scrape proxies
def getProxies():
    request = requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=1000&country=all&ssl=all&anonymity=all')
    with open("proxies.txt","wb") as fp:
        fp.write(request.content)
        print("")
        print("")
        print(f"({Fore.LIGHTGREEN_EX}✔{Fore.RESET})-({Fore.LIGHTGREEN_EX}Success{Fore.RESET})-({Fore.LIGHTGREEN_EX}HTTP Proxies Scraped{Fore.RESET}")

#command logic
if len(argv) > 1:
    commands = ['--help', '-h', '-f', '-p', '-t', '-rd', '-gp']
    if argv[1] in commands:
        if argv[1] in ('--help', '-h'):
            printHelp()
        elif argv[1] == '-f':
            try:
                file = open(argv[2])
                proxies = list(file)
                num_threads = 1
                if '-t' in argv:
                    t_index = argv.index('-t')
                    if len(argv) > t_index + 1:
                        num_threads = int(argv[t_index + 1])
                terminal(CMD_CLEAR_TERM)
                checkProxies(proxies, num_threads)
            except IndexError:
                print(f"({Fore.RED}✘{Fore.RESET})-({Fore.RED}Error{Fore.RESET})-({Fore.RED}Missing File Name{Fore.RESET}")
        elif '-rd' in argv:
            try:
                with open(argv[2], 'r') as f:
                    proxies = list(set(f.readlines()))
                with open(argv[2], 'w') as f:
                    f.writelines(proxies)
                print(f"({Fore.LIGHTGREEN_EX}✔{Fore.RESET})-({Fore.LIGHTGREEN_EX}Complete{Fore.RESET})-({Fore.GREEN}All Duplicates Removed{Fore.RESET}")
            except FileNotFoundError:
                print(f"({Fore.RED}✘{Fore.RESET})-({Fore.RED}Error{Fore.RESET})-({Fore.RED}File Not Found{Fore.RESET}")
            except Exception as e:
                print(f"({Fore.RED}✘{Fore.RESET})-({Fore.RED}Error{Fore.RESET})-({Fore.RED}{e}{Fore.RESET}")
        elif argv[1] == '-p':
            try:
                argv[2] = argv[2].split(' ')[0]
                threadlessCheckProxy(argv[2])
            except IndexError:
                print(f"({Fore.RED}✘{Fore.RESET})-({Fore.RED}Error{Fore.RESET})-({Fore.RED}Missing Proxy Info{Fore.RESET}")
        elif argv[1] == '-gp':
            getProxies()
        else:
            print(Fore.LIGHTRED_EX + 'Unknown option "' + argv[1] + '"')
    else:
        printHelp()
