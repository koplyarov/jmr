from itertools import groupby
import json

from ..fs import Directory
from ..joint_adapters import *
from ..operation import MapOperation, MapReduceOperation
from ..storage import MemoryStorage
from ..tables import Row, RowReader, RowWriter


class ClientSession(jmr_IClientSession):
    def __init__(self, joint_module):
        super(ClientSession, self).__init__()
        self._module = joint_module
        self._storage = MemoryStorage()

    def GetVersionString(self):
        return 'JMR Client python prototype'

    def GetFsRoot(self):
        return self._module.CreateComponent(jmr_fs_IDirectory, Directory, self._module, '', self._storage.get_root_dir())

    def CreateRow(self):
        return self._module.CreateComponent(jmr_io_IRow, Row)

    def CreateTable(self, path):
        return self._module.CreateComponent(jmr_io_IRowWriter, RowWriter, self._storage.create_table(path))

    def ReadTable(self, path):
        return self._module.CreateComponent(jmr_io_IRowReader, RowReader, self._module, self._storage.get_table(path))

    def RunMap(self, config, mapper):
        mapper.Process(self.ReadTable(config.InputTable), self.CreateTable(config.OutputTable))
        return self._module.CreateComponent(jmr_operations_IOperation, MapOperation)

    def RunMapReduce(self, config, mapper, reducer):
        intermediate_rows = []
        mapper_out = self._module.CreateComponent(jmr_io_IRowWriter, RowWriter, intermediate_rows)
        mapper.Process(self.ReadTable(config.InputTable), mapper_out)

        def group_func(row_json):
            return json.loads(row_json)[config.ReduceBy]

        output_writer = self.CreateTable(config.OutputTable)
        for key, rows in groupby(sorted(intermediate_rows, key=group_func), key=group_func):
            reducer_in = self._module.CreateComponent(jmr_io_IRowReader, RowReader, self._module, list(rows))
            reducer.Process(key, reducer_in, output_writer)

        return self._module.CreateComponent(jmr_operations_IOperation, MapReduceOperation)
