import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TriviaQuestion(object):
    def __init__(self, category, question, answers, correct_answer):
        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer
        self.category = category


class TriviaDB(object):
    def __init__(self):
        pass

    def get_questions(self, num=1):
        raise NotImplementedError()


class TriviaSession(object):
    def __init__(self, guild_id, channel_id):
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.responses = []

    def __str__(self):
        return "%d:%d" % (self.guild_id, self.channel_id)
