# School Broadcast Automation
![alt](/example.png)
![alt](/wiring_diagram.png)
Build with Python3.7
## Available Platform
* Windows 7 or later
* Raspbian Buster or later(**Buster 이전 버전은 Python3.7을 지원하지 않음**)
## 권장 프로젝트 세팅
### Windows
1. Python 3.7 설치
2. Pycharm Community 설치
3. GitTool(GitKraken, Github Desktop, Git Bash 등등)로 레포지토리 복제
4. Pycharm 으로 virtual env 생성
5. `pip3 install -r requirements-windows.txt` 로 의존 라이브러리 설치
6. Python으로 run.py 실행
### Linux
1. `sudo apt-get install python3 python3-dev-tools python3-setuptools` 로 파이썬 설치
2. `sudo python3 -m pip install -r requirements-posix.txt` 로 의존 라이브러리 설치
3. `sudo python3 run.py` 로 실행(**GUI 환경에서 실행**)

## 하드웨어 환경

## References
* [QDarkStyleSheet](https://github.com/ColinDuquesnoy/QDarkStyleSheet/)
* [IBM TTS](https://cloud.ibm.com/apidocs/text-to-speech?code=python/)
