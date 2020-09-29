import json
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


DISCORD_TOKEN_KEY = "discord_bot_api_token"
DISCORD_TOKEN_DEFAULT = ""

TRIVIA_ANSWER_TIME_KEY = "trivia_answer_time_seconds"
TRIVIA_ANSWER_TIME_DEFAULT = 60


def load_cfg_default(attrs, key, default):
    if key in attrs:
        return attrs[key]

    return default

class BotConfig(object):
    @classmethod
    def from_file(cls, filename):
        return BotConfig(filename)
    
    def __init__(self, filename=None):
        self.filename = filename
        if filename is None:
            # No filename passed- use default values
            self.discord_token = DISCORD_TOKEN_DEFAULT
            self.answer_time_seconds = TRIVIA_ANSWER_TIME_DEFAULT
        else:
            # Load provided config file
            self.load_from_file(filename)

    def load_from_file(self, filename):
        logger.info("loading configuration from %s", filename)

        with open(filename, 'r') as fh:
            attrs = json.load(fh)

        self.discord_token = load_cfg_default(attrs, DISCORD_TOKEN_KEY, DISCORD_TOKEN_DEFAULT)
        self.answer_time_seconds = load_cfg_default(attrs, TRIVIA_ANSWER_TIME_KEY, TRIVIA_ANSWER_TIME_DEFAULT)

        return self

    def save_to_file(self, filename=None):
        logger.info("saving configuration to %s", filename)

        if filename is None:
            filename = self.filename

        with open(filename, 'w') as fh:
            json.dump({
                DISCORD_TOKEN_KEY: self.discord_token,
                TRIVIA_ANSWER_TIME_KEY: self.answer_time_seconds
            }, fh, indent=4)
