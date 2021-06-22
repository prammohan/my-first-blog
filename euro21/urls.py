from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:group_id>', views.detail, name='detail'),
    path('ACTION_OR_VIEW_URL_ON_SUBMIT_HERE', views.results, name='results'),
]
