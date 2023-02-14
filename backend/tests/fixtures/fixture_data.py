import pytest

from study.models import Result, Task, Topic, Word


@pytest.fixture
def topic(db):
    return Topic.objects.create(
        name='topic'
    )


@pytest.fixture
def word(db, topic):
    return Word.objects.create(
        origin='origin', translation='translation', topic=topic
    )


@pytest.fixture
def task(db, topic, user):
    obj = Task.objects.create(topic=topic, category=Task.QUIZ)
    obj.users.add(user)
    obj.save()
    return obj


@pytest.fixture
def words(db, topic):
    Word.objects.bulk_create(
        [
            Word(origin='one', translation='один', topic=topic),
            Word(origin='two', translation='два', topic=topic),
            Word(origin='tree', translation='три', topic=topic),
            Word(origin='four', translation='четыре', topic=topic),
            Word(origin='five', translation='пять', topic=topic),
        ]
    )


@pytest.fixture
def two_tasks_with_words(db, user, words, topic):
    quiz = Task.objects.create(topic=topic, category=Task.QUIZ)
    spell = Task.objects.create(topic=topic, category=Task.SPELLING)
    quiz.users.add(user)
    spell.users.add(user)
    quiz.save()
    spell.save()
    return quiz, spell


@pytest.fixture
def one_task_passed(db, two_tasks_with_words):
    task_1, _ = two_tasks_with_words
    result = Result.objects.get(task=task_1)
    result.correct = 5
    result.save()
    return result


@pytest.fixture
def two_tasks_passed(db, two_tasks_with_words):
    task_1, task_2 = two_tasks_with_words
    result_1 = Result.objects.get(task=task_1)
    result_1.correct = 5
    result_1.save()
    result_2 = Result.objects.get(task=task_2)
    result_2.correct = 5
    result_2.save()
    return result_1, result_2
