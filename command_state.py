
class CommandState(object):
    current_command = "NONE"

    def Start(self):
        self.current_command = "START"
        print(self.current_command)

    def Stop(self):
        self.current_command = "STOP"
        print(self.current_command)

    def Reset(self):
        self.current_command = "RESET"
        print(self.current_command)