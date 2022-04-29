from django.urls import path

from . import views

urlpatterns = [
    # path('upload/', views.get_packets, name='get_packets'),
    path('', views.index, name='index'),
    # path('output/', views.output, name='output')
    # path('get_packets/', views.get_packets, name='get_packets'),
    # path('/', views.upload_file_view, name='upload_file_view'),
]