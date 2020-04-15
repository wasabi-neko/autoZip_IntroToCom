# @Deprecated

import subprocess
import re
import os
import shutil
import zipfile
import glob
import platform

def getBirthTime(path):
    if platform.system == 'Windows':
        return os.path.getctime(path)
    else:
        stat = os.stat(path)
        try:
            return stat.st_birthtime
        except ArithmeticError:
            return stat.st_mtime

# `projectName` and `student number`
projectName = input("Enter your project/folder name:")
studentNumber = 0
projectPath = projectName

# preprocese fo projectPath
# "P01" -> "./P01", "~/Document/P01" -> "~/Document/01"(not changed)
if (projectPath[0] != '.' or projectPath[0] != '/' or projectPath[0] != '~'):
    projectPath = "./" + projectPath

if (not os.path.isdir(projectPath)):
    print("Error: folder'{}' not found. EXIT!\n".format(projectPath))
    exit()

print("Searching '.java' file and ('.png') file...")
javaFilePath = ""
imgFilePath = ""
for root, dirs, files in os.walk(projectPath):
    for file in files:
        if ( re.search(r".*java", file)):   
            # java file
            javaFilePath = root + "/" + file
        elif ( re.search(r".*.png", file)):
            # png file
            imgFilePath = root + "/" + file
        if (javaFilePath != "" and imgFilePath != ""):
            break

print("Java file:'{}'\nImg file:'{}'\n".format(javaFilePath, imgFilePath))
if (imgFilePath == ""):
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


if (javaFilePath == ""):
    print("Error: java file not found")
    exit()
if (imgFilePath == ""):
    print("Error: png file not found")
    exit()

print("Searching 'StudnetNumber' in JavaFile\n")
with open(javaFilePath) as file:
    result = None
    for line in file:
        result = re.search(r".*student.*[0-9]{9}", line, re.IGNORECASE)
        if (result != None):
            break
    if result == None:
        print("Error: No StduentID in .java file.\nEXIT!")
        exit()
    studentNumber = re.search(r"[0-9]{9}", result.group()).group()

print("StudentID:{}\n".format(studentNumber))


print("Renaming 'java' file and 'png' file...")
dstJavaPath = "{}/{}_{}.java".format(projectPath, projectName, studentNumber)
dstImgPath  = "{}/{}_{}.png".format(projectPath, projectName, studentNumber)
shutil.copyfile(javaFilePath, dstJavaPath)
shutil.move(imgFilePath, dstImgPath)


print("Zipping java and img files...")
zipPath = "{}/{}_{}.zip".format(projectPath, projectName, studentNumber)
with zipfile.ZipFile(zipPath, 'w') as zf:
    zf.write(dstJavaPath)
    zf.write(dstImgPath)

print("!!!!!Compelet!!!!")
print("The zip file:'{}'".format(zipPath))