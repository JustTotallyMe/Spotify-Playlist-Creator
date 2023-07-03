

class ConfigHelper:
    def __init__(self, configFilePath):
        self.path = configFilePath

    def writeToFile(self, content):
        file = open(self.path, mode='ap')
        file.write(content)
        file.close()

    def readFromFile(self):
        return open(self.path).read()