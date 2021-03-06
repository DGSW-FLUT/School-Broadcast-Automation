import datetime

schedule = {
    '평일': {
        datetime.time(hour=6, minute=17): '기상송',
        datetime.time(hour=6, minute=27): '아침운동체크',
        datetime.time(hour=7, minute=14): '3학년아침',
        datetime.time(hour=7, minute=19): '2학년아침',
        datetime.time(hour=7, minute=24): '1학년아침',
        datetime.time(hour=7, minute=57): '기상송',
        datetime.time(hour=8, minute=15): '기상송초기화',
        datetime.time(hour=8, minute=17): '기숙사퇴실',
        datetime.time(hour=21, minute=17): '입구폐쇄',
        datetime.time(hour=22, minute=20): '기상송다운로드',
        datetime.time(hour=22, minute=27): '점호준비',
        datetime.time(hour=22, minute=40): '점호시작',
        datetime.time(hour=22, minute=50): '점호종료'
    },
    '휴일': {
        datetime.time(hour=7, minute=27): '기상송',
        datetime.time(hour=7, minute=37): '아침운동체크',
        datetime.time(hour=7, minute=47): '기상송초기화',
        datetime.time(hour=8, minute=9): '3학년아침',
        datetime.time(hour=8, minute=14): '2학년아침',
        datetime.time(hour=8, minute=19): '1학년아침',
        datetime.time(hour=12, minute=29): '3학년점심',
        datetime.time(hour=12, minute=34): '2학년점심',
        datetime.time(hour=12, minute=39): '1학년점심',

        datetime.time(hour=17, minute=59): '3학년저녁',
        datetime.time(hour=18, minute=4): '2학년저녁',
        datetime.time(hour=18, minute=9): '1학년저녁',
        datetime.time(hour=19, minute=10): '복귀체크',

        datetime.time(hour=21, minute=17): '입구폐쇄',
        datetime.time(hour=22, minute=20): '기상송다운로드',
        datetime.time(hour=22, minute=27): '점호준비',
        datetime.time(hour=22, minute=40): '점호시작',
        datetime.time(hour=22, minute=50): '점호종료'
    }
}
