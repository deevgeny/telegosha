from study.models import Task, Topic


def test_task_creation_sequence(intro_task, user):
    """Check task creation sequence via Task post_save signals."""
    # Test first task category sequence
    start_cat = 'intro'
    obj = intro_task
    assert obj.category == start_cat, (
        f'Newly created task should have category={start_cat}'
    )
    # Test second task category sequence
    obj.correct = 5
    obj.save()
    prev_cat = start_cat
    next_cat = 'learn'
    obj = Task.objects.get(user=user, category=next_cat)
    assert obj.category == next_cat, (
        f'When task with category={prev_cat} is completed, next task should '
        f'be created with category={next_cat} via django signals.'
    )
    # Test third task category sequence
    obj.correct = 5
    obj.save()
    prev_cat = next_cat
    next_cat = 'test'
    obj = Task.objects.get(user=user, category=next_cat)
    assert obj.category == next_cat, (
        f'When task with category={prev_cat} is completed, next task should '
        f'be created with category={next_cat} via django signals.'
    )
    # Test forth task category sequence
    obj.correct = 5
    obj.save()
    prev_cat = next_cat
    next_cat = 'spell'
    obj = Task.objects.get(user=user, category=next_cat)
    assert obj.category == next_cat, (
        f'When task with category={prev_cat} is completed, next task should '
        f'be created with category={next_cat} via django signals.'
    )


def test_topic_task_signals(user, school_group):
    """Check task creation via Topic post_add signal."""
    # Prepare test data
    category = 'intro'
    # Add user to group
    obj_user = user
    obj_user.school_group = school_group
    obj_user.save()
    # Create topic and add group to topic
    obj_topic = Topic.objects.create(name='test')
    obj_topic.school_groups.add(school_group)
    obj_topic.save()
    # Get task object which was created for user
    obj_task = Task.objects.get(user=user, topic=obj_topic)
    # Run test
    assert obj_task.topic == obj_topic, (
        'New task should be created for all users who are in the group which '
        'is added to the new topic school_groups field'
    )
    assert obj_task.category == category, (
        f'Newly created task by Topic signals should have category={category}'
    )
