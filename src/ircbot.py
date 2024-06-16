import socket
import requests
import time
import json
import re
from colorama import Fore, Style, init
from src.obs_controller import ObsWebSocket

init() # colorama
class IRCBot:
    def __init__(self, config_file):
        with open(config_file) as f:
            config = json.load(f)
            self.obs_config = config["obs"]
            self.twitch_config = config["twitch"]
            self.syncore_config = config["syncore"]
        self.irc_socket = None
        self.obs = ObsWebSocket(address=self.obs_config["ip"], port=self.obs_config["port"], password=self.obs_config["password"])

    def start_bot(self):
        self.irc_socket = self.irc_login()
        if self.irc_socket:
            self.listen_irc()

    def irc_login(self):
        print(f"Connecting to IRC server: {self.twitch_config['server']}:{self.twitch_config['port']}")
        print(f"Joining channel: {self.twitch_config['channel']}")

        irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            irc_socket.connect((self.twitch_config['server'], self.twitch_config['port']))
            irc_socket.send(f"CAP REQ :{self.twitch_config['cap']}\r\n".encode())
            irc_socket.send(f"PASS {self.twitch_config['oauth']}\r\n".encode())
            irc_socket.send(f"NICK {self.twitch_config['username']}\r\n".encode())

            print("[LOG] IRC Bot: Successfully logged in to IRC.")
            irc_socket.send(f"JOIN {self.twitch_config['channel']}\r\n".encode())
            return irc_socket
        except Exception as e:
            print("An error occurred during IRC login:", e)
            return None

    def listen_irc(self):
        with open("irc_log.txt", "a") as log_file:
            motd_received = False
            try:
                while True:
                    server_response = self.irc_socket.recv(2048).decode('ascii', 'ignore')
                    if not server_response:
                        break

                    log_file.write(server_response)

                    if not motd_received:
                        if "376" in server_response:
                            motd_received = True
                            print("[IRC] End of MOTD.")
                        continue

                    if "PING" in server_response:  # Ignore PING/PONG messages
                        self.irc_socket.send("PONG :tmi.twitch.tv\r\n".encode())
                        continue

                    self.handle_irc_message(server_response)
            except Exception as e:
                print("An error occurred during IRC communication:", e)
            finally:
                self.irc_socket.close()
                
    def send_message(self, message):
        if self.irc_socket:
            try:
                self.irc_socket.send(f"PRIVMSG {self.twitch_config['channel']} :{message}\r\n".encode())
            except Exception as e:
                print("An error occurred while sending message:", e)
        else:
            print("IRC socket is not connected.")
            
    def handle_irc_message(self, message):
        nickname_pattern = re.compile(r":([^!]+)!")
        nickname_match = nickname_pattern.search(message)
        if nickname_match:
            nickname = nickname_match.group(1)
        else:
            nickname = ""

        content_pattern = re.compile(r"PRIVMSG #([^ ]+) :([^\x00-\x1F\x7F-\x9F]+)")
        content_match = content_pattern.search(message)
        if content_match:
            channel = content_match.group(1)
            content = content_match.group(2)
        else:
            channel = ""
            content = ""

        if nickname and channel and content:
            print(f"{Fore.WHITE}[#{channel.upper()}]{Fore.RED}<{nickname}{Fore.WHITE}@{Fore.BLUE}{channel}> {Fore.GREEN}{content}{Style.RESET_ALL}")
            if content.split():
                if content.startswith('!'):
                    command = content.split()[0]
                    if command == "!rezo" or command == "!rézo" or command == "!socials" or command == "!links" or command == "!onlyfans":
                        self.send_message("Find all my socials here : https://linktr.ee/YOUR-USER :o)")
                    if nickname in self.twitch_config['admins']:
                        if command == 'empty':
                            self.obs.obs_login()
                            self.obs.setEmpty()

    def get_server_info(self):
        response = requests.get(f"{self.syncore_config['url']}?ids={self.syncore_config['serverid']}")
        return response.json()