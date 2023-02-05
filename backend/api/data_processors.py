"""
Data processors for database data.

Helper functions to process and prepare data for telegram bot.
"""
import random


def prepare_quiz_questions(words: list) -> list:
    """Prepare quiz questions with buttons from database data.

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
    counts = [1] * len(words)  # Sampling map
    questions = []
    for i in range(len(words)):
        # Add word and correct button
        q = {'word': words[i][1], 'buttons': [{words[i][0]: 'correct'}]}
        # Remove current word from sampling map
        counts[i] -= 1
        # Sample 2 incorrect buttons
        buttons = random.sample(words, counts=counts, k=2)
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
