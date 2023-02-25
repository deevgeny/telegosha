"""
Data processors module.

Helper functions to process and prepare data for specific telegram bot tasks.
"""
import random


def prepare_test_questions(words: list) -> list:
    """Prepare test questions with buttons from database data.

    Input:
    [('blue', 'синий'), ('green', 'зеленый'), ('red', 'красный'),
     ('yellow', 'желтый')]

    Output:
    [{'word': 'желтый', 'buttons': [{'blue': 'incorrect'},
                                    {'green': 'incorrect'},
                                    {'yellow': 'correct'}]},
     {...}, ...
    ]
    """
    incorrect_buttons = 2
    if len(words) < 3:
        return []
    counts = [1] * len(words)  # Sampling map
    questions = []
    for i in range(len(words)):
        # Add word, origin and correct button
        q = {'word': words[i][1], 'origin': words[i][0],
             'buttons': [{words[i][0]: 'correct'}]}
        # Remove current word from sampling map
        counts[i] -= 1
        # Sample k=INCORRECT_BUTTONS incorrect buttons
        buttons = random.sample(words, counts=counts, k=incorrect_buttons)
        # Restore current word in sampling map
        counts[i] += 1
        # Add incorrect buttons
        q['buttons'].extend([{button[0]: 'incorrect'} for button in buttons])
        random.shuffle(q['buttons'])
        questions.append(q)
    random.shuffle(questions)
    return questions


def prepare_spelling_questions(words: list) -> list:
    """Prepare spelling questions from database data.

    Input:
    [('blue', 'синий'), ('green', 'зеленый'), ('red', 'красный'),
     ('yellow', 'желтый')]

    Output:
    [{'word': 'синий',
      'spelling': 'blue'},
     {'word': 'красный',
      'spelling': 'red'},
      {...}, ...
    ]
    """
    questions = []
    for word in words:
        q = {'word': word[1], 'spelling': word[0]}
        questions.append(q)
    random.shuffle(questions)
    return questions
