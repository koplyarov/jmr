from .joint_adapters import *
from .client import ClientSession


def MakeClientSession(joint_module):
    return joint_module.CreateComponent(joint_IObject, ClientSession, joint_module)
