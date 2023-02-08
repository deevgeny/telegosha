COMMANDS_LEXICON: dict[str, str] = {
    '/start': ('Привет!\n\nТеперь я твой помощник. Мы будем вместе учить '
               'английские слова. Время от времени я буду присылать тебе '
               'разные задания и проводить словарные диктанты.\n\nЯ умею '
               'выполнять следующие команды:\n\n'
               '/help - подсказка\n/tasks - задания\n/cancel - отмена'),
    'start_description': 'задания',
    '/help': ('Я помощник для запоминания английских слов.\n'
              'Я могу проводить словарный диктант.\n'
              'Помогаю учить новые слова.\n\nЯ умею выполнять следующие '
              'команды:\n\n/help - подсказка\n/tasks - задания'
              '\n/cancel - отмена'),
    'help_description': 'помощь',
    'cancel_description': 'отмена',
    'tasks_description': 'задания'
}

QUIZ_LEXICON: dict[str, str] = {
    'title': '&#128214; <b>Словарный тест</b>\n\n',
    'topic': 'Тема: ',
    'total_questions': 'Количество слов: ',
    'rules': ('Правила:\n- Я буду по очереди присылать слова на русском языке '
              'с вариантами перевода.\n- Необходимо выбирать правильный '
              'вариант ответа.\n- Тест можно прервать командой '
              '/cancel или найти ее в меню'),
    'result_title': '&#128214; <b>Словарный тест окончен</b>\n\n',
    'quiz_exit': ('Хорошо, выполним словарный тест позже.\n\nЧтобы начать '
                  'словарный тест отправьте команду /quiz или '
                  'воспользуйтесь кнопкой меню.'),
    'quiz_warning': ('&#128070; <b>В этом задании можно использовать только '
                     'кнопки!</b>\n\nЗадание можно отменить командой /cancel '
                     'и выполнить его позже. При этом прогресс не будет '
                     'сохранен!\n\nКоманду отмены можно так же найти в меню.\n'
                     '&#128071;'),
    'correct': ['&#128587; Отлично!\n', '&#128587; Молодец!\n',
                '&#128587; Так держать!\n'],
    'incorrect': ['&#129335; Неверно.\n', '&#129335; Ошибка.\n',
                  '&#129335; Ну как же так.\n'],
    'total_correct': 'Правильных ответов: ',
    'total_incorrect': 'Неправильных ответов: ',
    'total_left': 'Осталось: ',
    'start_button': 'Начать',
    'exit_button': 'Отмена',
    'next_button': 'Следующее слово',
    'result_button': 'Результат'
}

SPELLING_LEXICON: dict[str, str] = {
    'title': '&#128221; <b>Словарный диктант</b>\n\n',
    'topic': 'Тема: ',
    'total_questions': 'Количество слов: ',
    'rules': ('Правила:\n- Я буду по очереди присылать слова на русском языке'
              '\n- На каждое присланное слово нужно писать его перевод на '
              'английском\n- Перевод можно писать как маленькими, так и '
              'заглавными буквами\n- Диктант можно прервать командой '
              '/cancel или найти ее в меню'),
    'result_title': '&#128221; <b>Словарный диктант окончен</b>\n\n',
    'correct': ['&#128587; Отлично!\n', '&#128587; Молодец!\n',
                '&#128587; Так держать!\n'],
    'incorrect': ['&#129335; Неверно.\n', '&#129335; Ошибка.\n',
                  '&#129335; Ну как же так.\n'],
    'feedback': 'Правильный ответ:\n',
    'total_correct': 'Правильных ответов: ',
    'total_incorrect': 'Неправильных ответов: ',
    'mistakes': 'Неправильные ответы:\n',
    'start_button': 'Начать',
    'exit_button': 'Отмена',

}

TASKS_LEXICON: dict[str, str] = {
    'title': '&#128203; <b>Задания</b>\n\n',
    'no_tasks': 'Новых заданий пока нет',
    'select_button': 'Выбрать',
    'prev_button': '<<',
    'next_button': '>>',
    'quiz': 'Словарный тест',
    'spelling': 'Словарный диктант',
    'pointer': '&#128073;',
    'tab': '&#9;' * 7,
    'error': 'Произошла ошибка!'
}
