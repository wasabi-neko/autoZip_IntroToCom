import subprocess
import re
import os
import shutil
import zipfile
import glob
import platform
import json
from PIL import Image, ImageDraw, ImageFont


# ==============================================================================
# Class: FileManager
# Usage: control files in the project
# ==============================================================================
class FileManager():
    FOLDER_NAME = 'autoZip'
    studentID = ''
    config = {}
    DEFAULT_CONFIG = {
        'img': {
            'fontSize': 30,
            'fontFamily': 'Courier New.ttf',
            'startPoint': (0,0),
            'extendX': 10,
            'extendY': 10,
            'imgColor': (0,0,0),
            'textColor': (255,255,255)
        }
    }

    def __init__(self, projectName='',projectPath='', javaPath='', pngPath=''):
        self.projectName = projectName
        self.projectPath = projectPath
        self.javaPath = javaPath
        self.pngPath = pngPath


    def printInfo(self):
        """Print all of the files
        """
        print("javaPath:" + self.javaPath)
        print("pngPath:" + self.pngPath)
        print("folderPath" + self.getFilePath())


    def resetAll(self):
        """Reset all 
        """
        # remove all files in 'folder': 'autoZip'
        for root, dirs, files in os.walk(self.getFilePath('folder')):
            for file in files:
                os.remove(file)
        os.removedirs(self.getFilePath('folder'))
        self.projectName = ''
        self.projectPath = ''
        self.javaPath = ''
        self.pngPath = ''


    def getFilePath(self, fileType='folder', number=0):
        """\nReturn the path of some file
        
        Args:
            fileType (str): the file type:{'config', 'folder', 'input', 'output'}
            number (str): the number of inputfile. e.g. input2
        
        Returns:
            str: the path of the target file. return `None` when enter the wrong fileType
        """
        if (type(number) != str):
            number = str(number)
        
        re = ''
        if (fileType == 'config'):
            # re = '{}/{}/config'.format(self.projectPath, self.FOLDER_NAME)
            re = './config.json'
        elif (fileType == 'folder'):
            re = '{}/{}'.format(self.projectPath, self.FOLDER_NAME)
        elif (fileType == 'input'):
            re = '{}/{}/input{}'.format(self.projectPath, self.FOLDER_NAME, number)
        elif (fileType == 'output'):
            re = '{}/{}/output{}'.format(self.projectPath, self.FOLDER_NAME, number)
        else:
            Warning("the fileType:{} not found...\n#\tat `getFilePath`".format(fileType))
            re = None
        
        return re

    
    def saveFile(self, content, fileType='folder', number=0):
        """\nA template of saving file
        
        Args:
            content (str): the content of the file
            fileType (str, optional): the fileType you wanna save(input, output, folder). Defaults to 'folder'.
            number (int, optional): the number of input/output. Defaults to 0.
        
        Returns:
            boolean: return if file save sucessfully
        """
        filePath = self.getFilePath(fileType, number)
        try:
            with open(filePath, 'w') as file :
                file.write(content)
            print("{}{}:{} save Successfully!OwO".format(fileType, number, filePath))
            return True
        except:
            print("{}{}:{} save FAILED!".format(fileType, number, filePath))
            return False


    def setConfig(self, config=None):
        """\nSet the configration of the autoZip. Use default if input is None
        
        Args:
            config (object, optional): the config you wanna set. Use default if input is None. Defaults to None.
        """
        path = self.getFilePath('config')
        if (config == None):
            config = self.DEFAULT_CONFIG
        
        self.config = config
        with open(path, 'w') as file:
            file.write(json.dumps(config))


    def getConfig(self):
        """\nget config from file and retrun a copy
        
        Returns:
            dict: a copy of config
        """
        path = self.getFilePath('config')
        if (not os.path.isfile(path)):
            self.setConfig()
        
        with open(path, 'r') as file:
            self.config = json.loads(file.read())
        self.config['img']['imgColor'] = tuple(self.config['img']['imgColor'])
        self.config['img']['textColor'] = tuple(self.config['img']['textColor'])
        self.config['img']['startPoint'] = tuple(self.config['img']['startPoint'])
        return self.config.copy()
            

    def findNewJavaFile(self):
        """\nSearching for the java file in the project
        
        Returns:
            str: the path of the java file
        """
        newPath = ''
        print("Searching new java files")
        for root, dirs, files in os.walk(self.projectPath):
            for file in files:
                if (re.search(r".*java", file) and file != self.javaPath):
                    newPath = root + "/" + file
                    break
        return newPath


    def updateJavaFile(self):
        """Find the new java file in the project then copy it to root and rename
        """
        newPath = self.findNewJavaFile()

        if (self.javaPath == ''):
            self.studentID = getStudentID(newPath)
            if (self.studentID == ''):
                print("StudentID not found in java file{}.".format(newPath))
                print("EXIT!")
                exit()
            self.javaPath = '{}/{}_{}.java'.format(self.projectPath, self.projectName, self.studentID)
        else:
            os.remove(self.javaPath)
        
        shutil.copy(newPath, self.javaPath)
    
    def saveImg(self, content):
        """\ndraw a img and save
        
        Args:
            content (str): input + output
        """
        setting = self.config['img']
        textSize = setting['fontSize']
        fontFamily = setting['fontFamily']

        startPoint = self.config['img']['startPoint']

        imgColor = setting['imgColor']
        textColor = setting['textColor']

        
        font = ImageFont.truetype(fontFamily, textSize)
        imgRows = 0
        imgColumns = 0
        size = list(font.getsize(max(content.split('\n'), key=len)))
        imgColumns = size[0] + self.config['img']['extendX']
        imgRows = size[1] * content.count('\n') + self.config['img']['extendY']
        
        img = Image.new('RGB', (imgColumns, imgRows), color=imgColor)

        d = ImageDraw.Draw(img)
        d.text( startPoint, content,  font=font, fill=textColor)
        img.save(self.pngPath)
        print("png:{} save success!".format(self.pngPath))


    def prepare(self, projectName, projectPath):
        """\nprepare for `runJava`
        the task: get project name and path, updateJavaFile, make png path, make `autoZip` folder

        Args:
            projectName (str): the name of the project
            projectPath (str): the path of the project
        """
        
        self.projectName = projectName
        self.projectPath = projectPath
        self.updateJavaFile()
        self.pngPath = "{}/{}_{}.png".format(self.projectPath, self.projectName, self.studentID)
        if (not os.path.isdir(self.getFilePath('folder'))):
            os.mkdir(self.getFilePath('folder'))
        if (self.config == {}):
            self.getConfig()


    def zipFiles(self):
        """Make a zip file with java fie and png file
        """
        print("Zipping java and img files...")
        zipPath = "{}/{}_{}.zip".format(self.projectPath, self.projectName, self.studentID)
        with zipfile.ZipFile(zipPath, 'w') as zf:
            zf.write(self.pngPath)
            zf.write(self.javaPath)
        print("Zip success!")

    
    def saveCredit(self):
        pass
    

# ------------------------------------------------------------------------------
# Tool methods
# ------------------------------------------------------------------------------
def getBirthTime(path):
    """\nGet the birth time of the file
    capable with windows, macos, linux

    Args:
        path (str): the path of the target file
    Return:
        float: the birth time of the file
    """

    if platform.system == 'Windows':
        return os.path.getctime(path)
    else:
        stat = os.stat(path)
        try:
            return stat.st_birthtime
        except ArithmeticError:
            return stat.st_mtime


def searchNewestPng():
    """\nGet the newest png file at Desktop
    
    Returns:
        str: img file path
    """

    print("img file not found in projectfile.")
    print("Seraching the newest '*.png' at Desktop")

    # finding bigest(nest) png file at `~/Desktop`
    desktopPath = os.path.expanduser('~') + "/Desktop"
    maxBrithTime = 0
    for file in os.listdir(desktopPath):
        if ( re.search(r".*.png", file)):
            filePath = desktopPath + "/" + file
            if (getBirthTime(filePath) > maxBrithTime):
                maxBrithTime = getBirthTime(filePath)
                imgFilePath = filePath
    print("Img Path:'{}'\n".format(imgFilePath))
    return imgFilePath


def getStudentID(filePath):
    """\nGet student id from file
    
    Args:
        filePath (str): the path of the file
    
    Returns:
        str: the stduent id
    """
    print("Searching 'StudnetNumber' in File:{}\n".format(filePath))
    with open(filePath) as file:
        result = None
        for line in file:
            result = re.search(r".*student.*[0-9]{9}", line, re.IGNORECASE)
            if (result != None):
                break
        if result == None:
            print("Error: No StduentID in .java file.\nEXIT!")
            exit()
        studentNumber = re.search(r"[0-9]{9}", result.group()).group()
    return studentNumber


if __name__ == "__main__":
    print("UwU... no... not this.")