import http.server
import socketserver
import subprocess
import platform
import os

def check_tor_is_present():
    try:
        result = subprocess.run(['which', "tor"], capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            return False
    except FileNotFoundError:
        return False

def install_tor():
    if platform.system() == "Linux":
        os.system("apt install tor")
    else:
        print("You are using {} os, But this tool is only design for Linux.").format(platform.system)

def torrc_configuration_startmode(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if lines[-2] == "HiddenServiceDir /var/lib/tor/hidden_service/\n":
                pass
            else:
                lines.append("HiddenServiceDir /var/lib/tor/hidden_service/\n")
            
            if lines[-1] == "HiddenServicePort 80 127.0.0.1:80":
                pass
            else:
                lines.append("HiddenServicePort 80 127.0.0.1:80")

        with open(filename, 'w') as file:
            file.writelines(lines)
    except FileNotFoundError:
        print("torrc file not present in your system")


def home_logo():
    print("""
        ####   ##     ##      ###        #####      #######     ####### 
         ##    ##     ##     ## ##      ##   ##    ##     ##   ##     ##
         ##    ##     ##    ##   ##    ##     ##   ##     ##   ##     ##
         ##    #########   ##     ##   ##     ##    #######     ########
         ##    ##     ##   #########   ##     ##   ##     ##          ##
         ##    ##     ##   ##     ##    ##   ##    ##     ##   ##     ##
        ####   ##     ##   ##     ##     #####      #######     #######
    
IHA089: Navigating the Digital Realm with Code and Security - Where Programming Insights Meet Cyber Vigilance.
    """)

def torrc_configuration_stopmode(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if lines[-2] == "HiddenServiceDir /var/lib/tor/hidden_service/\n":
                lines.pop(-2)
            
            if lines[-1] == "HiddenServicePort 80 127.0.0.1:80":
                lines.pop(-1)

        with open(filename, 'w') as file:
            file.writelines(lines)
    except FileNotFoundError:
        print("torrc file not present in your system")

def HTTP_SERVER(PORT):
    handler = http.server.SimpleHTTPRequestHandler
    server = socketserver.TCPServer(("localhost", PORT), handler)
    server.serve_forever()

def Main():
    home_logo()
    if not check_tor_is_present():
        prin("Tor is not installed on your system")
        print("Installing tor....")
        install_tor()
    else:
        port = 80
        filename = "/etc/tor/torrc"
        try:
            torrc_configuration_startmode(filename)
            os.system("service tor start")
            with open("/var/lib/tor/hidden_service/hostname", 'r') as file:
                url = file.read()
            print("Onion URL ::: http://"+url)
            HTTP_SERVER(port)
        except KeyboardInterrupt:
            print("Stoping...")
            os.system("service tor stop")
            torrc_configuration_stopmode(filename)

if __name__ == "__main__":
    Main()