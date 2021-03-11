import datetime

schedule = {
    '평일': {
        datetime.time(hour=6, minute=17): '기상송',
        datetime.time(hour=6, minute=27): '아침운동체크',
        datetime.time(hour=7, minute=15): '3학년아침',
        datetime.time(hour=7, minute=18): '2학년아침',
        datetime.time(hour=7, minute=21): '1학년아침',
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
        datetime.time(hour=8, minute=10): '3학년아침',
        datetime.time(hour=8, minute=15): '2학년아침',
        datetime.time(hour=8, minute=20): '1학년아침',
        datetime.time(hour=12, minute=30): '3학년점심',
        datetime.time(hour=12, minute=35): '2학년점심',
        datetime.time(hour=12, minute=40): '1학년점심',

	datetime.time(hour=17, minute=10):'복귀체크',
        datetime.time(hour=18, minute=0): '3학년저녁',
        datetime.time(hour=18, minute=3): '2학년저녁',
        datetime.time(hour=18, minute=6): '1학년저녁',
        datetime.time(hour=19, minute=0): '복귀체크',
	
        datetime.time(hour=21, minute=17): '입구폐쇄',
        datetime.time(hour=22, minute=20): '기상송다운로드',
        datetime.time(hour=22, minute=27): '점호준비',
        datetime.time(hour=22, minute=40): '점호시작',
        datetime.time(hour=22, minute=50): '점호종료'
    }
}
