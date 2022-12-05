import enum

class Command(enum.Enum):
    COMMIT = "C"
    WRITE = "W"
    READ = "R"


class Item:
    def __init__(self, label, version=0, read_ts=0, write_ts=0):
        self.label = label
        self.version = version
        self.read_ts = read_ts
        self.write_ts = write_ts
        self.subscriber_ids: list[int] = []

    def __str__(self):
        return f'{self.label}_{self.version}(R{self.read_ts},W{self.write_ts})'


class Transaction():
    def __init__(self, transaction_id, ts):
        self.transaction_id = transaction_id
        self.ts = ts
        self.arr_process: list[Operation] = []
        self.created_items: list[Item] = []

    def __str__(self):
        return f"{self.transaction_id}: [{';'.join(map(lambda x: str(x), self.arr_process))}]"


class VersionControl:
    def __init__(self):
        self.map: dict[str, list[Item]] = {}

    def add_new_version(self, item: Item):
        if item.label not in self.map:
            self.map.update({item.label: [item]})
        else:
            self.map[item.label].append(item)

    def get(self, label: str):
        return self.map[label]

    def __str__(self):
        str = ""
        for key in self.map:
            str += f"{key}: ["
            for item in self.map[key]:
                str += f"{item};"
            str += "]\n"
        return str


class Operation:
    def __init__(self, str: str):
        temp = str.split("(")

        self.operation = str[0]
        self.transaction_id = int(temp[0][1:])
        if len(temp) > 1:
            self.item = Item(temp[1][:-1])

    def __str__(self):
        return f"Operation: {self.operation}, Transaction ID: {self.transaction_id}" + (f", Item: {self.item.label}" if hasattr(self, "item") else "")

    def __eq__(self, other):
        selfHas = hasattr(self, "item")
        otherHas = hasattr(other, "item")

        if selfHas != otherHas:
            return False

        return self.operation == other.operation and self.transaction_id == other.transaction_id and (not selfHas or self.item == other.item)

    def format(self):
        return f"{self.operation}{self.transaction_id}" + (f"({self.item.label})" if hasattr(self, "item") else "")
