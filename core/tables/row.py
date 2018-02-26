import json

from ..joint_adapters import *


class Row(jmr_IRow):
    def __init__(self):
        super(Row, self).__init__()
        self._row_dict = {}

    def GetI32Field(self, column):
        return self._row_dict[column]

    def GetStringField(self, column):
        return self._row_dict[column]

    def SetI32Field(self, column, value):
        self._row_dict[column] = value

    def SetStringField(self, column, value):
        self._row_dict[column] = value

    def SerializeToJson(self):
        return json.dumps(self._row_dict, sort_keys=True)

    def DeserializeFromJson(self, jsonString):
        self._row_dict = json.loads(jsonString)
