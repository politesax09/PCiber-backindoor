
import datetime
import time
from backdoor import Backdoor, get_saved_backdoors
from msf import Msf

# DONE: 1. Implementar dos colas de mensajes y reestructurar libreria de mensajes para ello:
# menu ---> monitor, monitor ---> menu
# TODO: 2. Implementar acciones de MENU por paso de mensajes y que las ejecute MONITOR:
#   > Parseador de json (como vienen backdoors en los mensajes) a clase backdoor
# TODO: 3. Revisar implementacion tecnica SSH
# TODO: 4. Implementar tecnica 2
# TODO: 5. Implementar tecnica 3
# TODO: 6. Implementar tecnica 4
# TODO: 7. Implementar acciones de monitorizacion: list, select, restart, delete, edit

class Menu:
    def __init__(self, msg_q_menu, msg_q_mon, msg_count, backdoor, msf) -> None:
        self.msg_q_menu = msg_q_menu
        self.msg_q_mon = msg_q_mon
        self.msg_last_id = msg_count
        self.msg_last = None
        self.backdoor = backdoor
        # self.backdoor_list = get_saved_backdoors()
        self.backdoor_list = None
        self.msf = msf

        # Esperar inicio de Monitor
        if self.wait_msg('monitor', 'monitor'):
            if self.msg_last['msg'] == 'start':
                print('-- COOL: MONITOR inciado correctamente')
                self.put_msg_q('menu', 'menu', 'ok')
                self.menu()
            else: print('-- HOT: Fallo al iniciar MONITOR. Saliendo de BackInDoor')


    # def get_msg_q(self):
    #     if not self.msg_q.empty():
    #         self.msg_q.get()


    def put_msg_q(self, type, subject, msg):
        if subject and type and msg:
            # msg.append(datetime.datetime.now())
            self.msg_last_id += 1
            self.msg_q_mon.put({
                "id": self.msg_last_id,
                "type": type,
                "subject": subject,
                "msg": msg
            })


    def wait_msg(self, type, subject):
        m = None
        while not m:
            if not self.msg_q_menu.empty():
                m = self.msg_q_menu.get()
                if m['id'] > self.msg_last_id and m['type'] == type and m['subject'] == subject:
                    self.msg_last_id = m['id']
                    self.msg_last = m
                    return True
                else:
                    print(f'-- HOT: MENU: Error en mensaje: {m}')
                    return False


    def menu(self):
        while (True):
            print('\n\nBienvenido a B4ckInD00r\n\
        Opnciones: \n \
        \t> deploy\t[[Despliega una nueva backdoor]]\n \
        \t> monitor\t[[Estado de las backdoors]]\n\
        \t> select <backdoor_name>\t[[Selecciona una backdoor activa]]\n\
        \t> utils\t[[Ejecuta utilidades complementarias]]\n\
        \t> modules\t[[Usa un modulo MSF]]\n\
        \t> exit\t[[Salir]]\n')
            op = input('>>>   ').strip().lower()
            ops = []
            if (' ' in op):
                delim = op.index(' ')
                ops.append(op[:delim].strip())
                ops.append(op[delim+1:].strip())
            else:
                ops.append(op)


            if (ops[0] == 'exit'):
                break

            ##################  DEPLOY  ##################

            elif (ops[0] == 'deploy'):
                print('\nDesplegar nueva backdoor\n')
                name = input('Ponle nombre >>>   ').strip().lower()

                self.backdoor.name = name
                self.backdoor.status = 'created'

                while (True):
                    print('\nOpciones:\n\
                > msf_ssh_key   [[Inyecta claves SSH en la victima]]\n\
                > bashrc     [[Inyecta shell en .bashrc]]\n\
                > back  [[Atras]]\n')

                    op = input('[deploy]>>>   ').strip().lower()

                    ops.clear()
                    if (' ' in op):
                        delim = op.index(' ')
                        ops.append(op[:delim].strip())
                        ops.append(op[delim+1:].strip())
                    else:
                        ops.append(op)
                    
                    if (ops[0] == 'msf_ssh_key'):
                        print('\nDesplegando backdoor...\n')
                        self.backdoor.type = 'msf_ssh_key'
                        self.backdoor.attacker_ip = '127.0.0.1'
                        self.backdoor.shell = 'ncshell'
                        session_id = self.msf.msf_ssh_key()
                        if session_id:
                            session = self.msf.get_session(session_id)
                            self.backdoor.target_ip = session['target_host']
                            self.backdoor.status = 'active'
                        else:
                            self.backdoor.status = 'innactive'
                        self.backdoor.save_backdoor()

                    elif (ops[0] == 'bashrc'):
                        self.backdoor.type = 'bashrc'
                        self.backdoor.attacker_ip = '127.0.0.1'
                        self.backdoor.shell = 'ncshell'
                        session_id = self.msf.msf_bashrc()
                        if session_id:
                            session = self.msf.get_session(session_id)
                            self.backdoor.target_ip = session['target_host']
                            self.backdoor.status = 'active'
                        else:
                            self.backdoor.status = 'innactive'
                        self.backdoor.save_backdoor()

                    elif (ops[0] == 'back'):
                        break

                    else: print('-- HOT: La opcion no existe')
                    

            ##################  MONITOR  ##################

            elif (ops[0] == 'monitor'):
                self.put_msg_q('menu', 'monitor','run')
                # time.sleep(1)
                if self.wait_msg('monitor', 'monitor'):
                    if self.msg_last['msg'] == 'ok':
                        print('MENU: recibido ok')
                        if self.wait_msg('status', 'backdoor'):
                            print('MENU... ', self.msg_last['msg'])
                            self.put_msg_q('status', 'backdoor', 'ok')
                    # for b in self.backdoor_list:
                    #     mon_res = self.wait_msg()
                    #     if mon_res != None:
                    #         if mon_res['type'] == 'entrie' and mon_res['backdoor'] == b.name:
                    #             if mon_res['msg'][0] == 'status_up':
                    #                 b.status = 'active'
                    #             elif mon_res['msg'][0] == 'status_down':
                    #                 b.status = 'innactive'
                    #             self.put_msg_q('monitor', 'menu', ['run'])
                        
                # print('Backdoors activas:\n')
                # for bdoor in self.backdoor_list:
                #     bdoor.print_backdoorclass()
                #     print()
                # print('Sesiones activas:\n')
                # print(self.msf.get_sessions())

                while True:
                    print('\nOpciones:\n\
                > list   [[Lista las backdoors guardadas]]\n\
                > select <nombre backdoor>    [[Selecciona una backdoor]]\n\
                > restart <nombre backdoor>     [[Ejecutar de nuevo]]\n\
                > edit <nombre backdoor>        [[Editar una backdoor]]\n\
                > delete <nombre backdoor>      [[Eliminar una backdoor]]\n\
                > back  [[Atras]]\n')

                    op = input('[monitor]>>>   ').strip().lower()
                    ops.clear()
                    if (' ' in op):
                        delim = op.index(' ')
                        ops.append(op[:delim].strip())
                        ops.append(op[delim+1:].strip())
                    else:
                        ops.append(op)

                    if ops[0] == 'list':
                        print('Backdoors activas:\n')
                        self.backdoor_list = get_saved_backdoors()
                        for bdoor in self.backdoor_list:
                            bdoor.print_backdoorclass_simple()
                            print('------------------')
                        print('Sesiones activas:\n')
                        print(self.msf.get_sessions())
                    
                    if (ops[0] == 'select'):
                        if (len(ops) > 1):
                            self.backdoor_list = get_saved_backdoors()
                            for bdoor in self.backdoor_list:
                                if (ops[1] == bdoor.name):
                                    self.backdoor = bdoor
                                    break
                            if self.backdoor.name != None:
                                self.put_msg_q('action', 'backdoor', ['select', self.backdoor.name])
                                if self.wait_msg('action', 'monitor'):
                                    if self.msg_last['msg'][0] == 'ok':
                                        print('COOL: Seleccionada ' + self.backdoor.name)
                                        self.backdoor.print_backdoorclass()
                                        print()
                                    else: print('HOT: Error al seleccionar ' + self.backdoor.name)
                            else: print('-- HOT: La backdoor seleccionada no existe\n')
                        else: print('-- HOT: Debes seleccionar una backdoor disponible\n')

                    if ops[0] == 'restart':
                        if len(ops) > 1:
                            for bdoor in self.backdoor_list:
                                if ops[1] == bdoor.name:
                                    self.backdoor = bdoor
                                    break
                            if self.backdoor.name != None:
                                print('COOL: Reiniciando ' + self.backdoor.name)
                                # Enviar mensaje para que monitor la reinicie
                                self.put_msg_q(self.backdoor.name, 'action', ['restart', datetime.datetime.now()])
                            else:
                                print('-- HOT: La backdoor seleccionada no existe\n')
                        else: print('-- HOT: Debes seleccionar una backdoor disponible\n')
                    
                    if ops[0] == 'delete':
                        if len(ops) > 1:
                            for bdoor in self.backdoor_list:
                                if ops[1] == bdoor.name:
                                    self.backdoor = bdoor
                                    break
                            if self.backdoor.name != None:
                                self.backdoor.rm_backdoor()
                                print(f'COOL: {self.backdoor.name} eliminada\n')
                            else:
                                print('-- HOT: La backdoor seleccionada no existe\n')
                        else: print('-- HOT: Debes seleccionar una backdoor disponible\n')


            ##################  UTILIS  ##################

            elif ops[0] == 'utils':
                while (True):
                    print('Utilidades complementarias')
                    print('\nOpciones:\n\
                    > enum_users\n\
                    > back  [[Atras]]\n')
                    op = input('>>>   ').strip().lower()

                    ops.clear()
                    if (' ' in op):
                        delim = op.index(' ')
                        ops.append(op[:delim].strip())
                        ops.append(op[delim+1:].strip())
                    else:
                        ops.append(op)
                        
                    if ops[0] == 'enum_users':
                        self.msf.enum_users()
            

            ##################  MODULES  ##################

            elif (ops[0] == 'modules'):
                print('Desplegar modulos de MSF\n')
                name = input('Ponle nombre a la backdoor para guardar los datos >>>   ').strip().lower()

                self.backdoor.name = name
                self.backdoor.status = 'created'

                while (True):
                    print('\nOpciones:\n\
                > select <module_name || module_num>  [[Selecciona un modulo]]\n\
                > config    [[Configura el modulo seleccionado]]\n\
                > list  [[Lista los modulos disponibles]]\n\
                > back  [[Atras]]\n')
                    op = input('>>>   ').strip().lower()
                    ops.clear()
                    if (' ' in op):
                        delim = op.index(' ')
                        ops.append(op[:delim].strip())
                        ops.append(op[delim+1:].strip())
                    else:
                        ops.append(op)

                    if (ops[0] == 'select'):
                        modules_list = self.msf.get_modules()

                        if (len(ops) > 1):
                            if (len(ops[1]) < 4):
                                if (int(ops[1]) < len(modules_list)):
                                    self.backdoor.modules.append({'id': 'post/' + modules_list[int(ops[1])], 'tool': 'msf'})
                                    print('Seleccionado modulo ' + modules_list[int(ops[1])])
                                else:
                                    print('-- HOT: El numero del modulo seleccionado no es correcto')
                            else:
                                if (ops[1] in modules_list):
                                    self.backdoor.modules.append({'id': 'post/' + ops[1], 'tool': 'msf'})
                                    print('Seleccionado modulo ' + ops[1])
                                else:
                                    print('-- HOT: El modulo seleccionado no es correcto')
                        else:
                            print('-- HOT: Se debe indicar el modulo seleccionado')
                        
                        # TODO: DECIDIR Se puede escribir backdoor en DB en este punto aunque no este rellena
                        

                    elif (ops[0] == 'config'):
                        print('Configuracion de ' + str(self.backdoor.name) + ':')

                        if (len(self.backdoor.modules) > 0):
                            module = self.msf.select_module(self.backdoor.modules[0]['id'])
                            config_missing = self.msf.get_missing_required(module)
                            for item in config_missing:
                                if (item == 'SESSION'):
                                    print(item)
                        else: print('-- HOT: No hay modulos seleccionados')


                        # op_target_ip = input('target_ip [' + str(self.backdoor.target_ip) + '] -> ')
                        # op_attacker_ip = input('attacker_ip [' + str(self.backdoor.attacker_ip) + '] -> ')
                        # op_payload_url = input('target_ip [' + str(self.backdoor.payload_url) + '] -> ')

                        # if (op_target_ip == ''):
                        #     self.backdoor.target_ip = None
                        # else: self.backdoor.target_ip = op_target_ip
                        # if (op_attacker_ip == ''):
                        #     self.backdoor.attacker_ip = '127.0.0.1'
                        # else: self.backdoor.attacker_ip = op_attacker_ip
                        # if (op_payload_url == ''):
                        #     self.backdoor.payload_url = None
                        # else: self.backdoor.payload_url = op_payload_url
                            

                    elif (ops[0] == 'list'):
                        modules_list = self.msf.get_modules()
                        i = 0
                        for module in modules_list:
                            i += 1
                            print(i, ' -> ', module)
                    # elif (ops[0] == 'run'):


                    elif (ops[0] == 'back'):
                        break

                    else: print('-- HOT: El comando no existe')






            

    