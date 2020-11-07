# School Broadcast Automation
![alt](/data/example.png)
Build with Python3.7
## Available Platform
* Windows 7 or later
* Raspbian Buster or later(**Buster 미만 버전은 Python3.7을 지원하지 않음**)
## 권장 프로젝트 세팅
### Windows
1. Python 3.7 설치
2. Pycharm Community 설치
3. GitTool(GitKraken, Github Desktop, Git Bash 등등)로 레포지토리 복제
4. Pycharm 으로 virtual env 생성
5. `pip3 install -r requirements-windows.txt` 로 의존 라이브러리 설치
6. Python으로 run.py 실행
### Linux
1. `sudo apt-get install python3 python3-dev-tools python3-setuptools qt5-default` 로 파이썬 설치
2. `sudo python3 -m pip install -r requirements-posix.txt` 로 의존 라이브러리 설치
3. `sudo python3 run.py` 로 실행(**GUI 환경에서 실행**)
### Project 구조
#### 실행 구조
1. `planner.ui` 를 이용하여 `MainWindow(QtWidgets.QMainWindow)`를 생성 
2. 각 로그 유닛(`external_storage_manager.py`, `music_player.py`, `scheduler.py`)을 생성 후 실행
3. `data/schedule.py`를 바탕으로 스케줄 조회 창 완성, `data/quick_macros.py`를 바탕으로 매크로 버튼 목록 완성
4. 로그 갱신 타이머(`log_timer(QTimer)`) 실행
5. `MainWindow` 콘솔 입력, 로그 표시, 매크로 입력 등의 UI 작업 처리  
  `ExternalStorageManager(QThreadWithLogging)` 외부저장장치 변동 시에 외부저장장치의 mp3를 내부저장장치로 복사
  `MusicPlayer(QThreadWithLogging)` 플레이 리스트에 음악이 있다면 재생  
  `Scheduler(QThreadWithLogging)` `data/schedule.py`에 따라서 해당하는 태그를 실행
6. 로그 갱신 타이머 중단 후 각 로그 유닛의 `close()` 호출 뒤 종료.

#### 콘솔 명령어(MainWindow에서 처리)
- `test` 테스트 방송 송출
- `get_musics` 현재 기상송 목록 표시 
- `all_around_test` 당일 스케줄의 모든 태그 명령어 순차 실행 
- `-로 시작하는 명령어들` 태그 명령어로 실행 
#### 태그 명령어(Scheduler에서 처리)
##### 정적 태그 명령어
고정 오디오 재생시 사용
- `입구폐쇄, 점호준비, 점호시작, 점호종료, 기숙사퇴실, M-N학년급식`
##### 동적 태그 명령어
- `기상송` 기상송 재생목록에 추가 `buffer/`에 비었을 경우(`ExternalStorageManager` 참조) 기본 노래 추가  
  (실제 재생은 `MusicPlayer`에서 실행함) 
- `기상송초기화` `buffer/` 초기화 
- `아침운동체크` `MusicPlayer`에서 재생중인 노래 일시정지 후 `아침운동체크.mp3` 재생
#### `run.py` 구조
- `create_quick_macro_button` 매크로 버튼 UI 생성 함수
- `qt_message_handler` Qt가 보내는 메시지 핸들링 함수


#### File 구조
+ `run.py`, `scheduler.py`, `music_player.py`, `external_storage_manager.py`  
   등의 기본 소스코드가 루트에 존재
+ `audio/` 오디오 파일 존재 
+ `audio/default_music/` 각 요일별 기본 노래 존재 
+ `buffer/` 외부저장소(USB)에서 복사된 파일이 존재
+ `data/` 리소스 파일 존재
+ `data/planner.ui` Qt5 UI 파일
+ `data/quick_macros.py` 매크로의 이름과 해당 콘솔 명령어 목록 
+ `data/requiremnets-posix.txt` 리눅스 환경에서 필요한 파이썬 모듈 목록
+ `data/requiremnets-windows.txt` 윈도우 환경에서 필요한 파이썬 모듈 목록
+ `data/schedule.py` 평일과 휴일의 스케쥴의 태그 명령어와 시간 목록
 

## 하드웨어 환경
![alt](/data/wiring_diagram.png)

## References
* [QDarkStyleSheet](https://github.com/ColinDuquesnoy/QDarkStyleSheet/)
