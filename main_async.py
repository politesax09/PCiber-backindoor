import asyncio

async def menu_async():
    pass

async def monitor_async():
    pass

async def main():
    # Creamos una lista de tareas
    task_list = [menu_async(), monitor_async()]

    # Ejecutamos las tareas de forma concurrente
    await asyncio.gather(*task_list)

# Ejecutamos el bucle de eventos
asyncio.run(main())