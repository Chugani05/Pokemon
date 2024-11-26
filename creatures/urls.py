from django.urls import path

from . import views

app_name = 'creatures'

urlpatterns = [
    path('', views.creature_list, name='creature-list'),
    path('<creature_slug>/', views.creature_detail, name='creature-detail'),
]
