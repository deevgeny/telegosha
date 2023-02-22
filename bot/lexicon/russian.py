COMMANDS_LEXICON: dict[str, str] = {
    '/start': ('Привет!\n\nЯ школьный помощник для запоминания иностранных '
               'слов.\nЯ умею выполнять следующие команды:\n\n'
               '/tasks - задания\n/progress - результаты\n/cancel - отмена\n'
               '/help - помощь\n'),
    '/help': ('Я школьный помощник для запоминания иностранных '
              'слов.\nЯ умею выполнять следующие команды:\n\n'
              '/tasks - задания\n/progress - результаты\n/cancel - отмена\n'
              '/help - помощь\n'),
    'tasks_description': 'задания',
    'progress_description': 'результаты',
    'help_description': 'помощь',
    'cancel_description': 'отмена',
}

TASKS_LEXICON: dict[str, str] = {
    'title': '&#128203; <b>Задания</b>\n\n',
    'no_tasks': 'Новых заданий пока нет',
    'select_button': 'Выбрать',
    'prev_button': '<<',
    'next_button': '>>',
    'quiz': 'Словарный тест',
    'spelling': 'Правописание',
    'pointer': '&#128073;',
    'tab': '&#9;' * 7,
}

INTRO_LEXICON: dict[str, str] = {
    'title': '<b>Знакомимся с новыми словами</b>\n\n',
    'result_title': '<b>Знакомство с новыми словами окончено</b>\n\n',
    'topic': 'Тема: ',
    'total_words': 'Количество слов: ',
    'rules': ('Правила:\n- Я буду по очереди присылать новые слова.\n- Нужно '
              'постараться их запомнить.\n- Задание можно прервать '
              'командой /cancel или найти ее в меню'),
    'warning': ('&#128070; <b>В этом задании можно использовать только '
                'кнопки!</b>\n\nЗадание можно отменить командой /cancel '
                'и выполнить его позже. При этом прогресс не будет '
                'сохранен!\n\nКоманду отмены можно так же найти в меню.\n'
                '&#128071;'),
    'start_button': 'Начать',
    'exit_button': 'Отмена',
    'next_button': 'Следующее слово',
    'result_button': 'Готово'
}

LEARN_LEXICON: dict[str, str] = {
    'title': '<b>Учим новые слова</b>\n\n',
    'result_title': '<b>Изучение новых слов окончено</b>\n\n',
    'topic': 'Тема: ',
    'total_words': 'Количество слов: ',
    'rules': ('Правила:\n- Я буду по очереди присылать новые слова.\n- Нужно '
              'постараться их запомнить.\n- После каждого нового слова я буду '
              'проверять, удалось ли его запомнить.\n- Задание можно прервать '
              'командой /cancel или найти ее в меню'),
    'warning': ('&#128070; <b>В этом задании можно использовать только '
                'кнопки!</b>\n\nЗадание можно отменить командой /cancel '
                'и выполнить его позже. При этом прогресс не будет '
                'сохранен!\n\nКоманду отмены можно так же найти в меню.\n'
                '&#128071;'),
    'correct': ['&#128587; Отлично!\n', '&#128587; Молодец!\n',
                '&#128587; Так держать!\n'],
    'incorrect': ['&#129335; Неверно.\n', '&#129335; Ошибка.\n',
                  '&#129335; Ну как же так.\n'],
    'total_left': 'Осталось: ',
    'total_correct': 'Правильных ответов: ',
    'total_incorrect': 'Неправильных ответов: ',
    'start_button': 'Начать',
    'exit_button': 'Отмена',
    'check_button': 'Проверить',
    'next_button': 'Следующее слово',
    'result_button': 'Результат'
}

TEST_LEXICON: dict[str, str] = {
    'title': '&#128214; <b>Словарный тест</b>\n\n',
    'result_title': '&#128214; <b>Словарный тест окончен</b>\n\n',
    'topic': 'Тема: ',
    'total_words': 'Количество слов: ',
    'rules': ('Правила:\n- Я буду по очереди присылать слова на русском языке '
              'с вариантами перевода.\n- Необходимо выбирать правильный '
              'вариант ответа.\n- Задание можно прервать командой '
              '/cancel или найти ее в меню'),
    'warning': ('&#128070; <b>В этом задании можно использовать только '
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
    'title': '&#128221; <b>Правописание</b>\n\n',
    'topic': 'Тема: ',
    'total_questions': 'Количество слов: ',
    'rules': ('Правила:\n- Я буду по очереди присылать слова на русском языке'
              '\n- На каждое присланное слово нужно писать его перевод на '
              'английском\n- Перевод можно писать как маленькими, так и '
              'заглавными буквами\n- Задание можно прервать командой '
              '/cancel или найти ее в меню'),
    'result_title': '&#128221; <b>Задание окончено</b>\n\n',
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

PROGRESS_LEXICON: dict[str, str] = {
    'title': '<b>Результаты</b>\n\n',
    'topics': 'Всего тем: ',
    'words': 'Пройденных слов: ',
    'total_tasks': 'Всего заданий: ',
    'passed_tasks': 'Пройденных заданий: '
}

API_ERROR_LEXICON: dict[str, str] = {
    'server_error': 'Ошибка на стороне сервера!',
    'connection_error': 'Ошибка соединения с сервером!',
    'not_found': ('Для незарегистрированных пользователей эта функция '
                  'недоступна!'),
}
