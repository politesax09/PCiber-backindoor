import asyncio
import datetime
import time
import subprocess
from db import *
from backdoor import get_saved_backdoors

# TODO: AL ARRANCAR LA HERRAMIENTA COMPROBAR SI HAY SESIONES ACTIVAS
#       Y GUARDADAS EN LAS CORRESPONDIENTES BACKDOORS
class Monitor:

    def __init__(self, msg_q_menu, msg_q_mon, msg_count, backdoor, msf) -> None:
        self.backdoor_list = get_saved_backdoors()
        self.backdoor_list.append(backdoor)
        self.backdoor_selected = None
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
                                    self.refresh_backdoor_list()
                                    # REFRESCAR SESIONES
                                    # ENVIAR INFO A MENU
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


    def refresh_backdoor_list(self):
        self.backdoor_list = get_saved_backdoors()

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
    


