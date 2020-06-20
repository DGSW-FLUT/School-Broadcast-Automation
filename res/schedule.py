import datetime

schedule = {
    '평일': {
        datetime.time(hour=6, minute=17): '기상송',
        datetime.time(hour=7, minute=10): '3학년아침',
        datetime.time(hour=7, minute=15): '2학년아침',
        datetime.time(hour=7, minute=20): '1학년아침',
        datetime.time(hour=7, minute=57): '기상송',
        datetime.time(hour=9, minute=10): '나이스자가진단',

        datetime.time(hour=22, minute=30): '점호준비',
        datetime.time(hour=22, minute=40): '점호시작',
        datetime.time(hour=22, minute=50): '점호종료'
    },
    '휴일': {
        datetime.time(hour=7, minute=27): '기상송',
        datetime.time(hour=8, minute=10): '3학년아침',
        datetime.time(hour=8, minute=15): '2학년아침',
        datetime.time(hour=8, minute=20): '1학년아침',
        datetime.time(hour=9, minute=10): '나이스자가진단',
        datetime.time(hour=12, minute=10): '3학년점심',
        datetime.time(hour=12, minute=15): '2학년점심',
        datetime.time(hour=12, minute=20): '1학년점심',
        # datetime.time(hour=18, minute=0): '기숙사이동',
        datetime.time(hour=18, minute=5): '3학년저녁',
        datetime.time(hour=18, minute=10): '2학년저녁',
        datetime.time(hour=18, minute=15): '1학년저녁',

        datetime.time(hour=22, minute=30): '점호준비',
        datetime.time(hour=22, minute=40): '점호시작',
        datetime.time(hour=22, minute=50): '점호종료'
    }
}
