# {FILE: java_manager.py}
# imports
import subprocess
import os


class JavaManager():
    def __init__(self, main='', src='', classpath='', pkg=''):
        self.main = main
        self.src = src
        self.classpath = classpath
        self.pkg = pkg

    def printInfo(self):
        print("JavaManager Info:")
        print("main: " + self.main)
        print("src: " + self.src)
        print("classpath: " + self.classpath)
        print("pkg: " + self.pkg)
        print("#========")

    def prepare(self, mainPath):
        """prepate for compile&run java\n
        Args:
            mainPath (str): the path fo mainPath
        """
        self.main = os.path.basename(mainPath).replace('.java', '')
        self.readClasspath()

    def readClasspath(self):
        # TODO: read .classpath file
        self.src = "./src"
        self.classpath = "./bin"
        self.pkg = "app"


    def compileJava(self):
        arg1 = "-d {}".format(self.classpath)
        input1 = "{}/*".format(self.src)
        subprocess.Popen("javac " + arg1 + " " + input1, shell=True)
        # javac -d $classpath $src/*

    def runJava(self, inputContent):
        arg1 = "-cp {}".format(self.classpath)
        input1 = "{}.{}".format(self.pkg, self.main)
        cmd = ["java", "-cp", self.classpath, input1]

        result = subprocess.run( cmd, stdout=subprocess.PIPE, input=inputContent, encoding='ascii')
        # java -cp $classpath $pkg.$main
        print(result)

        # TODO:
        print("test")
        print(result.stdout)
        return result.stdout