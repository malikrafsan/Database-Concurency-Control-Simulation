import enum


class TransactionStatus(enum.Enum):
    ABORTED = "X"
    AVAILABLE = "A"
    WAITING = "W"
    COMMITED = "C"


class Command(enum.Enum):
    COMMIT = "C"
    WRITE = "W"
    READ = "R"
