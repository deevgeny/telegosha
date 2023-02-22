from rest_framework import serializers

from api.data_processors import (
    prepare_spelling_questions,
    prepare_test_questions,
)
from study.models import Task, Word


class WordSerializer(serializers.ModelSerializer):
    """Word model serializer."""

    class Meta:
        model = Word
        fields = ['origin', 'translation']


class TaskSerializer(serializers.ModelSerializer):
    """Task model serializer."""

    topic = serializers.StringRelatedField()
    data = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'category', 'topic', 'data']

    def get_data(self, obj):
        queryset = obj.topic.words.values_list('origin', 'translation')
        if obj.category == Task.INTRO:
            return list(queryset)
        if obj.category in [Task.TEST, Task.LEARN]:
            return prepare_test_questions(list(queryset))
        if obj.category == Task.SPELL:
            return prepare_spelling_questions(list(queryset))
        return []


class TaskUpdateSerializer(serializers.ModelSerializer):
    """Task model update serializer."""

    class Meta:
        model = Task
        fields = ['correct', 'incorrect']


class TaskResultSerializer(serializers.ModelSerializer):
    """Task model serializer to display results."""

    topic = serializers.StringRelatedField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['topic', 'category', 'passed']

    def get_category(self, obj):
        return obj.get_category_display()


class UserProgressSerializer(serializers.Serializer):
    """User progress serializer."""

    topics = serializers.IntegerField()
    words = serializers.IntegerField()
    total_tasks = serializers.IntegerField()
    passed_tasks = serializers.IntegerField()
