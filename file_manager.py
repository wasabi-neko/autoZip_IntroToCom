import os

class FileManager():
    dirPath = './autozip'

    def __init__(self, inputFiles='', outputFiles='', config=''):
        self.inputFiles = inputFiles
        self.ouptutFiles = outputFiles
        self.config = config

    def prepare(self):
        self.checkFolder()

    def checkFolder(self):
        if (self.hasFolder() == False):
            os.mkdir(self.dirPath)
    

    def hasFolder(self):
        return os.path.isdir(self.dirPath)

    def hasInputFile(self):
        return os.path.isfile(self.dirPath + '/input.txt')


    def hasOutputFile(self):
        return False
    
    def getInput(self, index=0):
        with open(self.dirPath + '/input.txt', 'r') as file:
            return file.read()

    def getOutput(self, index=0):
        pass

    def getConfig(self):
        pass

    def saveInput(self, content, index=0):
        self.checkFolder()
        with open(self.dirPath + '/input.txt', 'w+') as file:
            file.write(content)
