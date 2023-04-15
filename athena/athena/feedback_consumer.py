from typing import Callable
from functools import wraps

from athena import _app
from .models import Exercise, Submission, Feedback
from .storage import store_feedback

def feedback_consumer(func: Callable[[Exercise, Submission, Feedback], None]):
    @_app.post("/feedback")
    @wraps(func)
    def wrapper(exercise: Exercise, submission: Submission, feedback: Feedback):
        store_feedback(feedback)
        func(exercise, submission, feedback)
    return wrapper