# autoZip_IntroToCom
auto zip `.java` and `.png` to `.zip` in the format that fits the rule of 1082IntoductionToComputerSicence

## Intro
由於我懶得改檔名&做Zip檔，所以就寫了這個
## Usage
```bash=
$cd ./autoZip
$python3 main.py
$Enter your project path
$Enter input of path
# Done
```
input檔會留著，只要輸過一次，之後就不用輸了。
如果想要改掉原本的input，就把file: `input0` 刪除即可

### 單檔案 project

以下是舊版本(autoZip.py) 適用單 java 的 autoZip
```bash=
# !bash
$cp ./autoZip.py "your homeWork folder path"
$cd "your homework folder path"
$python3 ./autoZip.py
```
```口語=
# 白話版
把`autoZip.py`放到機概作業的root
run `python3 ./autoZip.py`
```
你看很簡單的～ :+1: 

### 多檔案 project
```bash=
# mv folder
$cp ./autoZip_IntroToCom "your homeWork folder path" 
$cd "path to autoZip_IntroToCom"
$pipenv run python main.py
```

## Customize
### `config.json`
- img
    - fontSize
    - fontFamily
    - spacing
    - imgColor
    - fontColor
### pathConfig.json
- src: the src folder of java files
- classpath: the classpath (the folder contained .class file)
- pkg: the java pakage you used
- main: the path of main java file

## TODOs
- [x] add java project support
  - [ ] add read `.classpath file`
- add exception handleing
- add more user interface
- add Docstring