from itertools import groupby
import json

from ..joint_adapters import *
from ..operation import MapOperation, MapReduceOperation
from ..storage import MemoryStorage
from ..tables import Row, RowReader, RowWriter


class ClientSession(jmr_IClientSession):
    def __init__(self, joint_module):
        super(ClientSession, self).__init__()
        self._joint_module = joint_module
        self._storage = MemoryStorage()

    def GetVersionString(self):
        return 'JMR Client python prototype'

    def CreateRow(self):
        return self._joint_module.CreateComponent(jmr_IRow, Row)

    def CreateTable(self, path):
        return self._joint_module.CreateComponent(jmr_IRowWriter, RowWriter, self._storage.create_table(path))

    def ReadTable(self, path):
        return self._joint_module.CreateComponent(jmr_IRowReader, RowReader, self._joint_module, self._storage.get_table(path))

    def RunMap(self, config, mapper):
        mapper.Process(self.ReadTable(config.InputTable), self.CreateTable(config.OutputTable))
        return self._joint_module.CreateComponent(jmr_IOperation, MapOperation)

    def RunMapReduce(self, config, mapper, reducer):
        intermediate_rows = []
        mapper_out = self._joint_module.CreateComponent(jmr_IRowWriter, RowWriter, intermediate_rows)
        mapper.Process(self.ReadTable(config.InputTable), mapper_out)

        def group_func(row_json):
            return json.loads(row_json)[config.ReduceBy]

        output_writer = self.CreateTable(config.OutputTable)
        for key, rows in groupby(sorted(intermediate_rows, key=group_func), key=group_func):
            reducer_in = self._joint_module.CreateComponent(jmr_IRowReader, RowReader, self._joint_module, list(rows))
            reducer.Process(key, reducer_in, output_writer)

        return self._joint_module.CreateComponent(jmr_IOperation, MapReduceOperation)
