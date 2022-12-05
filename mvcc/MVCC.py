from FileHandler import FileHandler
from module import *

class MVCC:
    def __init__(self, file_handler: FileHandler):
        self.file_handler = file_handler
        self.items: list[Item] = []
        self.transactions: list[Transaction] = []
        self.operations: list[Operation] = []
        self.queue: list[int] = []
        self.version_control = VersionControl()
        self.local_ts = 0
        self.aborted_trx_ids: list[int] = []

    def run(self):
        while True:
            str = self.file_handler.next_line()
            if str == '':
                break
            self.operations.append(Operation(str))

        for op in self.operations:
            self.prepare_item(op)

        print(self.version_control)
        for op in self.operations:
            self.prepare(op)
            self.run_operation(op)

    def find_transaction(self, trx_id: int):
        for trx in self.transactions:
            if trx.transaction_id == trx_id:
                return trx
        return None

    def prepare_item(self, op: Operation):
        if (op.operation != Command.COMMIT.value and op.item.label not in
                self.version_control.map):
            new_item = Item(op.item.label)
            self.version_control.add_new_version(new_item)

    def prepare(self, op: Operation):
        trx = self.find_transaction(op.transaction_id)
        if trx is None:
            new_trx = Transaction(op.transaction_id, op.transaction_id)
            new_trx.arr_process.append(op)
            self.transactions.append(new_trx)
            self.local_ts += 1
        else:
            trx.arr_process.append(op)

    def process(self, op: Operation):
        success = False
        if (op.operation == Command.READ.value):
            success = self.process_read(op)
        elif (op.operation == Command.WRITE.value):
            success = self.process_write(op)
        elif (op.operation == Command.COMMIT.value):
            success = self.process_commit(op)

        print(f"{op.format()}: {'success' if success else 'failed'}")
        return success

    def process_read(self, op: Operation):
        versions = self.version_control.get(op.item.label)
        op_ts = self.find_transaction(op.transaction_id).ts
        for version in reversed(versions):
            if version.read_ts < op_ts:
                print(f"Read {op.item.label} version: {version}")
                version.read_ts = op_ts
                print(f"Change read_ts to {op_ts} -> {version}")

                version.subscriber_ids.append(op.transaction_id)
                break
        return True

    def process_write(self, op: Operation):
        versions = self.version_control.get(op.item.label)
        op_ts = self.find_transaction(op.transaction_id).ts
        for version in reversed(versions):
            if (op_ts < version.read_ts):
                continue

            if (op_ts == version.write_ts):
                print(
                    f"Written by same timestamp: transaction {op.transaction_id} -> overwrite value")
                return True

            new_version = Item(op.item.label, version=op_ts,
                               read_ts=op_ts, write_ts=op_ts)
            new_version.subscriber_ids.append(op.transaction_id)
            self.version_control.add_new_version(new_version)
            self.find_transaction(
                op.transaction_id).created_items.append(new_version)

            print(
                f"Write {op.item.label} -> create new version: {new_version}")

            return True

        return False

    def process_commit(self, _: Operation):
        return True

    def handle_abort(self, trx_id: int) -> list[int]:
        print(f'Abort T{trx_id}')
        trx = self.find_transaction(trx_id)
        aborted: list[int] = [trx_id]

        for item in trx.created_items:
            versions = self.version_control.get(item.label)
            versions.remove(item)

            for id in item.subscriber_ids:
                if id == trx_id:
                    continue

                cur_aborted = self.handle_abort(id)
                new_aborted = []
                for id in cur_aborted:
                    if id not in aborted:
                        new_aborted.append(id)
                aborted.extend(new_aborted)

        return aborted

    def run_operation(self, op: Operation):
        print("=======================================")
        print("Current version control:")
        print(self.version_control)

        print(f"Run operation: {op.format()}")
        success = self.process(op)
        if success:
            return

        aborted_ids = self.handle_abort(op.transaction_id)
        for id in aborted_ids:
            self.local_ts += 1

            trx = self.find_transaction(id)
            trx.ts = self.local_ts
            trx.created_items = []

            for op in trx.arr_process:
                self.run_operation(op)
