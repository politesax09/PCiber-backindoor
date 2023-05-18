from pymetasploit3.msfrpc import *


# client = MsfRpcClient('backindoor', port=55553, ssl=True)

try:
    client = MsfRpcClient('backindoor', port=55552, ssl=False)
    # print(client.sessions.list)
    module = client.modules.use('post', 'linux/manage/sshkey_persistence')
    

except:
    print('-- ERROR: No hay servidor RPC activo')

