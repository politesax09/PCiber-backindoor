import threading
from time import sleep
import queue


def menu(q):
    while True:
        print('Menú principal')
        in1 = input('MENU: Escribe algo >>> ')
        if 'msg' in in1:
            q.put(in1)
            print('MENU: anadido nuevo mensaje en cola')
        elif in1 == 'q':
            break
        else: 
            print('MENU: ', in1)


def monitor(q):
    while True:
        print('Monitor')
        sleep(5)  # Simula una operación que toma 1 segundo
        if not q.empty():
            print('MONITOR: msg: ',  q.get())
        else: print('MONITOR: no hay mensajes')

# Crear cola de mensajes
msg_q = queue.Queue()

# Crear los hilos
t1 = threading.Thread(target=menu, args=(msg_q,))
t2 = threading.Thread(target=monitor, args=(msg_q,))

# Iniciar los hilos
t1.start()
t2.start()

# Esperar a que los hilos terminen
t1.join()
t2.join()

print("Programa finalizado.")
