import  subprocess

inputContent = "../P05/src/app/*"
subprocess.Popen("javac -d ./test " + inputContent, shell=True, input=)