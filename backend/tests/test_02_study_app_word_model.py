import pytest
from django.db import models

from study.models import Word


@pytest.mark.parametrize('class_attr, value',
                         [['verbose_name', 'слово'],
                          ['verbose_name_plural', 'слова'],
                          ['ordering', ['origin']]])
def test_model_meta_class(class_attr, value):
    assert getattr(Word._meta, class_attr) == value, (
        'Word model Meta class should be defined as '
        f'{class_attr}={repr(value)}'
    )


def test_model_str_method(word):
    assert str(word) == f'{word.origin} - {word.translation}', (
        'Word __str__() method should return `self.origin - self.translation`'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Слово'],
                          ['max_length', 30],
                          ['help_text', 'Слово на иностранном языке']])
def test_origin_field(field_attr, value):
    field = 'origin'
    assert getattr(Word._meta.get_field(field), field_attr) == value, (
        f'Word.{field} field should be defined as {field_attr}={repr(value)}'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Перевод'],
                          ['max_length', 30],
                          ['help_text', 'Значение на родном языке']])
def test_translation_field(field_attr, value):
    field = 'translation'
    assert getattr(Word._meta.get_field(field), field_attr) == value, (
        f'Word.{field} field should be defined as {field_attr}={repr(value)}'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Тема'],
                          ['on_delete', models.PROTECT],
                          ['help_text', 'Выберите тематику слова'],
                          ['_related_name', 'words']])
def test_topic_field(field_attr, value):
    field = 'topic'
    if field_attr == 'on_delete':
        assert (getattr(Word._meta.get_field(field).remote_field, field_attr)
                == value), (f'Word.{field} field should be defined as '
                            f'{field_attr}={repr(value)}')
        return
    assert getattr(Word._meta.get_field(field), field_attr) == value, (
        f'Word.{field} field should be defined as {field_attr}={repr(value)}'
    )
