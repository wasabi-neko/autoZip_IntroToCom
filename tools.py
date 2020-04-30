# `re` is regular expression
import re
import os

def readInput(prompt):
    """\nPrompt interface to ask for project name\n
    Args:
        prompt (str): the prompt of fileName
    
    Returns:
        str: the user input
    """
    # print("{} file not found".format(prompt))
    print("Please enter the content of {}".format(prompt))
    # print("(you can config the {}s in folder:'autoZip')".format(prompt))
    # garbage code... 'w'
    content = ''
    while True:
        try:
            content += input() + '\n'
        except EOFError:
            break
    return content


def getStudentIDFromFile(filePath):
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


def findJavaMainFile(workingdir):
    # TODO: 

    return os.path.join(workingdir, "src/app/App.java")
