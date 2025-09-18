from enum import Enum


class Status(str, Enum):
    not_completed = "not_completed"
    in_progress = "in_progress"
    completed = "completed"
