from .joint_adapters import *
from .client import Client


def MakeClient(joint_module):
    return joint_module.CreateComponent(joint_IObject, Client, joint_module)
