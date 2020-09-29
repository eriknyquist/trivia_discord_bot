import requests
import html
import logging

from trivia_discord_bot.trivia import TriviaDB, TriviaQuestion

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class OpenTDBTriviaDB(TriviaDB):
    def __init__(self):
        pass

    def get_question(self):
        dburl = "https://opentdb.com/api.php?amount=1"
        resp = requests.get(url=dburl)
        attrs = resp.json()

        q = attrs["results"][0]
        
        answers = (
            [html.unescape(q["correct_answer"])] + 
            [html.unescape(x) for x in q["incorrect_answers"]]
        )

        newq = TriviaQuestion(html.unescape(q["category"]),
                              html.unescape(q["question"]),
                              answers,
                              answers[0])

        return newq
