import requests
import html
import logging
import random
import time

from trivia_discord_bot.trivia import TriviaDB, TriviaQuestion

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class OpenTDBTriviaDB(TriviaDB):
    def __init__(self):
        random.seed(time.time())

    def get_question(self):
        dburl = "https://opentdb.com/api.php?amount=1"
        resp = requests.get(url=dburl)
        attrs = resp.json()

        q = attrs["results"][0]

        correct_answer = html.unescape(q["correct_answer"])

        answers = (
            [correct_answer] +
            [html.unescape(x) for x in q["incorrect_answers"]]
        )

        random.shuffle(answers)

        newq = TriviaQuestion(html.unescape(q["category"]),
                              html.unescape(q["question"]),
                              answers,
                              correct_answer)

        return newq
