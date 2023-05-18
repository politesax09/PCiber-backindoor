import asyncio

async def tarea1():
    print('Tarea 1 iniciada')
    await asyncio.sleep(2)  # Simula una operación que toma 2 segundos
    print('Tarea 1 completada')

async def tarea2():
    print('Tarea 2 iniciada')
    await asyncio.sleep(3)  # Simula una operación que toma 3 segundos
    print('Tarea 2 completada')

async def tarea3():
    print('Tarea 3 iniciada')
    await asyncio.sleep(1)  # Simula una operación que toma 1 segundo
    print('Tarea 3 completada')

async def main():
    # Creamos una lista de tareas
    tareas = [tarea1(), tarea2(), tarea3()]

    # Ejecutamos las tareas de forma concurrente
    await asyncio.gather(*tareas)

# Ejecutamos el bucle de eventos
asyncio.run(main())
