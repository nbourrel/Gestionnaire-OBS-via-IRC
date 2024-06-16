import threading
import time

class PlayerCountTimer:
    def __init__(self, irc_bot, obs):
        self.irc_bot = irc_bot
        self.obs = obs
        self._stop_event = threading.Event()

    def start(self):
        while not self._stop_event.is_set():
            try:
                response = self.irc_bot.get_server_info()
                current_map = response["servers"][0]["info"]["map"]
                game_state = response["servers"][0]["rules"]["g_gameState"]
                player_count = len(response["servers"][0]["players"])
                player_names = [player["name"] for player in response["servers"][0]["players"]]

                if self._can_login_to_obs():
                    if player_count < 2:
                        self.obs.setEmpty()
                    elif player_count == 2:
                        self.obs.setNeedOne()
                    elif player_count >= 3:
                        if game_state == "PRE_GAME":
                            self.obs.setPreGame()
                        elif game_state == "COUNT_DOWN":
                            self.obs.setWarmUp()
                        elif game_state == "IN_PROGRESS":
                            self.obs.setInGame()
                    self.obs.obs_logout()
            except Exception as e:
                # Optionally log the error to a file or logging system
                pass

            time.sleep(1)

    def stop(self):
        self._stop_event.set()

    def _can_login_to_obs(self):
        try:
            self.obs.obs_login()
            return True
        except Exception:
            return False
    def stop(self):
        self._stop_event.set()