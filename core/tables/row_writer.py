from ..joint_adapters import *
from .row import Row


class RowWriter(jmr_IRowWriter):
    def __init__(self, table):
        super(RowWriter, self).__init__()
        self._table = table

    def WriteRow(self, row):
        self._table.append(row.SerializeToJson())
