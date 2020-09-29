import os
import discord
import asyncio
import logging

from trivia_discord_bot.command_processor import CommandProcessor, trivia_bot_command_list


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

main_event_loop = asyncio.get_event_loop()


class MessageResponse(object):
    def __init__(self, response_data, channel=None, member=None):
        self.channel = channel
        self.member = member
        self.response_data = response_data

class DiscordBot(object):
    def __init__(self, config):
        self.token = config.discord_token
        self.config = config
        self.client = discord.Client()

        @self.client.event
        async def on_connect():
            self.on_connect()

        @self.client.event
        async def on_member_join(member):
            self.on_member_join(member)

        @self.client.event
        async def on_message(message):
            resp = None

            if (self.mention() in message.content) or (self.nickmention() in message.content):
                resp = self.on_mention(message)
            else:
                resp = self.on_message(message)

            if resp is None:
                return

            if resp.member is not None:
                # Response should be sent in a DM to given member
                await message.author.create_dm()
                await message.author.dm_channel.send(resp.response_data)
            elif resp.channel is not None:
                # Response should be sent on the given channel
                await resp.channel.send(resp.response_data)
            else:
                raise RuntimeError("malformed response: either member or "
                                   "channel must be set")

    def mention(self):
        return "<@%d>" % self.client.user.id

    def nickmention(self):
        return"<@!%d>" % self.client.user.id

    def name(self):
        return self.client.user.name

    def run(self):
        self.client.run(self.token)

    def stop(self):
        self.client.logout()

    def send_message(self, message, channel):
        asyncio.run_coroutine_threadsafe(channel.send(message), main_event_loop)

    def on_connect(self):
        pass

    def on_member_join(self, member):
        pass

    def on_message(self, message):
        pass

    def on_mention(self, message):
        pass

def main():
    bot = build_sketi_bot()
    bot.run()

if __name__ == "__main__":
    main()
