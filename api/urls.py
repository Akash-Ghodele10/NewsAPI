from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.NewsSearchView.as_view(), name='search'),
    path('history/', views.get_search_history, name='history'),
    path('history/<int:search_history_id>/', views.get_search_results, name='search_results'),
]
