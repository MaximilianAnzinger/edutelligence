from typing import Callable, List
from functools import wraps

from athena import _app
from .models import Exercise, Submission, Feedback

def feedback_provider(func: Callable[[Exercise, Submission], List[Feedback]]):
    @_app.post("/feedback_suggestions")
    @wraps(func)
    def wrapper(exercise: Exercise, submission: Submission):
        func(exercise, submission)
    return wrapper