from FileHandler import FileHandler
from enums import TransactionStatus, Command
from Table import TransactionTable, LockTable
from Operation import Operation

class SimpleLocking:
    def __init__(self, file_handler: FileHandler):
        self.file_handler = file_handler
        self.operations: list[Operation] = []
        self.waiting_ops: list[Operation] = []
        
        self.lock_table_items: list[LockTable] = []
        self.transaction_table_items: list[TransactionTable] = []
        self.local_timestamp = 1
        self.aborted_transactions: list[TransactionTable] = []

    def run(self):
        while True:
            str = self.file_handler.next_line()
            if str == '':
                break

            self.operations.append(Operation(str))

        print(f"[I]\t Starting to run operations")
        for op in self.operations:
            self.check_begin_operation(op)
            self.run_operation(op)

        print(f"[I]\t Running aborted transactions serially if any")
        for trx in self.transaction_table_items:
            if trx.transaction_status != TransactionStatus.ABORTED:
                continue
            
            print(f"[!]\t Restart transaction {trx.transaction_id}")
            trx.change_transaction_status(TransactionStatus.AVAILABLE)
            for op in trx.all_operations:
                self.run_operation(op)
        
        print(f"[I]\t Program is finished")

    def find_transaction(self, transaction_number: int):
        for transaction in self.transaction_table_items:
            if transaction.transaction_id == transaction_number:
                return transaction
        return None

    def check_begin_operation(self, op: Operation):
        trx = self.find_transaction(op.transaction_id)
        if trx is not None:
            trx.add_operation(op)
        else:
            print(
                f"[B{op.transaction_id}]\t Beginning Transaction Number {op.transaction_id}")
            trx = TransactionTable(
                op.transaction_id, TransactionStatus.AVAILABLE, self.local_timestamp)
            trx.add_operation(op)
            self.transaction_table_items.append(trx)
            self.local_timestamp += 1

    def run_operation(self, op: Operation):        
        status_trx = self.find_transaction(op.transaction_id).transaction_status
        if status_trx == TransactionStatus.WAITING:
            self.waiting_ops.append(op)
            return
        elif status_trx == TransactionStatus.ABORTED:
            return
        
        if op.operation == Command.READ.value:
            self.read_operation(op)
        elif op.operation == Command.WRITE.value:
            self.write_operation(op)
        elif op.operation == Command.COMMIT.value:
            self.commit_operation(op)

    def read_operation(self, op: Operation):
        item = op.item
        trx_id = op.transaction_id
        print(
            f"[R{trx_id}({item})]\t Try to execute READ on {item} in Transaction {trx_id}")
        self.handle_read_write(op)

    def write_operation(self, op: Operation):
        item = op.item
        trx_id = op.transaction_id
        print(
            f"[W{trx_id}({item})]\t Try to execute WRITE on {item} in Transaction {trx_id}")
        self.handle_read_write(op)

    def handle_read_write(self, op: Operation):
        item = op.item
        trx_id = op.transaction_id

        for locked_item in self.lock_table_items:
            if (locked_item.locked_item == item
                    and locked_item.transaction_id != trx_id):
                print(
                    f"[!]\t Conflicting Lock: Item '{item}' is locked by {locked_item.transaction_id}")
                self.handle_wait(self.find_transaction(
                    trx_id), self.find_transaction(locked_item.transaction_id), op)
                return

        for lock in self.lock_table_items:
            if (lock.locked_item == item and lock.transaction_id == trx_id):
                print(f"[!]\t Item '{item}' is already locked by {trx_id}")
                return

        self.lock_table_items.append(LockTable(item, trx_id))
        self.find_transaction(trx_id).add_locked_item(op)
        print(
            f"[XL({item})]\t Locking item '{item}' under Transaction {trx_id}")

    def commit_operation(self, op: Operation):
        print(
            f"[C{op.transaction_id}]\t Committing Transaction {op.transaction_id}")
        self.find_transaction(op.transaction_id).change_transaction_status(TransactionStatus.COMMITED)
        self.handle_unlock(op.transaction_id)
        self.handle_resume()
        
    def handle_unlock(self, transaction_id: int):
        print(
            f"[!]\t Unlocking all items under Transaction {transaction_id}")
        trx = self.find_transaction(transaction_id)
        new_lock_table_items = []
        for lock in self.lock_table_items:
            if (lock.transaction_id != trx.transaction_id):
                new_lock_table_items.append(lock)
        self.lock_table_items = new_lock_table_items
        
    def handle_resume(self):
        print(
            "[?]\t Checking for any waiting transaction that can be resumed after freeing item...")        
        for trx in self.transaction_table_items:
            if trx.transaction_status == TransactionStatus.WAITING:
                print(f"[I]\t Change status of waiting transaction {trx.transaction_id} to available")
                trx.change_transaction_status(TransactionStatus.AVAILABLE)
        
        print(f"[I]\t Try to run waiting operations")
        copy_waiting_ops = self.waiting_ops
        self.waiting_ops = []
        for op in copy_waiting_ops:
            self.run_operation(op)
        
    def handle_wait(self, requester: TransactionTable, holder: TransactionTable, op: Operation):
        if requester.timestamp < holder.timestamp:
            print(f"[A]\t Aborting Transaction {holder.transaction_id}")
            self.handle_abort(holder)
            self.run_operation(op)
        else:
            print(f"[!]\t Change transaction {requester.transaction_id} status to waiting")
            requester.change_transaction_status(TransactionStatus.WAITING)
            self.waiting_ops.append(op)

    def handle_abort(self, trx: TransactionTable):
        trx.change_transaction_status(TransactionStatus.ABORTED)
        new_waiting_ops = []
        for op in self.waiting_ops:
            if op.transaction_id != trx.transaction_id:
                new_waiting_ops.append(op)
        self.waiting_ops = new_waiting_ops
        
        self.handle_unlock(trx.transaction_id)
