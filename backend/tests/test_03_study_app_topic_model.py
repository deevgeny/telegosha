import pytest
from django.db import models

from study.models import Topic


@pytest.mark.parametrize('field_attr, result',
                         [['verbose_name', 'Название'],
                          ['help_text', 'Укажите тему (категорию) слов'],
                          ['max_length', 32],
                          ['unique', True]])
def test_name_field(field_attr, result):
    field = 'name'
    assert getattr(Topic._meta.get_field(field), field_attr) == result, (
        f'Topic.{field} field should be defined as '
        f'{field_attr}={repr(result)}'
    )


@pytest.mark.parametrize('field_attr, result',
                         [['verbose_name', 'Описание'],
                          ['help_text', 'Краткое описание темы'],
                          ['max_length', 128],
                          ['blank', True]])
def test_description_field(field_attr, result):
    field = 'description'
    assert getattr(Topic._meta.get_field(field), field_attr) == result, (
        f'Topic.{field} field should be defined as '
        f'{field_attr}={repr(result)}'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Группы'],
                          ['help_text', 'Выбрать группы'],
                          ['_related_name', 'topics']])
def test_school_groups_field(field_attr, value):
    field = 'school_groups'
    if field_attr == 'on_delete':
        assert getattr(Topic._meta.get_field(field).remote_field,
                       field_attr) == value, (
            f'Topic.{field} field should be defined as '
            f'{field_attr}={repr(value)}'
        )
        return
    assert getattr(Topic._meta.get_field(field), field_attr) == value, (
        f'Topic.{field} field should be defined as '
        f'{field_attr}={repr(value)}'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Слова'],
                          ['help_text', 'Выбрать минимум три слова'],
                          ['_related_name', 'topics']])
def test_words_field(field_attr, value):
    field = 'words'
    if field_attr == 'on_delete':
        assert getattr(Topic._meta.get_field(field).remote_field,
                       field_attr) == value, (
            f'Topic.{field} field should be defined as '
            f'{field_attr}={repr(value)}'
        )
        return
    assert getattr(Topic._meta.get_field(field), field_attr) == value, (
        f'Topic.{field} field should be defined as '
        f'{field_attr}={repr(value)}'
    )


@pytest.mark.parametrize('class_attr, value',
                         [['verbose_name', 'тема'],
                          ['verbose_name_plural', 'темы']])
def test_model_meta_class(class_attr, value):
    assert getattr(Topic._meta, class_attr) == value, (
        'Topic model Meta class should be defined as '
        f'{class_attr}={repr(value)}'
    )


def test_model_meta_class_constraints():
    n_of_constraints = 1
    fields = ('name', 'description')
    name = 'Тема с таким названием и описанием уже существует'
    assert len(Topic._meta.constraints) == n_of_constraints, (
        f'Topic model should have {n_of_constraints} constraint(s) in Meta '
        'class'
    )
    assert isinstance(Topic._meta.constraints[0], models.UniqueConstraint), (
        'Incorrect constraint type in Topic model Meta class'
    )
    assert Topic._meta.constraints[0].fields == fields, (
        'Incorrect fields in Meta class constraint'
    )
    assert Topic._meta.constraints[0].name == name, (
        'Incorrect error message in Meta class constraint'
    )


def test_model_str_method(topic):
    assert str(topic) == topic.name, (
        'Topic __str__() method should return `self.name`'
    )
