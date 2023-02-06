import pytest

from study.models import Topic


@pytest.mark.parametrize('class_attr, value',
                         [['verbose_name', 'тема'],
                          ['verbose_name_plural', 'темы']])
def test_model_meta_class(class_attr, value):
    assert getattr(Topic._meta, class_attr) == value, (
        'Topic model Meta class should be defined as '
        f'{class_attr}={repr(value)}'
    )


def test_model_str_method(topic):
    assert str(topic) == topic.name, (
        'Topic __str__() method should return `self.name`'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Тема'],
                          ['max_length', 150],
                          ['help_text', 'Укажите тему (категорию) слов'],
                          ['unique', True]])
def test_name_field(field_attr, value):
    field = 'name'
    assert getattr(Topic._meta.get_field(field), field_attr) == value, (
        f'Topic.{field} field should be defined as {field_attr}={repr(value)}'
    )
