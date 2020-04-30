# {File: project_manager.py}
# imports
import os

# my imports
from java_manager import JavaManager
from zip_manager import ZipManager
from file_manager import FileManager
import tools

class ProjectManager():
    def __init__(self, projectPath='', projectName='', mainPath=''):
        self.projectPath = projectPath
        self.projectName = projectName
        self.mainPath = mainPath
        self.javaManager = JavaManager()
        self.zipManager = ZipManager()
        self.fileManager = FileManager()

    def execAll(self):
        self.readProjectPath()
        self.prepare()
        self.autoZip()

    def printInfo(self):
        print("projectManager Info:")
        print("projectName: " + self.projectName)
        print("projectPath: " + self.projectPath)
        print("mainPath: " + self.mainPath)
        print("#======")
        self.javaManager.printInfo()
        self.zipManager.printInfo()

    def readProjectPath(self):
        """Read project path from user input
        """
        while True:
            projectName = input("Enter your project name or path:")
            projectPath = ''

            if (projectName == ''):
                print("Try again")
                continue

            # preprocese fo projectPath
            # "P01" -> "./P01", "~/Document/P01" -> "~/Document/01"(not changed)
            if (projectName[0] == '.' or projectName[0] == '/' or projectName[0] == '~'):
                # input is a project path
                projectPath = projectName
                projectName = projectPath.split('/')[-1]
            else:
                # input is a project name
                projectPath = "./" + projectName

            if (not os.path.isdir(projectPath)):
                print("Error: folder'{}' not found.".format(projectPath))
                print("Please try again.\n")
                continue

            self.projectName = projectName
            self.projectPath = projectPath
            break
    

    def prepare(self):
        os.chdir(self.projectPath)

        self.mainPath = tools.findJavaMainFile("./")
        self.javaManager.prepare(self.mainPath)
        self.zipManager.prepare(self.mainPath, self.projectName, self.javaManager.src)
        self.fileManager.prepare()

        self.printInfo()

    def autoZip(self):
        inputContent = ''
        if (self.fileManager.hasInputFile()):
            inputContent = self.fileManager.getInput(0)
        else :
            inputContent = tools.readInput("input")
            self.fileManager.saveInput(inputContent)

        print("running java...")
        output = self.javaManager.runJava(inputContent)
        print("Compeleted")
        
        print("zipping files and outputs")
        content = inputContent + output
        self.zipManager.saveImg(content)
        self.zipManager.zipFiles()
        print("Compeleted")