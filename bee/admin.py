from django.contrib import admin

from bee.models import Action, Beehive, Queen, Reminder, Row, Work, Honey


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('beehive', 'text', 'post_date')
    # fields = ['beehive', 'pub_date', 'text']
    search_fields = ['text']
    list_filter = ['post_date']
    # date_hierarchy = ['post_date']
    list_per_page = 10


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('beehive', 'text', 'post_date', 'is_active')
    search_fields = ['text']
    list_filter = ['post_date', 'is_active']
    # date_hierarchy = ['post_date']
    list_per_page = 10


@admin.register(Row)
class RowAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_per_page = 10


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('post_date', 'display_beehive', 'text')
    list_per_page = 10


@admin.register(Honey)
class HoneyAdmin(admin.ModelAdmin):
    list_display = ('post_date', 'beehive', 'quantity')
    list_per_page = 10


@admin.register(Beehive)
class BeehiveAdmin(admin.ModelAdmin):
    list_display = ('number', 'row', 'queen', 'is_active')
    search_fields = ['number']
    list_filter = ['is_active']

    list_per_page = 10


@admin.register(Queen)
class QueenAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'is_active')
    search_fields = ['title']
    list_filter = ['is_active']
    list_per_page = 10
