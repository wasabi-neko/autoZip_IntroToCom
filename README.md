# autoZip_IntroToCom
auto zip `.java` and `.png` to `.zip` in the format that fits the rule of 1082IntoductionToComputerSicence

## Intro
由於我懶得改檔名&做Zip檔，所以就寫了這個
## Usage
```= bash
# ~bash
$cp ./autoZip.py "your homeWork folder path"
$cd "your homework folder path"
$python3 ./autoZip.py
```
```= 口語
把`autoZip.py`放到機概作業的root
run `python3 ./autoZip.py`
```
你看很簡單的～ :+1: 

## 程式流程
- 由使用者輸入 $projectName
- 尋找 $projectFolder 裡的 `.java` & `.png`
- 如果 $projectFolder 裡沒有 `.png`
    - 從`桌面`提取最新的`.png`
- 從 `.java` 檔裡提取 $studentID
- 把原`.java``.png` 複製至 $projectfoler 並改名
- 生產`.zip`
- complete
