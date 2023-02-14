from rest_framework import serializers

from api.data_processors import (
    prepare_quiz_questions,
    prepare_spelling_questions,
)
from study.models import Result, Task, Word


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
        if obj.category == Task.QUIZ:
            return prepare_quiz_questions(list(queryset))
        if obj.category == Task.SPELLING:
            return prepare_spelling_questions(list(queryset))
        return []


class ResultUpdateSerializer(serializers.ModelSerializer):
    """Result model update serializer."""

    class Meta:
        model = Result
        fields = ['correct', 'incorrect']


class ResultSerializer(serializers.ModelSerializer):
    """Result model serializer."""

    topic = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Result
        fields = ['topic', 'category', 'passed']

    def get_topic(self, obj):
        return obj.task.topic.name

    def get_category(self, obj):
        return obj.task.get_category_display()


class UserProgressSerializer(serializers.Serializer):
    """User progress serializer."""

    topics = serializers.IntegerField()
    words = serializers.IntegerField()
    total_tasks = serializers.IntegerField()
    passed_tasks = serializers.IntegerField()
