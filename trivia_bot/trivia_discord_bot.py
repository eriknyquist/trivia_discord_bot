import logging

from trivia_bot.trivia import TriviaSession
from trivia_bot.discord_bot import DiscordBot, MessageResponse
from trivia_bot.command_processor import CommandProcessor, trivia_bot_command_list


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TriviaDiscordBot(DiscordBot):
    def __init__(self, config):
        super(TriviaDiscordBot, self).__init__(config)
        self.cmdprocessor = CommandProcessor(config, self, trivia_bot_command_list)

    def on_mention(self, message):
        if not message.channel:
            return None

        msg = message.content.replace(self.mention(), '').replace(self.nickmention(), '')
        session = TriviaSession(message.channel.guild.id, message.channel.id)
        resp = self.cmdprocessor.process(msg, session)

        if resp is not None:
            return MessageResponse(resp, channel=message.channel)
