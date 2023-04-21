from django.contrib import admin

from bee.models import Action, Beehive, Queen, Reminder


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


@admin.register(Beehive)
class BeehiveAdmin(admin.ModelAdmin):
    list_display = ('number', 'row_num', 'queen', 'is_active')
    search_fields = ['number']
    list_filter = ['is_active']

    list_per_page = 10


@admin.register(Queen)
class QueenAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'is_active')
    search_fields = ['title']
    list_filter = ['is_active']
    list_per_page = 10
