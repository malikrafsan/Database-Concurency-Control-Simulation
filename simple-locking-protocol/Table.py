from enums import TransactionStatus
from Operation import Operation


class LockTable:
    def __init__(self, locked_item, transaction_id):
        self.locked_item = locked_item
        self.transaction_id = transaction_id


class TransactionTable:
    def __init__(self, transaction_id: int, transaction_status: TransactionStatus, timestamp: int):
        self.transaction_id = transaction_id
        self.transaction_status = transaction_status
        self.timestamp = timestamp
        self.locked_items: list[str] = []
        self.all_operations: list[Operation] = []
    
    def add_operation(self, operation: Operation):
        self.all_operations.append(operation)

    def add_locked_item(self, locked_item: str):
        self.locked_items.append(locked_item)

    def change_transaction_status(self, status: TransactionStatus):
        self.transaction_status = status

    def __str__(self):
        return f"Transaction ID: {self.transaction_id} | Status: {self.transaction_status} | Timestamp: {self.timestamp} | Locked Items: {self.locked_items} | Operations: [{';'.join(map(lambda x: x.__str__(), self.all_operations))}]"
