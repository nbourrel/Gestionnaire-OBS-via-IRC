import threading
from src.ircbot import IRCBot
from src.player_count_timer import PlayerCountTimer
from src.discordbot import DiscordClient
if __name__ == "__main__":
    bot = IRCBot("config/config.json")
    bot_thread = threading.Thread(target=bot.start_bot)
    bot_thread.start()
    timer = PlayerCountTimer(bot, bot.obs)
    timer_thread = threading.Thread(target=timer.start)
    timer_thread.start()
    dscbot = DiscordClient(command_prefix='!')
    dscbot_thread = threading.Thread(target=dscbot.run("TOKEN"))
    dscbot_thread.start()
    dscbot_thread.join()
    bot_thread.join()
    timer_thread.join()