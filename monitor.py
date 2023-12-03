import asyncio
import datetime
import time
import subprocess
from db import *
from backdoor import *

# TODO: AL ARRANCAR LA HERRAMIENTA COMPROBAR SI HAY SESIONES ACTIVAS
#       Y GUARDADAS EN LAS CORRESPONDIENTES BACKDOORS
class Monitor:

    def __init__(self, msg_q_menu, msg_q_mon, msg_count, backdoor, msf) -> None:
        self.backdoor_list = get_saved_backdoors()
        # self.backdoor_list.append(backdoor)
        self.new_backdoor_list = get_saved_backdoors()
        self.backdoor_selected = None
        self.session_list = None
        self.msf = msf
        self.msg_q_menu = msg_q_menu
        self.msg_q_mon = msg_q_mon
        self.msg_last_id = msg_count
        self.msg_last = None
        
        # MONITOR indica que se ha iniciado correctamente
        self.put_msg_q('monitor', 'monitor', 'start')
        # time.sleep(1)
        if self.wait_msg('menu','menu'):
            if self.msg_last['msg'] == 'ok':
                # Esperando a que menu mande mensaje RUN
                while True:
                    if self.wait_msg('menu', 'monitor'):
                        # MONITOR hace comprobacion backdoors cuando MENU se lo pide
                        if self.msg_last['msg'] == 'run':
                            # self.run_monitor()
                            self.put_msg_q('monitor', 'monitor', 'ok')
                            
                            # Ejemplo mensaje de status de backdoors
                            self.put_msg_q('status', 'backdoor', self.backdoor_to_msg())
                            self.wait_msg('status', 'backdoor')
                            if self.msg_last['msg'] != 'ok': print('-- HOT: MONITOR: Mensaje inesperado de MENU')

                            # RECIBIR OPCION DE MENU
                            if self.wait_msg('action', 'backdoor'):
                                if self.msg_last['msg'][0] == 'list':
                                    # Actualizar backdoors
                                    self.refresh_backdoor_list()
                                    # print('MON... ',self.backdoor_list)
                                    self.put_msg_q('status', 'backdoor', self.backdoor_to_msg())
                                    self.wait_msg('status', 'backdoor')
                                    # Actualizar sesiones activas
                                    # self.refresh_session_list()
                                    # print(self.session_list)
                                    
                                if self.msg_last['msg'][0] == 'select':
                                    if self.select_backdoor(self.msg_last['msg'][1]):
                                        self.put_msg_q('action', 'monitor', ['ok'])
                                    else: self.put_msg_q('action', 'monitor', ['error'])

                                if self.msg_last['msg'][0] == 'restart':
                                    pass

                                if self.msg_last['msg'][0] == 'edit':
                                    pass

                                if self.msg_last['msg'][0] == 'delete':
                                    pass

                        # else: print('MONITOR: ',self.msg_last_id)
        # self.run_monitor()

    # def wait_for_run(self):


    # Comprobacion para las persistencias via SSH
    # Devuelve 0 si tiene exito y 1 si falla
    def check_ssh_conn(self, rhost, rport):
        res = subprocess.run(f'timeout 5 bash -c "</dev/tcp/{rhost}/{rport}"', shell=True, capture_output=True, text=True)
        return res.returncode    

    def run_monitor(self):
        # Comprobar estado de cada backdoor de la lista y manda un mensaje con su estado
        # Cuando no ha cambiado de estado msg contiene '-'
        for bdoor in self.backdoor_list:
            if bdoor.type in ('msf_ssh_key', 'msf_bashrc'):
                if self.check_ssh_conn(bdoor.target_ip, 22):
                    if bdoor.status == 'innactive':
                        self.put_msg_q(bdoor.name, 'entrie', ['status_up'])
                    else: self.put_msg_q(bdoor.name, 'entrie', ['-'])
                    bdoor.status = 'active'
                else:
                    if bdoor.status == 'active':
                        self.put_msg_q(bdoor.name, 'entrie', ['status_down'])
                    else: self.put_msg_q(bdoor.name, 'entrie', ['-'])
                    bdoor.status = 'innactive'
            last_msg = self.wait_msg()
            if last_msg == None or last_msg['type'] != 'menu':
                break

    # def get_msg_q(self):
    #     if not self.msg_q.empty():
    #         return self.msg_q.get()
    #     else: return None
        
    def put_msg_q(self, type, subject, msg):
        if subject and type and msg:
            # msg.append(datetime.datetime.now())
            self.msg_last_id += 1
            self.msg_q_menu.put({
                "id": self.msg_last_id,
                "type": type,
                "subject": subject,
                "msg": msg
            })


    def wait_msg(self, type, subject):
        m = None
        while not m:
            if not self.msg_q_mon.empty():
                m = self.msg_q_mon.get()
                if m['id'] > self.msg_last_id and m['type'] == type and m['subject'] == subject:
                    self.msg_last_id = m['id']
                    self.msg_last = m
                    return True
                else:
                    print(f'-- HOT: MONITOR: Error en mensaje: {m}')
                    return False

    def backdoor_to_msg(self):
        msg = []
        # print('MON backdoor list... ',self.backdoor_list[0].print_backdoorclass_simple())
        # print(f'MON new backdoor list... {self.new_backdoor_list[0].print_backdoorclass_simple()}')

        for bdoor in self.backdoor_list:
            msg.append({'name':bdoor.name})
            msg[-1]['type'] = bdoor.type
            msg[-1]['target_ip'] = bdoor.target_ip
            msg[-1]['target_url'] = bdoor.target_url
            msg[-1]['attacker_ip'] = bdoor.attacker_ip
            msg[-1]['attacker_url'] = bdoor.attacker_url
            msg[-1]['shell'] = bdoor.shell
            msg[-1]['status'] = bdoor.status
            msg[-1]['error'] = bdoor.error
            msg[-1]['entries'] = bdoor.entries

        return msg
            
    def msg_to_backdoor(self):
        b_list = []

        for b in self.msg_last['msg']:
            b_list.append(Backdoor(b['name']))

        for b1, b2 in zip(b_list, self.msg_last['msg']):
            if b1.type != b2['type']:
                b1.type = b2['type']
            if b1.target_ip != b2['target_ip']:
                b1.target_ip = b2['target_ip']
            if b1.target_url != b2['target_url']:
                b1.target_url = b2['target_url']
            if b1.attacker_ip != b2['attacker_ip']:
                b1.attacker_ip = b2['attacker_ip']
            if b1.attacker_url != b2['attacker_url']:
                b1.attacker_url = b2['attacker_url']
            if b1.shell != b2['shell']:
                b1.shell = b2['shell']
            if b1.status != b2['status']:
                b1.status = b2['status']
            if b1.error != b1.error:
                b1.error = b2['error']
            for e1, e2 in zip(b1.entries, b2['entries']):
                if e1 != e2:
                    e1 = e2
        return b_list



    def refresh_session_list(self):
        self.session_list = self.get_msf_sessions()

    def get_msf_sessions(self):
        return self.msf.get_sessions()

    def is_msf_session_alive(self, session):
        if session in self.get_msf_sessions():
            return True
        else: return False

    def check_session_status(self):
        pass

    def alert_session_down(self, session):
        pass

    def relaunch_session(self):
        pass


    def refresh_new_backdoor_list(self):
        self.new_backdoor_list = get_saved_backdoors()

    def refresh_backdoor_list(self):
        self.backdoor_list = get_saved_backdoors()

    def select_backdoor(self, name):
        for bdoor in self.backdoor_list:
            if bdoor.name == name:
                self.backdoor_selected = bdoor
                return True
        return False

    def edit_backdoor(self):
        self.backdoor_selected = self.select_backdoor()

    def delete_backdoor(self):
        pass
    


