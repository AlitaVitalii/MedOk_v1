from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('beehive/', views.BeehiveListView.as_view(), name='beehives'),
    path('beehive/<int:pk>/', views.BeehiveDetailView.as_view(), name='beehive_detail'),
    path('beehive/create/', views.BeehiveCreate.as_view(), name='beehive_create'),
    path('beehive/<int:pk>/update/', views.BeehiveUpdate.as_view(), name='beehive_update'),

    path('queen/', views.QueenListView.as_view(), name='queens'),
    path('queen/<int:pk>/', views.QueenDetailView.as_view(), name='queen_detail'),
    path('queen/create/', views.QueenCreate.as_view(), name='queen_create'),
    path('queen/<int:pk>/update/', views.QueenUpdate.as_view(), name='queen_update'),

    path('action/', views.ActionListView.as_view(), name='actions'),
    path('action/<int:pk>/', views.ActionDetailView.as_view(), name='action_detail'),
    path('action/<int:pk>/create/', views.ActionCreate.as_view(), name='action_create'),
    path('action/<int:pk>/update', views.ActionUpdate.as_view(), name='action_update'),

    path('row/', views.RowListView.as_view(), name='rows'),
    path('row/<int:pk>/', views.RowDetailView.as_view(), name='row_detail'),
    path('row/create/', views.RowCreate.as_view(), name='row_create'),
    path('row/<int:pk>/update/', views.RowUpdate.as_view(), name='row_update'),

    path('reminder/', views.ReminderListView.as_view(), name='reminders'),
    path('reminder/<int:pk>/', views.ReminderDetailView.as_view(), name='reminder_detail'),
    path('reminder/<int:pk>/create/', views.ReminderCreate.as_view(), name='reminder_create'),
    path('reminder/<int:pk>/update/', views.ReminderUpdate.as_view(), name='reminder_update'),

    path('reminder/create/', views.ReminderCreat.as_view(), name='rem_create')
]
