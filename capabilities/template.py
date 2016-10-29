#This is the template to create backdoors. Please copy your backdoor into the suggested spots. Places you need to input are shown by ~tildes~.
from capability import *
#Remember extra imports.

class ~NAME~(Capability):

    def __init__(self, core):
        super(~NAME~, self).__init__core()
        self.name = "~NAME~"
        self.intro = GOOD + "Using ~NAME~ module..."
        self.core = core
        self.options = { #~Input extra options. You almost always need a port.~
                #example: "hi":  Option("hi", "default", description", True),
                }
        self.help_text = ""

    def restore(self):

    def launch(self):
	#~Add all commands needed to run the program.~

#After you have filled out this entire program, move it to the correct folder. 



