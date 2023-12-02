import threading
import queue
from menu import Menu

from monitor import Monitor
from msf import *
from backdoor import *


try:
    # OJO CON LA CONEXION EN Msf(), PUEDE FALLAR POR LOS PARAMETROS
    msf = Msf()
    print('\n-- COOL: Servicio MSF RPC conectado')
except:
    msf = None
    print('-- HOT: No hay servicio MSF RCP activo')

backdoor = Backdoor(None)
# Crear cola de mensajes
msg_q_menu = queue.Queue()
msg_q_mon = queue.Queue()
msg_count = 0

# Crear los hilos
t1 = threading.Thread(target=Menu, args=(msg_q_menu, msg_q_mon, msg_count, backdoor, msf,))
t2 = threading.Thread(target=Monitor, args=(msg_q_menu, msg_q_mon, msg_count, backdoor, msf,))

# Iniciar los hilos
t1.start()
t2.start()

# Esperar a que los hilos terminen
t1.join()
t2.join()
