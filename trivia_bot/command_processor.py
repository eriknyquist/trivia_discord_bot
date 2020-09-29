import time
import threading

from trivia_bot.trivia import TriviaSession
from trivia_bot.opentdb_trivia import OpenTDBTriviaDB

active_sessions = {}
trivia_db = OpenTDBTriviaDB()

COMMAND_PREFIX = "!"

CMD_HELP_HELP = """
{0} [command]

Shows helpful information about the given command. Replace [command] with the
command you want help with.
"""

CMD_TRIVIA_HELP = """
{0}

Commands the bot to retrieve a trivia question from the database and post it in a message.
"""

class Command(object):
    def __init__(self, word, handler, helptext):
        self.word = word
        self.handler = handler
        self.helptext = helptext

    def help(self):
        return "```%s```" % self.helptext.format(self.word)


class CommandProcessor(object):
    def __init__(self, config, bot, command_list, message_handler):
        self.config = config
        self.bot = bot
        self.cmds = {x.word: x for x in command_list}
        self.message_handler = message_handler

    def help(self):
        return "Available commands:\n```%s```" % "\n".join(self.cmds.keys())

    def is_command(self, text):
        return text.strip().startswith(COMMAND_PREFIX)

    def process_message(self, text, author, session):
        text = text.strip()
        if self.is_command(text):
            return None

        return self.message_handler(self, session, self.config, author, text)

    def process_command(self, text, author, session):
        text = text.strip()
        if not self.is_command(text):
            return None

        words = text.lstrip(COMMAND_PREFIX).split()
        command = words[0].lower()

        if command in self.cmds:
            return self.cmds[command].handler(self, session, self.config, author, words[1:])

        return "Sorry, I don't recognize the command '%s'" % command

def trivia_handler_thread(proc, config, session_id):
    time.sleep(config.answer_time_seconds)

    session = active_sessions[session_id]
    proc.bot.send_message("Trivia time is up!", session.channel)

    del active_sessions[session_id]

def cmd_help(proc, session, config, author, args):
    if len(args) == 0:
        return proc.help()

    cmd = args[0].strip()
    if cmd.startswith(COMMAND_PREFIX):
        cmd = cmd.lstrip(COMMAND_PREFIX)

    if cmd not in proc.cmds:
        return "No command '%s' to get help for" % cmd

    return proc.cmds[cmd].help()

def cmd_trivia(proc, session, config, author, args):
    session_id = session.session_id()

    if session_id in active_sessions:
        return "Chill out bro, there's already a trivia question in progress!"

    q = trivia_db.get_question()
    answers = "\n".join(["```%d. %s```" % (i + 1, q.answers[i]) for i in range(len(q.answers))])

    session.trivia = q

    session.thread = threading.Thread(target=trivia_handler_thread,
                                      args=(proc, config, session_id))
    session.thread.daemon = True
    session.thread.start()

    active_sessions[session_id] = session

    return ("%s\n\n%s\n\n (You have %d seconds to respond with the number of your "
            "desired answer, make sure to mention me!)" % (q.question, answers,
                                                           config.answer_time_seconds))

trivia_bot_command_list = [
    Command("help", cmd_help, CMD_HELP_HELP),
    Command("trivia", cmd_trivia, CMD_TRIVIA_HELP)
]

def message_handler(proc, session, config, author, text):
    session_id = session.session_id()

    if session_id not in active_sessions:
        # No active trivia question in this channel
        return "No active trivia session. Use the '!trivia' command to start one."

    session = active_sessions[session_id]

    # Check if this user already gave an answer
    for existing_author, existing_answer in session.responses:
        if author.id == existing_author.id:
            return "%s, I already have an answer from you" % author.mention

    field = text.strip().split()[0]

    try:
        answer = int(field)
    except:
        return "%s Umm... '%s' is not a number" % (author.mention, field)

    if answer > len(session_id):
        return ("%s '%d' is not a valid answer, please provide a number between 1-%d" %
                (author.mention, answer, len(session.trivia.answers)))

    session.responses.append((author, answer))

def build_command_processor(config, bot):
    return CommandProcessor(config, bot, trivia_bot_command_list, message_handler)
