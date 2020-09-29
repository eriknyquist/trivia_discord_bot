import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TriviaQuestion(object):
    def __init__(self, category, question, answers, correct_answer):
        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer
        self.category = category

    def correct_answer_index(self):
        return self.answers.index(self.correct_answer)


class TriviaDB(object):
    def __init__(self):
        pass

    def get_questions(self, num=1):
        raise NotImplementedError()


class TriviaSession(object):
    def __init__(self, channel):
        self.channel = channel
        self.thread = None
        self.trivia = None
        self.responses = []

    def session_id(self):
        return "%d:%d" % (self.channel.guild.id, self.channel.id)

    def __str__(self):
        return self.session_id()

    def __repr__(self):
        return self.session_id()
