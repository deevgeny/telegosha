from django.contrib import admin

from .models import Task, Topic, Word


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['id', 'origin', 'translation', 'sound']
    list_display_links = ['origin']
    search_fields = ['origin', 'translation']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'topic', 'category', 'user', 'correct', 'incorrect',
                    'attempts', 'active', 'passed']
    list_filter = ['topic', 'category', 'user__school_group', 'active',
                   'passed']
    # def _words(self, obj):
    #    return list(obj.words.all())

    # _words.short_description = 'Слова'
    # _words.admin_order_field = 'words'


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    list_display_links = ['name']
    filter_horizontal = ['school_groups', 'words']
