from db import *

class Backdoor:
    def __init__(self):
        self.name = ''
        self.type = ''
        self.targetIP = ''
        self.targetURL = ''
        self.attackerIP = ''
        self.attackerURL = ''
        self.payloadURL = ''

        self.entries = []
        self.modules = []
        self.shell = ''
        self.status = ''
        self.error = ''
    
    def get_module(id):
        return search_module(id)
    
    def get_modules():
        return read_modules()

    def get_backdoor(name):
        return search_backdoor(name)

    def set_backdoor(backdoor):
        add_backdoor(backdoor)

    def rm_backdoor(name):
        remove_backdoor(name)
