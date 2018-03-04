from ..joint_adapters import *
from .table import Table

import pyjoint


jmr_fs_INode_typeDescriptor = pyjoint.TypeDescriptor((16, jmr_fs_INode_proxy, jmr_fs_INode.interfaceChecksum))


class Directory(jmr_fs_IDirectory):
    def __init__(self, module, name, dir_dict):
        self._module = module
        self._name = name
        self._dir_dict = dir_dict

    def GetName(self):
        return self._name

    def GetChildren(self):
        result = pyjoint.Array(jmr_fs_INode_typeDescriptor, len(self._dir_dict))
        for i, name in enumerate(self._dir_dict):
            entry = self._dir_dict[name]
            if isinstance(entry, list):
                result[i] = self._module.CreateComponent(jmr_fs_INode, Table, name)
            elif isinstance(entry, dict):
                result[i] = self._module.CreateComponent(jmr_fs_INode, Directory, self._module, name, entry)
            else:
                raise RuntimeError('Unknown directory entry type: {}'.format(type(entry)))
        return result
