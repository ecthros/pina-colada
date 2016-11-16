from capability import *
from os import *

class wifi_connect(Capability):

    def __init__(self, core):
        super(wifi_connect, self).__init__(core)
        self.name = "Wifi Connect"
        self.intro = GOOD + "Using Wifi Connection module..."
        self.core = core
        self.options = { 
                #example: "hi":  Option("hi", "default", description", True),
                    "ssid":     Option("ssid", "", "SSID to connect to", True),
                    "password": Option("password", "", "Password to use", True),
                }
        self.help_text = "Allows you to connect to wifi."

    def restore(self):
        os.system("nmcli dev disconnect wlan0")

    def launch(self):
        if self.get_value("password") == "":
            os.system("nmcli dev wifi connect " + str(self.get_value("ssid")))
        else:
            os.system("nmcli dev wifi connect " + str(self.get_value("ssid")) + " password " + str(self.get_value("password")))
