import argparse
import time
import random
import os
import logging

from trivia_bot.trivia_discord_bot import TriviaDiscordBot
from trivia_bot.config import BotConfig


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


DEFAULT_CONFIG_FILE = "default_bot_config.json"


def check_streamers(config, monitor, bot, host_user):
    channels = monitor.read_all_streamer_info()
    msgs = []

    # If configured, check whether host is streaming before
    # making any announcements
    if config.silent_during_host_stream:
        if host_user is not None:
            host = monitor.read_streamer_info(host_user)
            if host.is_live:
                # Host is streaming, make no announcements
                return []

    # Check for any announcements that need to be made
    for c in channels:
        if c.name in streamers:
            if c.is_live and (not streamers[c.name].is_live):
                logger.debug("streamer %s went live" % c.name)
                format_args[FMT_TOK_STREAMER_NAME] = c.name
                format_args[FMT_TOK_STREAM_URL] = c.url
                fmtstring = random.choice(config.stream_start_messages)
                msgs.append(fmtstring.format(**format_args))

        streamers[c.name] = c

    return msgs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', default=None, nargs='?',
            help="Path to bot config file (default=%(default)s)")

    args = parser.parse_args()

    if args.config_file is None:
        b = BotConfig()
        b.save_to_file(DEFAULT_CONFIG_FILE)
        print("Created default config file '%s', please add required parameters" %
              DEFAULT_CONFIG_FILE)
        return

    config = BotConfig(args.config_file)

    bot = TriviaDiscordBot(config)

    try:
        bot.run()
    except KeyboardInterrupt:
        bot.stop()

if __name__ == "__main__":
    main()
