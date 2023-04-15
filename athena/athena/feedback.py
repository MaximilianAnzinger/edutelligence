from athena import _app
from .models import Feedback
from .storage import store_feedback

def receives_feedback(new_only=True, update_only=False):
    if new_only and update_only:
        raise ValueError("new_only and update_only cannot both be True")
    def decorator(func):
        @_app.post("/feedback")
        def wrapper(feedback: Feedback):
            store_feedback(feedback)
            if new_only and feedback.id is not None:
                return
            if update_only and feedback.id is None:
                return
            func(feedback)
        return wrapper
    return decorator