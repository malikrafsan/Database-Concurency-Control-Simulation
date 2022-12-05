class Operation:
    def __init__(self, str: str):
        temp = str.split("(")

        self.operation = str[0]
        self.transaction_id = int(temp[0][1:])
        if len(temp) > 1:
            self.item = temp[1][:-1]

    def __str__(self):
        return f"Operation: {self.operation}, Transaction ID: {self.transaction_id}" + (f", Item: {self.item}" if hasattr(self, "item") else "")

    def __eq__(self, other):
        # handle if self or other doesn't have item attribute
        selfHas = hasattr(self, "item")
        otherHas = hasattr(other, "item")
        
        if selfHas != otherHas:
            return False
        
        return self.operation == other.operation and self.transaction_id == other.transaction_id and (not selfHas or self.item == other.item)
        