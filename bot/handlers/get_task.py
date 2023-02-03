import random

WORDS = [
    ('blue', 'синий'), ('red', 'красный'), ('green', 'зелёный'),
    ('black', 'чёрный'), ('yellow', 'желтый'), ('pink', 'розовый')
]


def get_questions(words: list[tuple[str, str]]
                  ) -> list[dict[str, str | list[dict[str, str]]]]:
    """Prepare questions with bottons from database data.

    Django backend mock function.
    """
    counts = [1] * len(words)
    questions = []
    for i in range(len(words)):
        q = {'word': words[i][1], 'buttons': [{words[i][0]: 'correct'}]}
        counts[i] -= 1
        buttons = random.sample(words, counts=counts, k=2)
        counts[i] += 1
        q['buttons'].extend([{button[0]: 'incorrect'} for button in buttons])
        random.shuffle(q['buttons'])
        questions.append(q)
    random.shuffle(questions)
    return questions


print(get_questions(WORDS))


counts = [0, 1, 1, 1, 1, 1]
n = [1, 2, 3, 4, 5, 6]
for i in range(1000):
    a, b = random.sample(n, counts=counts, k=2)
    if a == b:
        break
    if a == 1 or b == 1:
        break
print(i)
