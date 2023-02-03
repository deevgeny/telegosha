from django.contrib import admin

from .models import Exercise, Task, Word


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1


class WordInline(admin.TabularInline):
    """Inline word select widget."""
    model = Exercise.words.through
    extra = 1
    verbose_name = 'слово'
    verbose_name_plural = 'слова'


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    search_fields = ('origin', 'translation')


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('topic', 'category', 'description', '_words')
    inlines = (TaskInline, WordInline)
    exclude = ('words',)

    def _words(self, obj):
        return list(obj.words.all())
    _words.short_description = 'Слова'
    _words.admin_order_field = 'words'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'user', 'correct', 'incorrect', 'passed')
