import pytest

from study.models import Word


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Слово'],
                          ['max_length', 32],
                          ['help_text', 'Слово на иностранном языке']])
def test_origin_field(field_attr, value):
    field = 'origin'
    assert getattr(Word._meta.get_field(field), field_attr) == value, (
        f'Word.{field} field should be defined as {field_attr}={repr(value)}'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Перевод'],
                          ['max_length', 32],
                          ['help_text', 'Значение на родном языке']])
def test_translation_field(field_attr, value):
    field = 'translation'
    assert getattr(Word._meta.get_field(field), field_attr) == value, (
        f'Word.{field} field should be defined as {field_attr}={repr(value)}'
    )


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
