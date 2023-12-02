# TODO: primero con msf
#   - use_module()
#   - config_module()
#   - exe_module()
#   - read_console()
#


import subprocess
from db import *

class Backdoor:
    def __init__(self, name):
        self.name = name
        self.type = None
        self.target_ip = None
        self.target_url = None
        self.attacker_ip = None
        self.attacker_url = None
        self.payload_url = None
        self.entries = []
        self.modules = []
        self.shell = None
        self.status = None
        self.error = []


    def get_module(self, id):
        self.modules.append(search_module(id)['id'])
    

    def get_modules(self):
        modules = read_modules()
        for module in modules:
            self.modules.append(module['id'])

    
    def get_backdoor(self):
        backdoor = search_backdoor(self.name)
        if backdoor['type']: self.type = backdoor['type']
        else: self.type = None
        if backdoor['target_ip']: self.target_ip = backdoor['target_ip']
        else: self.target_ip = None        
        if backdoor['target_url']: self.target_url = backdoor['target_url']
        else: self.target_url = None 
        if backdoor['attacker_ip']: self.attacker_ip = backdoor['attacker_ip']
        else: self.attacker_ip = None 
        if backdoor['attacker_url']: self.attacker_url = backdoor['attacker_url']
        else: self.attacker_url = None 
        if backdoor['payload_url']: self.payload_url = backdoor['payload_url']
        else: self.payload_url = None
        if backdoor['entries']: self.entries = backdoor['entries']
        else: self.entries = []
        if backdoor['modules']: self.modules = backdoor['modules']
        else: self.modules = []
        if backdoor['shell']: self.shell = backdoor['shell']
        else: self.shell = None
        if backdoor['status']: self.status = backdoor['status']
        else: self.status = None
        if backdoor['error']: self.error = backdoor['error']
        else: self.error = []


    def save_backdoor(self):
        backdoor = {}
        if self.name: backdoor['name'] = self.name
        else: backdoor['name'] = None
        if self.type: backdoor['type'] = self.type
        else: backdoor['type'] = None
        if self.target_ip: backdoor['target_ip'] = self.target_ip
        else: backdoor['target_ip'] = None
        if self.target_url: backdoor['target_url'] = self.target_url
        else: backdoor['target_url'] = None
        if self.attacker_ip: backdoor['attacker_ip'] = self.attacker_ip
        else: backdoor['attacker_ip'] = None
        if self.attacker_url: backdoor['attacker_url'] = self.attacker_url
        else: backdoor['attacker_url'] = None
        if self.payload_url: backdoor['payload_url'] = self.payload_url
        else: backdoor['payload_url'] = None
        if self.entries: backdoor['entries'] = self.entries
        else: backdoor['entries'] = []
        if self.modules: backdoor['modules'] = self.modules
        else: backdoor['modules'] = []
        if self.shell: backdoor['shell'] = self.shell
        else: backdoor['shell'] = None
        if self.status: backdoor['status'] = self.status
        else: backdoor['status'] = None
        if self.error: backdoor['error'] = self.error
        else: backdoor['error'] = None
        add_backdoor(backdoor)


    def rm_backdoor(self):
        remove_backdoor(self.name)

    
    def print_backdoorclass(self):
        print(self.name)
        print(self.attacker_ip)
        print(self.type)
        print(self.entries)
        print(self.modules)

    def print_backdoorclass_simple(self):
        print('Nombre: ' + self.name)
        if self.type != None:
            print('Tipo: ' + self.type)
        else: print('Tipo: -')
        if self.target_ip != None:
            print('Objetivo: ' + self.target_ip)
        else: print('Objetivo: -')
        if self.status != None:
            print('Estado: ' + self.status)
        else: print('Estado: -')

    def to_msg(self):
        return [
            
        ]


def get_saved_backdoors():
    backdoor_class_list = []
    backdoors_json = read_backdoors()
    i = 0
    for backdoor in backdoors_json['backdoors']:
        backdoor_class_list.append(Backdoor(backdoor['name']))
        backdoor_class_list[i].get_backdoor()
    return backdoor_class_list

