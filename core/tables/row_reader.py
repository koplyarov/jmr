from ..joint_adapters import *
from .row import Row


class RowReader(jmr_IRowReader):
    def __init__(self, joint_module, table):
        super(RowReader, self).__init__()
        self._joint_module = joint_module
        self._table_iterator = iter(table)

    def ReadRow(self):
        try:
            row_dict = next(self._table_iterator)
            return self._joint_module.CreateComponent(jmr_IRow, Row, row_dict)
        except StopIteration:
            return None
