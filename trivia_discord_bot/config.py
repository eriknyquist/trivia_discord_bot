import json
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


DISCORD_TOKEN_KEY = "discord_bot_api_token"
DISCORD_TOKEN_DEFAULT = ""

TRIVIA_ANSWER_TIME_KEY = "trivia_answer_time_seconds"
TRIVIA_ANSWER_TIME_DEFAULT = 30

SCORE_ARCHIVE_KEY = "score_archive"
SCORE_ARCHIVE_DEFAULT = {}


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
            self.scores = SCORE_ARCHIVE_DEFAULT
        else:
            # Load provided config file
            self.load_from_file(filename)

    def load_from_file(self, filename):
        logger.info("loading configuration from %s", filename)

        with open(filename, 'r') as fh:
            attrs = json.load(fh)

        self.discord_token = load_cfg_default(attrs, DISCORD_TOKEN_KEY, DISCORD_TOKEN_DEFAULT)
        self.answer_time_seconds = load_cfg_default(attrs, TRIVIA_ANSWER_TIME_KEY, TRIVIA_ANSWER_TIME_DEFAULT)
        self.scores = load_cfg_default(attrs, SCORE_ARCHIVE_KEY, SCORE_ARCHIVE_DEFAULT)

        return self

    def save_to_file(self, filename=None):
        if filename is None:
            filename = self.filename

        logger.info("saving configuration to %s", filename)

        with open(filename, 'w') as fh:
            json.dump({
                DISCORD_TOKEN_KEY: self.discord_token,
                TRIVIA_ANSWER_TIME_KEY: self.answer_time_seconds,
                SCORE_ARCHIVE_KEY: self.scores
            }, fh, indent=4)

    def update_score(self, user, winner=False):
        user_id = str(user.id)

        if user_id in self.scores:
            old = self.scores[user_id]

            new = [
                user.name,                         # Discord display name for user
                old[1] + 1,                        # Total trivia questions participated in
                (old[2] + 1) if winner else old[2] # Trivia questions correctly answered
            ]

            self.scores[user_id] = new
        else:
            self.scores[user_id] = (user.name, 1, 1 if winner else 0)

    def get_score(self, user_id):
        user_id = str(user_id)

        if user_id not in self.scores:
            return None, None

        return tuple(self.scores[user_id])
