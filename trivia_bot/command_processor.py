from trivia_bot.trivia import TriviaSession
from trivia_bot.opentdb_trivia import OpenTDBTriviaDB

sessions = {}
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
    def __init__(self, config, bot, command_list):
        self.config = config
        self.bot = bot
        self.cmds = {x.word: x for x in command_list}

    def help(self):
        return "Available commands:\n```%s```" % "\n".join(self.cmds.keys())

    def process(self, text, session):
        text = text.strip()
        if not text.startswith(COMMAND_PREFIX):
            return None

        words = text.lstrip(COMMAND_PREFIX).split()
        command = words[0].lower()

        if command in self.cmds:
            return self.cmds[command].handler(self, session, self.config, words[1:])

        return "Sorry, I don't recognize the command '%s'" % command


def cmd_help(proc, session, config, args):
    if len(args) == 0:
        return proc.help()

    cmd = args[0].strip()
    if cmd.startswith(COMMAND_PREFIX):
        cmd = cmd.lstrip(COMMAND_PREFIX)

    if cmd not in proc.cmds:
        return "No command '%s' to get help for" % cmd

    return proc.cmds[cmd].help()

def cmd_trivia(proc, session, config, args):
    session_id = str(session)

    if session_id in sessions:
        return "Chill out bro, there's already a trivia question in progress!"

    sessions[session_id] = session
    q = trivia_db.get_question()
    answers = "\n".join(["```%d. %s```" % (i + 1, q.answers[i]) for i in range(len(q.answers))])

    return ("%s\n\n%s\n\n (Respond with the number of your desired answer, "
            "make sure to mention me!)" % (q.question, answers))

trivia_bot_command_list = [
    Command("help", cmd_help, CMD_HELP_HELP),
    Command("trivia", cmd_trivia, CMD_TRIVIA_HELP)
]
