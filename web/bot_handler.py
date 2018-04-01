import logging
import threading

from web.bot.bots import SendingError, create_bot_from_json


def bot_iter(bot):
    ok = True
    try:
        bot.load_updates()
    except ConnectionError:
        logging.error('Connection error (bot iter)', filename='log.txt')
        ok = False

    if bot.updates and ok:
        try:
            for update in bot.updates:
                bot.send_message(update)
                bot.updates.remove(update)
        except ConnectionError:
            logging.error('Connection error (sending message, bot iter)', filename='log.txt')
            ok = False
        except SendingError:
            logging.error('Sending error (bot iter)', filename='log.txt')
            ok = False

    return ok


def load_bot():
    f = open('web/bot.txt', 'r')
    jsoned_bot = f.readline()
    f.close()
    bot = create_bot_from_json(jsoned_bot)

    return bot


class BotThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.is_active = False
        self.lock = threading.Lock()

    def run(self):
        self.is_active = True
        with self.lock:
            bot = load_bot()
        while self.is_active:
            ok = bot_iter(bot)
            if not ok or not self.is_active:
                break
        with self.lock:
            bot.save_bot()
