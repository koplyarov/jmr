from ..joint_adapters import *


class Table(jmr_fs_ITable):
    def __init__(self, name):
        self._name = name

    def GetName(self):
        return self._name
