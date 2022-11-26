# TODO: funciones
#   - get_modules()
#   - get_sessions()
#   - set_options()
#   - create_session() Se crea como salida de la ejecucion de modulos que generen meterpreter
#   - remove_session()
#   - _

# from db import *
from pymetasploit3.msfrpc import *


class Msf:

    def __init__(self) -> None:
        self.client = MsfRpcClient('backindoor', port=55553, ssl=True)
        

    def get_modules(self):
        return self.client.modules.post
        

    def select_module(self, name):
        return self.client.modules.use('post', name)
    

    def get_missing_required(self, module):
        return module.missing_required


    def config_module():
        pass

    def get_sessions():
        pass

    def create_session():
        pass

    def remove_session():
        pass



def get_modules(client, type):
    if type == 'post':
        client.modules.post
    elif type == 'multi':
        client.modules.multi
    elif type == 'auxiliary':
        client.modules.auxiliary
    elif type == 'payloads':
        client.modules.payloads
    elif type == 'nops':
        client.modules.nops
    elif type == 'encodeformats':
        client.modules.encodeformats
    elif type == 'encoders':
        client.modules.encoders
    elif type == 'evasion':
        client.modules.evasion
    elif type == 'platforms':
        client.modules.evasion





