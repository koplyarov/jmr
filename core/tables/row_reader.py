from ..joint_adapters import *
from .row import Row


class RowReader(jmr_io_IRowReader):
    def __init__(self, joint_module, table):
        super(RowReader, self).__init__()
        self._joint_module = joint_module
        self._table_iterator = iter(table)

    def ReadRow(self):
        try:
            row_json_str = next(self._table_iterator)
            row = self._joint_module.CreateComponent(jmr_io_IRow, Row)
            row.DeserializeFromJson(row_json_str)
            return row
        except StopIteration:
            return None
