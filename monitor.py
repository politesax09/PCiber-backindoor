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
                    # Da fallo porq MONITOR recibe su propio mensaje q han enviado de arranque,
                    # hay q comprobar el id SOLUCIONADO
                    if self.wait_msg('menu', 'monitor'):
                        # MONITOR hace comprobacion backdoors cuando MENU se lo pide
                        if self.msg_last['msg'] == 'run':
                            # self.run_monitor()
                            print('MONITOR RUN')
                            self.put_msg_q('monitor', 'monitor', 'ok')
                            
                            # Ejemplo mensaje de status de backdoors
                            self.put_msg_q('status', 'backdoor', [
                            {
                                "b1": {
                                    "status": "innactive",
                                    "entries": [
                                        {"status":"down"}
                                    ]
                                }
                            }
                            ,
                            {
                                "b2": {
                                    "entries":[
                                        {},
                                        {"status":"up"}
                                    ]
                                }
                            }])
                            # time.sleep(1)
                            self.wait_msg('status', 'backdoor')
                            if self.msg_last['msg'] == 'ok':
                                print('MONITOR STATUS OK')
                            else: print('-- HOT: MONITOR: Mensaje inesperado de MENU')

                            # RECIBIR OPCION DE MENU
                            if self.wait_msg('action', 'backdoor'):
                                if self.msg_last['msg'][0] == 'list':
                                    # Actualizar backdoors
                                    self.refresh_backdoor_list()
                                    print(self.backdoor_list)
                                    self.put_msg_q('status', 'backdoor', self.backdoor_to_msg())
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
        for bdoor in self.backdoor_list:
            for new_bdoor in self.new_backdoor_list:
                # msg.append({'name':new_bdoor.name})
                msg.append({new_bdoor.name:{}})
                if new_bdoor.type != bdoor.type:
                    msg[new_bdoor.name]['type'] = new_bdoor.type
                if new_bdoor.target_ip != bdoor.target_ip:
                    msg[new_bdoor.name]['target_ip'] = new_bdoor.target_ip
                if new_bdoor.target_url != bdoor.target_url:
                    msg[new_bdoor.name]['target_url'] = new_bdoor.target_url
                if new_bdoor.attacker_ip != bdoor.attacker_ip:
                    msg[new_bdoor.name]['attacker_ip'] = new_bdoor.attacker_ip
                if new_bdoor.attacker_url != bdoor.attacker_url:
                    msg[new_bdoor.name]['attacker_url'] = new_bdoor.attacker_url
                if new_bdoor.shell != bdoor.shell:
                    msg[new_bdoor.name]['shell'] = new_bdoor.shell
                if new_bdoor.status != bdoor.status:
                    msg[new_bdoor.name]['status'] = new_bdoor.status
                if new_bdoor.error != bdoor.error:
                    msg[new_bdoor.name]['error'] = new_bdoor.error
                msg[new_bdoor.name]['entries'] = []
                for e1 in bdoor.entries:
                    for e2 in new_bdoor.entries:
                        if e1 != e2:
                            msg[new_bdoor.name]['entries'] = e2
        return msg
            
    def msg_to_backdoor(self):
        b_list = []

        for bname in list(self.msg_last['msg'].keys()):
            b_list.append(Backdoor(bdoor['name']))
        for b1 in self.msg_last['msg']:
            for b2 in b_list:
                if b1.type != bdoor.type:
                    msg[new_bdoor.name]['type'] = b2.type
                if b1.target_ip != bdoor.target_ip:
                    msg[b2.name]['target_ip'] = b2.target_ip
                if b1.target_url != bdoor.target_url:
                    msg[b2.name]['target_url'] = b2.target_url
                if b1.attacker_ip != bdoor.attacker_ip:
                    msg[b2.name]['attacker_ip'] = b2.attacker_ip
                if b1.attacker_url != bdoor.attacker_url:
                    msg[b2.name]['attacker_url'] = b2.attacker_url
                if b1.shell != bdoor.shell:
                    msg[b2.name]['shell'] = b2.shell
                if b1.status != bdoor.status:
                    msg[b2.name]['status'] = b2.status
                if b1.error != bdoor.error:
                    msg[b2.name]['error'] = b2.error
                msg[b2.name]['entries'] = []
                for e1 in bdoor.entries:
                    for e2 in b2.entries:
                        if e1 != e2:
                            msg[b2.name]['entries'] = e2



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
    


