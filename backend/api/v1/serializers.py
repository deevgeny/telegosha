import random

from rest_framework import serializers

from study.models import Exercise, Task, Word


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


class WordSerializer(serializers.ModelSerializer):
    """Word model serializer."""

    class Meta:
        model = Word
        fields = ['origin', 'translation']


class ExerciseSerializer(serializers.ModelSerializer):
    """Exercise model serializer."""

    data = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = ['id', 'category', 'topic', 'description', 'data']

    def get_data(self, obj):
        queryset = obj.words.values_list('origin', 'translation')
        if obj.category == Exercise.QUIZ:
            return prepare_quiz_questions(list(queryset))
        elif obj.category == Exercise.SPELLING:
            return prepare_spelling_questions(list(queryset))


class TaskUpdateSerializer(serializers.ModelSerializer):
    """Task model update serializer."""

    class Meta:
        model = Task
        fields = ['correct', 'incorrect']
