from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movie',views.movie, name='Movie'),
    path('recommend',views.recommend, name='recommend'),

]