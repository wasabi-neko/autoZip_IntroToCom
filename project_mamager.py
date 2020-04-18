import os
import re
import subprocess

from file_manager import  FileManager

# Holy shit dirty code
# fuck myself

class ProjectManager():
    def __init__(self, projectName='', projectPath='', javaPath='', pngPath=''):
        self.projectName = projectName
        self.projectPath = projectPath
        self.fileManager = FileManager(projectName, projectPath, javaPath, pngPath)

    def printInfo(self):
        """print the info of the project{projectName, filePath}
        """
        print("ProjectName:" + self.projectName)
        print("projectPath:" + self.projectPath)
        self.fileManager.printInfo()


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
            


    def readInput(self, prompt):
        """\nPrompt interface to ask for project name
        
        Args:
            prompt (str): the prompt of fileName
        
        Returns:
            str: the user input
        """
        print("{} file not found".format(prompt))
        print("Please enter the content of {}".format(prompt))
        print("(you can config the {}s in folder:'autoZip')".format(prompt))
        # garbage code... 'w'
        content = ''
        while True:
            try:
                content += input() + '\n'
            except EOFError:
                break
        return content


    def getInput(self, number=0):
        """\nGet input for javaFile. ask for input if no input file in `/autoZip`
        
        Args:
            number (int, optional): the number of input. Defaults to 0.
        
        Returns:
            str: the input content
        """
        inputPath = self.fileManager.getFilePath('input', number)
        content = ''
        if (not os.path.isfile(inputPath)):
            content = self.readInput('input')
            print("Saving...")
            self.fileManager.saveFile('input', number, content)
        else:
            print("using inputFile:{} as input".format(inputPath))
            with open(inputPath, 'r') as file:
                content = file.read()
        return content
        

    def getOutput(self, number=0):
        """\nGet std output for javaFile. ask for output if no output file in `/autoZip`
        
        Args:
            number (int, optional): the number of output File. Defaults to 0.
        
        Returns:
            str: the output for javaFile
        """
        outputPath = self.fileManager.getFilePath('output', number)
        content = ''
        if (not os.path.isfile(outputPath)):
            content = self.readInput('output')
            print("Saving...")
            self.fileManager.saveFile('output', number, content)
        else:
            with open(outputPath, 'r') as file:
                content = file.read()
        return content


    def prepare(self, resetAll=False):
        """\nPrepare for autoZIP. step: set projectName, find java file, rename javaFile
        
        Args:
            resetAll (bool, optional): [description]. Defaults to False.
        """
        if (self.projectName == ''):
            self.readProjectPath()
        self.fileManager.prepare(self.projectName, self.projectPath)
        
    def resetAll(self):
        """resset all
        """
        self.projectName = ''
        self.projectPath = ''
        self.fileManager.resetAll()
        

    def runJava(self, withoutInput=False):
        """Compile and exec the java files
        
        Args:
            withoutInput (bool, optional): true if inputs is not needed for the program. Defaults to False.
        
        Returns:
            str: the result of execution of the javaFile
        """
        print("exec java...")
        inputContent = self.getInput()
        result = None
        try:
            result = subprocess.run(["java", self.fileManager.javaPath], stdout=subprocess.PIPE, input=inputContent, encoding='ascii')
        except:
            print("Error:JavaFile Not Found.\tat `runJava`")
        
        if(withoutInput == True):
            inputContent = ''
        print("java exec success!")
        return inputContent + result.stdout
    

    def autoZip(self):
        """autoZip
        """
        self.prepare()
        content = self.runJava()
        self.fileManager.saveImg(content)
        self.fileManager.zipFiles()
    
    def upload(self):
        pass

if __name__ == "__main__":
    project = ProjectManager()
    project.autoZip()