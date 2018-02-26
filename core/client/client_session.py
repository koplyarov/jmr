from ..joint_adapters import *
from ..operation import MapOperation
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
        return self._joint_module.CreateComponent(jmr_IRow, Row, {})

    def CreateTable(self, path):
        return self._joint_module.CreateComponent(jmr_IRowWriter, RowWriter, self._storage.create_table(path))

    def ReadTable(self, path):
        return self._joint_module.CreateComponent(jmr_IRowReader, RowReader, self._joint_module, self._storage.get_table(path))

    def RunMap(self, config, mapper):
        mapper.Process(self.ReadTable(config.InputTable), self.CreateTable(config.OutputTable))
        return self._joint_module.CreateComponent(jmr_IOperation, MapOperation)
