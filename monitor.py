# TODO: funciones
#   - get_sessions()
#   - is_session_alive()
#   - pull_msg_q()
#   - push_msg_q()
#   - 


# TODO: METODO PARA COMPROBAR ESTADO DE LAS BACKDOORS

import asyncio
from db import *


class Monitor:

    def __init__(self, msf) -> None:
        # TODO: COMPROBAR SI PASAR BACKDOOR_LIST POR PARAMETRO O COJER DE BD Y COMPROBAR
        self.backdoor_list = read_backdoors()['backdoors']
        self.msf = msf

    def monitor_menu():
        pass

    async def get_msg_q(self):
        global msg_q
        if not msg_q.empty():
            await msg_q.get()
        
    def put_msg_q(self, type, msg):
        pass

    def get_msf_sessions(self):
        pass

    def is_msf_session_alive(self):
        pass

    def check_session_status(self):
        pass

    def alert_session_down(self):
        pass

    def relaunch_session(self):
        pass

    


