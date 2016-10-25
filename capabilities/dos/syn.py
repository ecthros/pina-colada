from capability import *

class Syn(Capability):
    
    def __init__(self, core):
        super(Syn, self).__init__(core)
        self.name = "Syn Scan"
        self.options = {
                "port"   : Option("port", 53923, "port to connect to", True),
                }
        self.help_text = INFO + "Uses a simple bash command to connect to a specific ip and port combination, and pipes its input into a bash shell." 

    def launch(self):
        pass
