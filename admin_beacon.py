import requests
import threading
import argparse
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

#suppression of SSL Certificate error 
warnings.filterwarnings("ignore", message="Unverified HTTPS request", category=InsecureRequestWarning)

parser = argparse.ArgumentParser()
parser.add_argument("-u", help="target url", dest='target')
parser.add_argument("--path", help="custom path prefix", dest='prefix')
parser.add_argument("--type", help="set the type i.e. html, asp, php", dest='type')
parser.add_argument("--fast", help="uses multithreading", dest='fast', action="store_true")
args = parser.parse_args()

target = args.target

# Banner :p
print('''\033[1;34m______   ______ _______ _______ _______ _     _ _______  ______

░█████╗░██████╗░███╗░░░███╗██╗███╗░░██╗  ██████╗░███████╗░█████╗░░█████╗░░█████╗░███╗░░██╗
██╔══██╗██╔══██╗████╗░████║██║████╗░██║  ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗████╗░██║
███████║██║░░██║██╔████╔██║██║██╔██╗██║  ██████╦╝█████╗░░███████║██║░░╚═╝██║░░██║██╔██╗██║
██╔══██║██║░░██║██║╚██╔╝██║██║██║╚████║  ██╔══██╗██╔══╝░░██╔══██║██║░░██╗██║░░██║██║╚████║
██║░░██║██████╔╝██║░╚═╝░██║██║██║░╚███║  ██████╦╝███████╗██║░░██║╚█████╔╝╚█████╔╝██║░╚███║
╚═╝░░╚═╝╚═════╝░╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝  ╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░░╚════╝░╚═╝░░╚══╝

                          \033[37mMade with \033[91m<3\033[37m By Anvi\033[1;m''')

print('\033[1;31m--------------------------------------------------------------------------\033[1;m\n')

try:
    target = target.replace('https://', '')
except:
    print('\033[1;31m[-]\033[1;m -u argument is not supplied. Enter python admin-beacon -h for help')
    quit()

target = target.replace('http://', '')
target = target.replace('/', '')
target = 'http://' + target

if args.prefix is not None:
    target = target + args.prefix

try:
    r = requests.get(target + '/robots.txt', verify=False)
    if '<html>' in r.text:
        print('  \033[1;31m[-]\033[1;m Robots.txt Undiscovered\n')
    else:
        print('  \033[1;32m[+]\033[0m Robots.txt Discovered\n')
        print(r.text)
except requests.exceptions.SSLError:
    print('  \033[1;31m[-]\033[1;m SSL error occurred. Please check the SSL certificate of the target URL.')
except requests.exceptions.RequestException:
    print('  \033[1;31m[-]\033[1;m Failed to fetch robots.txt\n')

print('\033[1;31m--------------------------------------------------------------------------\033[1;m\n')

def scan(links):
    for link in links:
        link = target + link
        try:
            response = requests.get(link, verify=False)  # Disable SSL certificate verification
            if response.status_code == 200:
                content_length = response.headers.get("Content-Length")
                print("Content Length:", content_length)
                print('  \033[1;32m[+]\033[0m Admin panel discovered: %s (Content Length: %s)' % (link, content_length))
            elif response.status_code == 404:
                print('  \033[1;31m[-]\033[1;m %s' % link)
            elif response.status_code == 302:
                print('  \033[1;32m[+]\033[0m EAR vulnerability discovered : ' + link)
            else:
                print('  \033[1;31m[-]\033[1;m %s' % link)
        except requests.exceptions.SSLError:
            print('  \033[1;31m[-]\033[1;m SSL error occurred. Please check the SSL certificate of the target URL.')
        except requests.exceptions.RequestException:
            print('  \033[1;31m[-]\033[1;m Failed to fetch %s\n' % link)

paths = []

def get_paths(type):
    try:
        with open('paths.txt', 'r') as wordlist:
            for path in wordlist:
                path = str(path.replace("\n", ""))
                try:
                    if 'asp' in type:
                        if 'html' in path or 'php' in path:
                            pass
                        else:
                            paths.append(path)
                    if 'php' in type:
                        if 'asp' in path or 'html' in path:
                            pass
                        else:
                            paths.append(path)
                    if 'html' in type:
                        if 'asp' in path or 'php' in path:
                            pass
                        else:
                            paths.append(path)
                except:
                    paths.append(path)
    except IOError:
        print('\033[1;31m[-]\033[1;m Wordlist not found!')
        quit()

if args.fast:
    type = args.type
    get_paths(type)
    paths1 = paths[:len(paths) // 2]
    paths2 = paths[len(paths) // 2:]

    def part1():
        links = paths1
        scan(links)

    def part2():
        links = paths2
        scan(links)

    t1 = threading.Thread(target=part1)
    t2 = threading.Thread(target=part2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
else:
    type = args.type
    get_paths(type)
    links = paths
    scan(links)
