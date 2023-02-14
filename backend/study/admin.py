from django.contrib import admin

from .models import Result, Task, Topic, Word


class ResultInline(admin.TabularInline):
    model = Result
    extra = 1


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['origin', 'translation', 'topic']
    search_fields = ['origin', 'translation']
    list_filter = ['topic']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'topic', 'category']
    inlines = [ResultInline]
    exlude = ['users']

    def _words(self, obj):
        return list(obj.words.all())

    _words.short_description = 'Слова'
    _words.admin_order_field = 'words'


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'user', 'correct', 'incorrect', 'passed']
    list_display_links = ['task']
    list_filter = ['user']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']
