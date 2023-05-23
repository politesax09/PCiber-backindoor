import asyncio

msg_list = asyncio.Queue()

async def tarea1():
    print('Tarea 1 iniciada')
    await msg_list.put({'msg':'Mensage de prueba'})
    await asyncio.sleep(2)  # Simula una operación que toma 2 segundos
    print('Tarea 1 completada')

async def tarea2():
    print('Tarea 2 iniciada')
    # await tarea1()
    while True:
        if not msg_list.empty():
            print(await msg_list.get())
        else:
            break
    await asyncio.sleep(5)  # Simula una operación que toma 3 segundos
    print('Tarea 2 completada')

async def tarea3():
    print('Tarea 3 iniciada')
    await msg_list.put({'msg':'Mensage de prueba'})
    await asyncio.sleep(1)  # Simula una operación que toma 1 segundo
    print('Tarea 3 completada')

async def main():
    # Creamos una lista de tareas
    tareas = [tarea1(), tarea2(), tarea3()]

    # Ejecutamos las tareas de forma concurrente
    await asyncio.gather(*tareas)

# Ejecutamos el bucle de eventos
asyncio.run(main())
