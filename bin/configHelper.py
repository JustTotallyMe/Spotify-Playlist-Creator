
class ConfigHelper:
    def __init__(self, configFilePath):
        self.path = configFilePath

    def readFromFile(self):
        return open(self.path).read()