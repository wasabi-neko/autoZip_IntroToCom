# {FILE: ZIP_MANAGER}

# imports
import os
import re
import zipfile
import shutil
from PIL import Image, ImageDraw, ImageFont

# my modules
import tools    

class ZipManager():
    DEFAULT_CONFIG = {
        'img': {
            'fontSize': 30,
            'fontFamily': 'Courier New.ttf',
            'spacing': 0.5,
            'startPoint': (0,0),
            'extendX': 10,
            'extendY': 10,
            'imgColor': (0,0,0),
            'textColor': (255,255,255)
        }
    }

    def __init__(self, outputFormat='', includePaths=[], studentID=''):
        """initialize\n
        Args:
            mainPath (str): the path of main program
            outputFormat (str): the format of outputs. "{projectName}_{stduentID}"
            includePaths (list, optional): [description]. Defaults to [''].
            studentID (str, optional): [description]. Defaults to ''.
        """
        self.outputFormat = outputFormat
        self.includePaths = includePaths
        self.studentID = studentID
        self.config = self.DEFAULT_CONFIG

    def printInfo(self):
        print("ZipManager Info:")
        print("outputfFormat: " + self.outputFormat)
        print("includePaths: ")
        print(self.includePaths)
        print("stduentID: " + self.studentID)
        print("#======")


    def getImgPath(self):
        return self._getPath(".png")
    def getMainPath(self):
        return self._getPath(".java")
    def getZipPath(self):
        return self._getPath(".zip")

    def _getPath(self, typeStr):
        if (self.outputFormat != '' or self.outputFormat != None):
            return self.outputFormat + typeStr
        else :
            raise Exception("#Exception#: OutputFormat not set. cannot get {} output".format(typeStr))


    def prepare(self, mainPath, projectName, src):
        self.studentID = tools.getStudentIDFromFile(mainPath)
        self.outputFormat = "./{}_{}".format(projectName, self.studentID)

        fileList = []
        for root, dirs, files in os.walk(src):
            for file in files:
                if (re.search(r".*java", file) and file != mainPath):
                    fileList.append(os.path.join(root, file))

        if mainPath in fileList:
            fileList.remove(mainPath)
        
        self.includePaths = fileList
        self.config = self.DEFAULT_CONFIG

        # copy files to root
        shutil.copy(mainPath, self.getMainPath())
        for filePath in self.includePaths:
            shutil.copy(filePath, os.path.basename(filePath))


    def saveImg(self, content):
        """\ndraw a img and save
        Args:
            content (str): input + output
        """
        if (self.getImgPath() == '.png' or self.getImgPath() == None):
            raise Exception("#Exception#: Img Path not set! Cannot save img!")

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
        imgColumns = round(size[0] + self.config['img']['extendX'])
        imgRows = round(size[1] * (content.count('\n') + self.config['img']['spacing']) + self.config['img']['extendY'])
        

        img = Image.new('RGB', (imgColumns, imgRows), color=imgColor)
        d = ImageDraw.Draw(img)
        d.text( startPoint, content,  font=font, fill=textColor)

        img.save(self.getImgPath())
        print("Img:{} save success!".format(self.getImgPath()))


    def zipFiles(self):
        """Make a zip file with java fie and png file
        """
        print("Zipping java and img files...")
        zipPath = self.getZipPath()
        with zipfile.ZipFile(zipPath, 'w') as zf:
            zf.write(self.getImgPath())
            zf.write(self.getMainPath())
            for file in self.includePaths:
                zf.write(os.path.basename(file))
        print("Zip success!")    
