
# TODO:
#   - getModule()
#   - getBackdoor()
#   - setBackdoor()
#   - addBackdoor()
#   - rmBackdoor()
#   - 

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
        
