from flask_app.utils.questions_holder import questions
from flask_app.utils.graph import questions_config
import random

random.shuffle(questions)
state = {
    "messages": [],
    'questions_asked': 0,
    "questions": questions[:questions_config.max_questions_asked_limit],
    'answers': [],
    "intermediate_results": None,
    'final_suggestion': None,
    'explanation': None
}

