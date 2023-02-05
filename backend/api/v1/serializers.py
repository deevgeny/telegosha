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


class ResultSerializer(serializers.ModelSerializer):
    """Result model update serializer."""

    class Meta:
        model = Result
        fields = ['correct', 'incorrect']
