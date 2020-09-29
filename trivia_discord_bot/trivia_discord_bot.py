import logging

from trivia_discord_bot.trivia import TriviaSession
from trivia_discord_bot.discord_bot import DiscordBot, MessageResponse
from trivia_discord_bot.command_processor import build_command_processor


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TriviaDiscordBot(DiscordBot):
    def __init__(self, config):
        super(TriviaDiscordBot, self).__init__(config)
        self.cmdprocessor = build_command_processor(config, self)

    def on_mention(self, message):
        if not message.channel:
            return None

        msg = message.content.replace(self.mention(), '').replace(self.nickmention(), '')
        session = TriviaSession(message.channel)

        if self.cmdprocessor.is_command(msg):
            resp = self.cmdprocessor.process_command(msg, message.author, session)
        else:
            resp = self.cmdprocessor.process_message(msg, message.author, session)

        if resp is not None:
            return MessageResponse(resp, channel=message.channel)
