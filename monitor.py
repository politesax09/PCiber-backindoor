import asyncio
import datetime
import subprocess
from db import *
from backdoor import get_saved_backdoors

        # TODO: AL ARRANCAR LA HERRAMIENTA COMPROBAR SI HAY SESIONES ACTIVAS
        #       Y GUARDADAS EN LAS CORRESPONDIENTES BACKDOORS
class Monitor:

    def __init__(self, msg_q, msg_count, backdoor, msf) -> None:
        self.backdoor_list = get_saved_backdoors()
        self.backdoor_list.append(backdoor)
        self.msf = msf
        self.msg_q = msg_q
        self.msg_count = msg_count
        # MONITOR indica que se ha iniciado correctamente
        self.put_msg_q('monitor', 'monitor', ['start'])
        while True:
            last_msg = self.wait_msg()
            if last_msg != None:
                # MONITOR hace comprobacion backdoors cuando MENU se lo pide
                if last_msg['type'] == 'menu' and last_msg['backdoor'] == 'monitor' and \
                        last_msg['msg'][0] == 'run':
                    self.run_monitor()
                else: print('-- HOT: Mensaje inesperado de MENU a MONITOR')
        # self.run_monitor()



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

    def get_msg_q(self):
        if not self.msg_q.empty():
            return self.msg_q.get()
        else: return None
        
    def put_msg_q(self, bdoor_name, type, msg):
        if bdoor_name and type and msg:
            msg.append(datetime.datetime.now())
            self.msg_count += 1
            self.msg_q.put({
                "id": self.msg_count,
                "type": type,
                "backdoor": bdoor_name,
                "msg": msg
            })

    def wait_msg(self):
        msg = None
        while not msg:
            if not self.msg_q.empty():
                msg = self.msg_q.get()
        return msg


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

    


