import pytest

from study.models import Task, Topic, Word


@pytest.fixture(autouse=True)
def execute_celery_tasks_locally(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_DEFAULT_RETRY_DELAY = 0
    settings.CELERY_MAX_RETRIES = 0


@pytest.fixture
def word(db):
    return Word.objects.create(origin='origin', translation='translation')


@pytest.fixture
def words(db):
    return Word.objects.bulk_create([Word(origin='one', translation='один'),
                                     Word(origin='two', translation='два'),
                                     Word(origin='three', translation='три'),
                                     Word(origin='four', translation='четыре'),
                                     Word(origin='five', translation='пять')])


@pytest.fixture
def topic(db, words):
    obj = Topic.objects.create(name='topic')
    obj.words.add(*words)
    obj.save()
    return obj


@pytest.fixture
def intro_task(db, topic, user):
    return Task.objects.create(topic=topic, category=Task.INTRO, user=user)


@pytest.fixture
def learn_task(db, topic, user):
    return Task.objects.create(topic=topic, category=Task.LEARN, user=user)


@pytest.fixture
def test_task(db, topic, user):
    return Task.objects.create(topic=topic, category=Task.TEST, user=user)


@pytest.fixture
def spell_task(db, topic, user):
    return Task.objects.create(topic=topic, category=Task.SPELL, user=user)
