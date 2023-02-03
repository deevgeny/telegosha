"""
External API Mock data.
"""


USER_TASKS = [
    {"topic": "Цвета",
     "type": "quiz",
     "data": [
             {'word': 'зелёный',
              'buttons': [{'green': 'correct'}, {'blue': 'incorrect'},
                          {'pink': 'incorrect'}]},
             {'word': 'розовый',
                 'buttons': [{'pink': 'correct'}, {'blue': 'incorrect'},
                             {'black': 'incorrect'}]},
             {'word': 'красный',
                 'buttons': [{'green': 'incorrect'}, {'pink': 'incorrect'},
                             {'red': 'correct'}]},
             {'word': 'чёрный',
                 'buttons': [{'pink': 'incorrect'}, {'black': 'correct'},
                             {'red': 'incorrect'}]},
             {'word': 'желтый',
                 'buttons': [{'red': 'incorrect'}, {'yellow': 'correct'},
                             {'black': 'incorrect'}]},
             {'word': 'синий',
                 'buttons': [{'red': 'incorrect'}, {'blue': 'correct'},
                             {'black': 'incorrect'}]}]},
    {"topic": "Цвета",
     "type": "spelling",
     "data": [
             {'word': 'синий',
              'spelling': 'blue'},
             {'word': 'красный',
              'spelling': 'red'},
             {'word': 'зелёный',
              'spelling': 'green'},
             {'word': 'чёрный',
              'spelling': 'black'},
             {'word': 'желтый',
              'spelling': 'yellow'},
             {'word': 'розовый',
              'spelling': 'pink'}]}
]
