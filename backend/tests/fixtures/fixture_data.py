import pytest

from study.models import Task, Topic, Word


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
